from .base_controller import BaseController
from model.agents.ali.ali import get_response_ali
from model.agents.jett.jett import get_response_jett
from model.agents.nathan.nathan import get_response_nathan
from model.agents.kate.kate import get_response_kate
from model.agents.robby.robby import get_response_robby
from model.agents.cat.cat import get_response_cat
from model.openai_api import get_response
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
        chat_history.append({'role': 'user', 'content': f"{user}: {message}"})

        response = self.get_bot_response(bot, chat_history)
        return response


    def get_bot_response(self, bot, chat_history):
        if bot == "All":
            response, chat_history = self.get_response_all(chat_history)
        else:
            bot_response_function = {
                "Ali": get_response_ali,
                "Nathan":get_response_nathan,
                #"Kyle":get_response_kyle,
                "Robby":get_response_robby,
                "Jett":get_response_jett,
                "Kate":get_response_kate,
                "Cat": get_response_cat,
                #"Jake": chat.get_response_jake,
            }
            response = bot_response_function[bot](chat_history)
            chat_history.append({'role': 'assistant', 'content': f"{response}"})
        return response

    def on_send_button_click(self):
        """
        Handles the send button click event in the chat GUI.
        """
        pass

    def on_user_dropdown_change(self):
        """
        Handles the user dropdown change event in the chat GUI.
        """
        pass

    def on_target_user_dropdown_change(self):
        """
        Handles the target user dropdown change event in the chat GUI.
        """
        pass
    
    def get_response_todo(self, user, message, target_user):
        """
        Given the user, message, and target user, returns the AI-generated response.
        
        Args:
            user (str): The user sending the message.
            message (str): The content of the message.
            target_user (str): The user expected to respond.
        
        Returns:
            response (str): The AI-generated response.
        """
        pass

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
            response = get_response(user, history)
            history.append({'role':'assistant', 'content':f"{user}: {response}"})
            
        #Update history
        history = [*history, *responses]
        
        # Clean up responses for display
        for response in responses:
            response['content'] = response['content'].replace('{user}:', '')
        
        return responses, history
    
