import json


class Agent:
    def __init__(self, name, prompt_path, history_path):
        self.name = name
        self.prompt_path = prompt_path
        self.general_path = "./model/prompts/general_knowledge.txt"
        self.history_path = history_path
        self.msgs = []
        self.model = "gpt-3.5-turbo"
        self.max_tokens = 350
        self.general = ""
        self.prompt = ""
        self.history = []

    def get_prompt(self):
        try:
            with open(self.general_path, 'r', encoding='utf-8') as f:
                self.general = f.read()
            with open(self.prompt_path, 'r', encoding='utf-8') as f:
                self.prompt = f.read()
                return self.prompt, self.general
        except Exception as e:
            print(e)
            return ''

    def get_priming(self):
        try:
            with open(self.history_path, 'r', encoding='utf-8') as f:
                self.history = json.load(f)
                return self.history
        except Exception as e:
            print(e)
            return []
