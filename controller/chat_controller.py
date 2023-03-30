# ./controller/chat_controller.py
from .base_controller import BaseController
import ast

class ChatController(BaseController):
    def __init__(self, model):
        super().__init__(model)
        self.model = model
        self.chat_gui.set_controller(self)
        self.token_count = 0

    def send_message(self, user, bot, message):
        if message.strip() == "":
            return

        message = message.replace('\n', ' ')

        #Chat History from the gui
        chat_history = self.chat_gui.get_chat_history()

        # Pass the selected_classes from the GUI to the get_bot_response method
        response = self.get_bot_response(bot, chat_history)
        return response

    def get_bot_response(self, bot, chat_history):

        agent = self.model.agents.get(bot.lower())
        
        if bot == "All":
            response, chat_history = self.get_response_all(chat_history)
        
        response, tokens = self.model.get_response(agent, chat_history)
        self.token_count = self.token_count + tokens[0]
        chat_history.append({'role': 'assistant', 'content': f"{response}"})

        return response    

    #TODO
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
            response, tokens = self.model.get_response(user, history)
            self.token_count += tokens # type: ignore
            history.append({'role':'assistant', 'content':f"{user}: {response}"})
            
        #Update history
        history = [*history, *responses]
        
        # Clean up responses for display
        for response in responses:
            response['content'] = response['content'].replace('{user}:', '')
        
        return responses, history

    def close_app(self):
        #called from the gui
        #self.model.save_history()
        self.on_exit()