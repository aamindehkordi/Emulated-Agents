import json

class Agent:
    def __init__(self, name, prompt_path, history_path):
        self.name = name
        self.prompt_path = prompt_path
        self.history_path = history_path
        self.msgs = []
        self.model = "gpt-3.5-turbo"
        self.max_tokens = 350

    def get_prompt(self):
        with open(self.prompt_path, 'r', encoding='utf-8') as f:
            self.prompt = f.read()
            return self.prompt

    def get_history(self):
        try:
            with open(self.history_path, 'r', encoding='utf-8') as f:
                self.history = json.load(f)
                return self.history
        except Exception as e:
            print(e)
            return []

    def save_history(self, history):
        #TODO
        pass