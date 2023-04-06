from datetime import timedelta
from time import sleep, time
import sys
import json
from uuid import uuid4
import openai
from model.agent import Agent
from model.tools.david import timestamp_to_datetime, gpt3_embedding
from model.pinecone_handler import PineconeHandler

class BaseModel:
    def __init__(self):
        self.agents = {}
        self.initialize_agents()
        self.key = []
        with open('./key_openai.txt') as f:
            self.key.append(f.readline().strip())

        with open('./key_pinecone.txt') as f:
            self.key.append(f.readline().strip())
            self.environment = f.readline().strip()

        self.pinecone_handler = PineconeHandler(self.key[1], self.environment, "ai-langchain")

    def initialize_agents(self):
        agent_names = ['ali', 'nathan', 'jett', 'kate', 'robby', 'cat', 'kyle', 'jake']
        for name in agent_names:
            prompt_path = f"model/prompts/{name}_prompt.txt"
            history_path = f"model/history/{name}_history.json"
            self.add_agent(name, prompt_path, history_path)

    def add_agent(self, name, prompt_path, history_path):
        agent = Agent(name, prompt_path, history_path)
        self.agents[name] = agent

    def get_response(self, agent, history, k=10):
        """
        Format the query to get the best response from the agent.

        *args:
            agent: Agent object
            history: list of dictionaries containing the chat history
            k: number of nearest neighbors to query from the Pinecone index

        *returns:
            response: string containing the response from the agent
        """
        print("First few entries in Pinecone index:")
        with open('./model/history/embeddings.json', "r") as f:
            embeddings = json.load(f)
        for i, (uuid, embedding) in enumerate(embeddings.items()):
            if i >= 3:
                break
            print(f"{uuid}: {embedding[0:5]}")

        # Get the agent's prompt
        agent_prompt, general_prompt = agent.get_prompt()

        # Get the agent's priming and history
        chat_history_list = agent.get_priming() + history

        # Get the name of the user of the query
        user_name = chat_history_list[-1]['user']

        # 1. Get the query and convert it to a vector
        query = chat_history_list.pop()['content']
        input_vector = gpt3_embedding(query)
        user_message = {
            "id": str(uuid4()),
            "timestamp":str (timestamp_to_datetime(time())),
            "user": str(user_name),
            "message": str(query)
        }
        print(f"Query: {query}")
        print(f"Input vector: {input_vector[0:5]}")

        # Form the agent prompt
        agent.msgs = [
            {'role': 'system', 'content': f'{general_prompt}'},
            {'role': 'user', 'content': f'{agent_prompt}'},
            *chat_history_list
        ]

        # 2. Get the closest vectors for the most similar messages in the Pinecone index
        query_response = self.pinecone_handler.query(queries=[input_vector], top_k=k)
        nearest_ids = [match['id'] for match in query_response['results'][0]['matches']]
        print(f"Query response: {query_response}")
        print(f"Nearest IDs: {nearest_ids}")

        #3. Get the relevant messages from the nexus
        relevant_msgs = []
        i = 0
        while i < len(nearest_ids) and len(relevant_msgs) < 5:
            # Get the message for the nearest ID
            id = nearest_ids[i]
            msg = self.pinecone_handler.get_message(id)
            print(f"Message for ID {id}: {msg}")

            # If the message is None, continue to the next ID
            if msg == None:
                i += 1
                continue
            # If the message is from the agent, add it to the list of relevant messages
            if msg['user'] == agent.name:
                relevant_msgs.append(msg['message'])
            else:
                # for each message after the similar message
                for j in range(i + 1, len(nearest_ids)):
                    # Get the next message
                    msg = self.pinecone_handler.get_message(nearest_ids[j])
                    # If the message is None, continue to the next ID
                    if msg == None:
                        i += 1
                        continue
                    # If the message is from the agent, add it to the list of relevant messages
                    if msg['user'] == agent.name:
                        relevant_msgs.append(msg['message'])
                        i+=1
                        continue
                    # If the message is from the user
                    if msg['user'] == user_name:
                        # Get the next message
                        next_msg = self.pinecone_handler.get_next_message(msg['timestamp'], nearest_ids[j])
                        # If the next message is None, continue to the next ID
                        if next_msg == None:
                            i += 1
                            continue
                        # If the next message is from the agent, add it to the list of relevant messages
                        if next_msg['user'] == agent.name:
                            relevant_msgs.append(next_msg['message'])
                            i+=1
                            continue
                        # if the next message is close in proximity to time to the original message, add it to the list of relevant messages
                        if abs(timestamp_to_datetime(msg['timestamp']) - timestamp_to_datetime(next_msg['timestamp'])) < timedelta(minutes=5):
                            relevant_msgs.append(next_msg['message'])
                            i+=1
                            continue
                i += 1

        print(relevant_msgs)

        # If the list of relevant messages is empty, append the 3 closest message from the index/nexus
        if len(relevant_msgs) == 0:
            for id in nearest_ids[:3]:
                msg = self.pinecone_handler.get_message(id)
                if msg == None:
                    continue
                relevant_msgs.append(msg['message'])
        print(relevant_msgs)
        # 4. Concatenate the relevantmessages into a single string
        concatenated_messages = '\n'.join([msg for msg in relevant_msgs])

        # Add the concatenated messages to the agent's prompt along with the popped query
        agent.msgs += [
            {"role": "user", "content": f"Do not use these verbatim but here are suggestions on how to respond to the next message:{concatenated_messages}"},
            {"role": "user", "content": f"{query}"}
        ]

        # 5. Generate the response from the agent
        output, tokens = self.generate(agent, user=str(user_name))
        timestring = timestamp_to_datetime(time())
        print(output)
        print(agent.msgs)
        # 6. Save the query and output to the nexus and vector index
        agent_message = {
            "id": str(uuid4()),
            "timestamp": str(timestring),
            "user": str(agent.name),
            "message": str(output)
        }

        self.pinecone_handler.save_message(user_message, input_vector)
        self.pinecone_handler.save_message(agent_message, gpt3_embedding(output))

        # 7. Return the response
        return output

    def __del__(self):
        # Properly delete the Pinecone index when the class is destroyed
        self.pinecone_handler.delete_index()

    def generate(self, agent, user="", model="gpt-3.5-turbo", temperature=0.91, top_p=1, n=1, stream=False, stop="null",
                 max_tokens=350, presence_penalty=0, frequency_penalty=0, max_retry=2):
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
                    model=model,
                    messages=agent.msgs,
                    temperature=temperature,
                    top_p=top_p,
                    n=n,
                    stream=stream,
                    stop=stop,
                    max_tokens=max_tokens,
                    presence_penalty=presence_penalty,
                    frequency_penalty=frequency_penalty,
                    user=user
                )

                answer = response["choices"][0]["message"]["content"]  # type: ignore

                if model == "gpt-4":
                    prompt_tokens = response['usage']['prompt_tokens']  # type: ignore
                    completion_tokens = response['usage']['completion_tokens']  # type: ignore
                    total_tokens = response['usage']['total_tokens']  # type: ignore
                    tokens = (total_tokens, prompt_tokens, completion_tokens)
                    print(
                        f"token cost for last response: {prompt_tokens / 1000 * 0.03 + completion_tokens / 1000 * 0.06}")

                if model == "gpt-4-32k":
                    prompt_tokens = response['usage']['prompt_tokens']  # type: ignore
                    completion_tokens = response['usage']['completion_tokens']  # type: ignore
                    total_tokens = response['usage']['total_tokens']  # type: ignore
                    tokens = (total_tokens, prompt_tokens, completion_tokens)
                    print(
                        f"token cost for last response: {prompt_tokens / 1000 * 0.06 + completion_tokens / 1000 * 0.12}")

                else:
                    tokens = (response['usage']['total_tokens'],)  # type: ignore
                    print(f"token cost for last response: {tokens[0] / 1000 * 0.002}")

                return answer, tokens

            except Exception as oops:
                if 'maximum context length' in str(oops):
                    # TODO better solution
                    # cut off the first message
                    agent.msgs = agent.msgs[1:]
                    continue
                retry += 1
                if retry >= max_retry:
                    print(f"Exiting due to an error in ChatGPT: {oops}")
                    sys.exit(1)
                print(f'Error communicating with OpenAI: {oops}. Retrying in {2 ** (retry - 1) * 5} seconds...')
                sleep(2 ** (retry - 1) * 5)

