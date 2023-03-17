from .base_controller import BaseController
from model.agents.ali.ali import get_response_ali
from model.agents.jett.jett import get_response_jett
from model.agents.nathan.nathan import get_response_nathan
from model.agents.kate.kate import get_response_kate
from model.agents.robby.robby import get_response_robby
from model.agents.cat.cat import get_response_cat
from model.openai_api import get_response
from model.user_selection import predict_user

"""
Handles all the openai API stuff and user responses.
"""
class ChatController(BaseController):
    def __init__(self, gui):
        super().__init__(gui)
        self.continuous_mode = False


    def send_message(self, user, bot, message):
        if message.strip() == "":
            return

        message = message.replace('\n', ' ')

        chat_history = self.gui.get_chat_history()
        chat_history.append({'role': 'user', 'content': f"{user}: {message}"})

    #NEEDS TO BE fixed ----
        if self.continuous_mode:
            response = self.get_bot_response("nathan", chat_history)
        else:
            response = self.get_bot_response(bot, chat_history)

        return response



    def get_bot_response(self, bot, chat_history):
        if bot == "All":
            response, chat_history = self.get_response_all(chat_history)
        else:
            user_list = ['nathan', 'ali', 'jett', 'kate', 'robby', 'cat']
            bot_response_function = {
                "ali": get_response_ali,
                "nathan": get_response_nathan,
                "robby": get_response_robby,
                "jett": get_response_jett,
                "kate": get_response_kate,
                "cat": get_response_cat,
            }
            
            responses = [bot_response_function[user](chat_history) for user in user_list]
            selected_user = predict_user(chat_history, user_list, responses)
            
            response = f"{selected_user}: {bot_response_function[selected_user](chat_history)}"
            chat_history.append({'role': 'assistant', 'content': f"{response}"})
        return response
    #NEEDS TO BE fixed ----

    def toggle_continuous_mode(self):
        self.continuous_mode = not self.continuous_mode


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

    #NEEDS TO BE renewed ----
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
    #NEEDS TO BE renewed ----
    
