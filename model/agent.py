import json


class Agent:
    def __init__(self, name, prompt_path, history_path):
        self.name = name
        self.prompt_path = prompt_path
        self.general_path = "./model/prompts/general_knowledge.txt"
        self.history_path = history_path
        self.msgs = []
        self.model = "gpt-4"
        self.max_tokens = 350

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

    def save_message_metadata(self, metadata):
        unique_id = metadata['uuid']
        with open(f'{self.history_path}/nexus/{unique_id}.json', 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, sort_keys=True, indent=2)

    def save_history(self, history):
        # TODO
        pass
