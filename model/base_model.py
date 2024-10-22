"""
./model/base_model.py
"""
from time import sleep
import sys
import openai
from model.agent import Agent

class BaseModel:
    def __init__(self):
        with open('./key_openai.txt') as f:
            self.key = f.readline().strip()

        self.mode = 0 # 0 = chat, 1 = mirror, 2 = zoom
        self.agents = {}
        self.initialize_agents()

    def initialize_agents(self):
        self.agent_names = ['ali', 'nathan', 'jett', 'kate', 'robby', 'cat', 'kyle']
        for name in self.agent_names:
            agent = Agent(name)
            self.agents[name] = agent
            agent.initialize()
            agent.set_mode(self.mode)

    def load_agent(self, name):
        agent = Agent(name)
        print(agent)
        agent.set_mode(self.mode)
        return agent

    def generate(self, prompt="", user="", model="gpt-3.5-turbo", temperature=0.91, top_p=1, n=1, stream=False, stop="null",
                 max_tokens=350, presence_penalty=0, frequency_penalty=0, max_retry=2, agent=None):
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
        #too long
        retry = 0
        while True:
            try:
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=prompt,
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
                elif model == "gpt-4-32k":
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
                print(oops)
                if 'maximum context length' in str(oops):
                    # pop the first message
                    try:
                        agent.msgs = agent.msgs[1:]
                    except:
                        prompt=prompt[1:]


                retry += 1
                if retry >= max_retry:
                    print(f"Exiting due to an error in ChatGPT:\n {oops}")
                    sys.exit(1)
                print(f'Error communicating with OpenAI:\n {oops}.\n\n Retrying in {2 ** (retry - 1) * 5} seconds...')
                sleep(2 ** (retry - 1) * 5)

