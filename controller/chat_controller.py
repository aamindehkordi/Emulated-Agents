"""
This module provides the ChatController class, which connects the chatbot model with the user interface.

Classes in this module include:
- ChatController: Handles the communication between the chatbot model and the GUI.
"""
from .base_controller import BaseController
from model.agents.ali.ali import get_response_ali
from model.agents.jett.jett import get_response_jett
from model.agents.nathan.nathan import get_response_nathan
from model.agents.kate.kate import get_response_kate
from model.agents.robby.robby import get_response_robby
from model.agents.cat.cat import get_response_cat
from model.agents.developer.developer import get_response_developer
from model.openai_api import get_response
from model.tools.code_extractor import *
import ast, astor, os

"""
Handles all the openai API stuff and user responses.
"""
class ChatController(BaseController):
    def __init__(self, gui):
        super().__init__(gui)

    def send_message(self, user, bot, message):
        if message.strip() == "":
            return

        message = message.replace('\n', ' ')

        chat_history = self.gui.get_chat_history()

        # Pass the selected_classes from the GUI to the get_bot_response method
        response = self.get_bot_response(bot, chat_history, self.gui.selected_classes)
        return response

    def get_all_classes(self):
        self.file_dict = {}
        name_dict = find_py_files(".")
        for name, path in name_dict.items():
            file_content = read_file_content(path)
            relevant_code = extract_relevant_code(file_content)
            self.file_dict[path] = {'content': file_content, 'code': relevant_code}
        all_classes = []
        for data in self.file_dict.values():
            code = data['code']
            parsed_ast = ast.parse(code)  # Parse the code string into an AST
            classes = [node.name for node in ast.walk(parsed_ast) if isinstance(node, ast.ClassDef)]  # Extract class names from the AST
            all_classes.extend(classes)
        return all_classes

    def get_bot_response(self, bot, chat_history, class_list=[]):
        if bot == "All":
            response, chat_history = self.get_response_all(chat_history)

        elif bot == "developer":
            for path, data in self.file_dict.items():
                content = data['content']
                for class_name in class_list:
                    if class_name in content:
                        chat_history.append({'role': 'user', 'content': f"Here is a relevant code snippet:\n```{path}\n{content}\n```"})
            response, tokens = get_response_developer(chat_history)
            self.token_count = self.token_count + tokens[0]
            chat_history.append({'role': 'assistant', 'content': f"{response}"})
            
        else:
            bot_response_function = {
                "Ali": get_response_ali,
                "Nathan":get_response_nathan,
                #"Kyle":get_response_kyle,
                "Robby":get_response_robby,
                "Jett":get_response_jett,
                "Kate":get_response_kate,
                "Cat": get_response_cat,
                #"Jake": chat.get_response_jake
            }
            response, tokens = bot_response_function[bot](chat_history)
            self.token_count = self.token_count + tokens[0]
            chat_history.append({'role': 'assistant', 'content': f"{response}"})
            
        return response

    def get_response_all(self,history):
        """
            Get Responses from all agents and formats them into a chat history list
            
            *args:
            history: list of chat history
            
            *returns:
            updated history in this format {'role':'user', 'content':f"{user}: {message}"}
        """
        user_list = ['nathan', 'ali', 'jett', 'kate', 'robby', 'cat'] #add more users here
        responses = []
        #Get responses from all agents
        for user in user_list:
            response, tokens = get_response(user, history)
            self.token_count += tokens
            history.append({'role':'assistant', 'content':f"{user}: {response}"})
            
        #Update history
        history = [*history, *responses]
        
        # Clean up responses for display
        for response in responses:
            response['content'] = response['content'].replace('{user}:', '')
        
        return responses, history
    

