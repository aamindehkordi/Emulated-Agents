from time import sleep
import openai
import whisper
import json
from model.agent import Agent
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.document_loaders import TextLoader
from langchain.document_loaders import TextLoader
from langchain.llms import OpenAI
import pinecone


class BaseModel:
    def __init__(self):
        self.agents = {}
        self.initialize_agents()

    def initialize_agents(self):
        agent_names = ['ali', 'nathan', 'jett', 'kate', 'robby', 'cat', 'kyle', 'jake', 'developer']
        for name in agent_names:
            prompt_path = f"model/prompts/{name}_prompt.txt"
            history_path = f"model/history/{name}_history.json"
            self.add_agent(name, prompt_path, history_path)

    def add_agent(self, name, prompt_path, history_path):
        agent = Agent(name, prompt_path, history_path)
        self.agents[name] = agent
    
    def get_response(self, agent, history, debug=False):
        """
            Gets appropriate user chat response based off the chat history.
            
            **args:
            agent: agent object
            history: list of chat history
            debug: boolean for debug mode (developer)
            
        """
        if str(agent.name) == "developer":
            debug = True
            agent.model = "gpt-3.5-turbo-0301"
            agent.max_tokens = 810
            print("debug mode")

        agent_prompt = agent.get_prompt()
        agent_history = [x for x in agent.get_history()] + history #Long term History TODO
        query = agent_history.pop()['content']

        general_knowledge_file = "model/prompts/super_prompt.txt"

        if not debug:
            
            agent.msgs = [
                {'role':'system', 'content': f'{agent_prompt}\n'},
                *agent_history
            ]

        else:
            agent.msgs = [
                {'role':'system', 'content': f'{agent_prompt}'},
                {'role':'user', 'content': f'{agent_prompt}'},
                *agent_history
            ]
        
        return self.generate_response(query, agent.msgs, agent_prompt)

    def generate(self, agent, model="gpt-3.5-turbo", temperature=0.91, top_p=1, n=1, stream=False, stop= "null", max_tokens=350, presence_penalty=0, frequency_penalty=0, debug=False, max_retry = 2):
        """
            Generates a response from the OpenAI API.
            
            *args:
            model: the name of the model to use
            temperature: What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. We generally recommend altering this or top_p but not both.
            top_p: An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.
            n: How many chat completion choices to generate for each input_msg message.
            stream: If set, partial message deltas will be sent, like in ChatGPT. Tokens will be sent as data-only server-sent events as they become available, with the stream terminated by a data: [DONE] message.
            stop: Up to 4 sequences where the API will stop generating further tokens.
            max_tokens: The maximum number of tokens to generate.
            presence_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics.
            frequency_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.
        
            *returns:
            response: a string containing the chat response
            token_count: an int containing the number of tokens used
        """
        retry = 0
        while True:
            try:
                response = openai.ChatCompletion.create(
                model=model, # the name of the model to use
                messages=agent.msgs,
                temperature=temperature, #What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. We generally recommend altering this or top_p but not both.
                top_p=top_p, #An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.
                n=n, #How many chat completion choices to generate for each input_msg message.
                stream=stream, #If set, partial message deltas will be sent, like in ChatGPT. Tokens will be sent as data-only server-sent events as they become available, with the stream terminated by a data: [DONE] message.
                stop= stop,
                max_tokens=max_tokens,
                presence_penalty=presence_penalty,
                frequency_penalty=frequency_penalty,
                )
                
                answer = response["choices"][0]["message"]["content"] # type: ignore
                
                if model=="gpt-4":
                    prompt_tokens = response['usage']['prompt_tokens'] # type: ignore
                    completion_tokens = response['usage']['completion_tokens'] # type: ignore
                    total_tokens = response['usage']['total_tokens'] # type: ignore
                    tokens = (total_tokens, prompt_tokens, completion_tokens)
                    print(f"token cost for last response: {prompt_tokens/1000*0.03 + completion_tokens/1000*0.06}")
                    
                if model=="gpt-4-32k":
                    prompt_tokens = response['usage']['prompt_tokens'] # type: ignore
                    completion_tokens = response['usage']['completion_tokens'] # type: ignore
                    total_tokens = response['usage']['total_tokens'] # type: ignore
                    tokens = (total_tokens, prompt_tokens, completion_tokens)
                    print(f"token cost for last response: {prompt_tokens/1000*0.06 + completion_tokens/1000*0.12}")
                
                else:
                    tokens = (response['usage']['total_tokens'],) # type: ignore
                    print(f"token cost for last response: {tokens[0]/1000*0.002}")
                
                if debug:
                    #write response to history file ./model/agents/{user}/{user}_history.json
                    agent.save_history(answer)
                    #TODO add permanent history
                    
                return answer, tokens
            
            except Exception as oops:
                if 'maximum context length' in str(oops):
                    #TODO better solution
                    #cut off the first message
                    agent.msgs = agent.msgs[1:]
                    continue
                retry += 1
                if retry >= max_retry:
                    print(f"Exiting due to an error in ChatGPT: {oops}")
                    exit(1)
                print(f'Error communicating with OpenAI: {oops}. Retrying in {2 ** (retry - 1) * 5} seconds...')
                sleep(2 ** (retry - 1) * 5)

    def generate_response(self, query, agent_history, agent_prompt):
        # Add the code here, using the input parameters instead of hard-coded values
        loader = TextLoader('model/prompts/super_prompt.txt')
        documents = loader.load()

        text_splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=100)
        docs = text_splitter.split_documents(documents)
        
        key = "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"
        embeddings = OpenAIEmbeddings(openai_api_key=key)

        # Read the API key and environment from file lines 1 and 2
        """with open('./key_pinecone.txt') as f:
            api_key = f.readline().strip()
            environment = f.readline().strip()"""
        api_key = "3ad35bc4-f126-413d-8e1c-7b9c6344fab4"
        environment = "us-west4-gcp"
        # initialize pinecone
        pinecone.init(
            api_key=api_key,  # find at app.pinecone.io
            environment=environment  # next to api key in console
        )
        
        index_name = "ai-langchain"

        docsearch = Pinecone.from_documents(docs, embeddings, index_name=index_name)
        docs = docsearch.similarity_search(query)

        relevant_doc = docs[0].page_content
        print(f'relevant doc:\n{relevant_doc}')
        msg = [{'role':'system', 'content': f'{agent_prompt}'}, 
            *agent_history, 
            { "role": "user", "content": 
                f"""As Nathan, you are currently in a conversation with Kyle. 
                Maintain your persona and respond appropriately to his query [{query}]. 
                To assist you in the conversation, you may be provided with some information. 
                However, you should only use the information that is relevant to the current conversation and keep your response concise. 
                Do not use multiple lines of information from the document.
                Please see the following document for information:\n\n{relevant_doc}""" }]
        response = openai.ChatCompletion.create(messages=msg, model="gpt-3.5-turbo", temperature=0.91, top_p=1, n=1, stream=False, stop= "null", max_tokens=350, presence_penalty=0, frequency_penalty=0)
        answer = response["choices"][0]["message"]["content"]

        tokens = (response['usage']['total_tokens'],)

        print(answer, tokens)
        return answer, tokens
    
    def transcribe_video(self, fn_in, model="medium", prompt="", language="en", fp16=False, temperature=0):
        """ Transcribes a video file and returns the transcript.
        *args:
            fn_in: Input filename of the video to transcribe.
            model_size: The size of the model to use. Options are "tiny, "small", "base", "medium", and "large".
            prompt: The prompt to use for the model.
            language: The language to use for the model.
            fp16: Whether or not to use fp16 for the model.
        *returns:
            The transcript of the video.
        """
        # Load the model
        model = whisper.load_model(model)

        # Load the audio
        audio = whisper.load_audio(fn_in)
        
        # Transcribe the audio
        result = model.transcribe(audio, prompt=prompt, language=language, fp16=fp16, temperature=temperature)
        
        # Return the result
        return result["text"]