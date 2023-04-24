"""
./model/agent.py
"""
import yaml

class Agent:
    def __init__(self, name):
        self.name = name
        self.msgs = []
        self.model = "gpt-3.5-turbo"
        self.max_tokens = 75
        self.prompt = ""
        self.priming = []
        self.mode = 0
        self.path = "./model/Agents"

    def initialize(self):
        """
        Initialize the agent's prompt, and priming.
        """
        with open(f"{self.path}/{self.name}.yaml", 'r') as f:
            agent = yaml.load(f, Loader=yaml.FullLoader)
            self.set_prompt(agent['prompt'])
            if self.mode == 0:
                self.set_priming(agent['chat_priming'])
            elif self.mode == 1:
                self.set_priming(agent['mirror_priming'])
            elif self.mode == 2:
                self.set_priming(agent['zoom_priming'])


    def get_priming(self):
        return self.priming

    def get_prompt(self):
        return self.prompt

    def get_general(self):
        return self.general

    def get_mode(self):
        return self.mode

    def get_name(self):
        return self.name

    def get_model(self):
        return self.model

    def get_max_tokens(self):
        return self.max_tokens

    def get_msgs(self):
        return self.msgs

    def set_msgs(self, msgs):
        self.msgs = msgs

    def set_priming(self, priming):
        self.priming = priming

    def set_prompt(self, prompt):
        self.prompt = prompt

    def set_model(self, model):
        self.model = model

    def set_max_tokens(self, max_tokens):
        self.max_tokens = max_tokens

    def set_mode(self, mode):
        self.mode = mode
