# ./controller/chat_controller.py
from .base_controller import BaseController
import json
import os

class ChatController(BaseController):
    def __init__(self, model):
        super().__init__(model)
        self.model = model
        self.chat_gui.set_controller(self)

    def send_message(self, user, bot, message):
        if message.strip() == "":
            return

        message = message.replace('\n', ' ')

        #Chat History from the gui
        chat_history = self.chat_gui.get_chat_history()

        # Pass the selected_classes from the GUI to the get_bot_response method
        response = self.get_bot_response(bot, chat_history)

        self.append_response_to_json_file(message = message, is_assistant= 0, file_path="./model/history/nathan_history.json")
        return response

    def get_bot_response(self, bot, chat_history):

        agent = self.model.agents.get(bot.lower())
        
        if bot == "All":
            pass
            #response, chat_history = self.get_response_all(chat_history)
            #Todo
        
        response = self.model.get_response(agent, chat_history)
        chat_history.append({'role': 'assistant', 'content': f"{response}"})

        self.append_response_to_json_file(message =response, is_assistant= 1, file_path = './model/history/nathan_history.json')

        return response

    def append_response_to_json_file(self, message, is_assistant, file_path):
        is_assistant = bool(is_assistant)
        if is_assistant == 0:
            entry = {
                "role": "user",
                "content": message
            }
        else:
            entry = {
                "role": "assistant",
                "content": message
            }

        # Check if the file exists and create it if it doesn't
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                f.write('[\n')

        # Read the existing content of the file
        with open(file_path, 'r') as f:
            data = f.readlines()

        # If there is already content in the file, add a comma after the last JSON object
        if len(data) > 1:
            file_size = os.path.getsize(file_path)
            with open(file_path, 'r+') as f:
                f.seek(file_size - 2)
                f.write(',\n')

        # Append the entry as a JSON string followed by a newline character
        with open(file_path, 'a') as f:
            json_entry = json.dumps(entry, indent=2)
            f.write(json_entry + "\n]")

    #TODO
    def get_response_all(self,history):
        """
            Get Responses from all agents and formats them into a chat history list
            
            *args:
            history: list of chat history
            
            *returns:
            updated history in this format {'role':'user', 'content':f"{user}: {message}"}
        """
        #TODO

    def close_app(self):
        #called from the gui
        #self.model.save_history()
        self.on_exit()
