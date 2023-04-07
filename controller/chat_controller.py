# ./controller/chat_controller.py
from .base_controller import BaseController


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

        return response

    def get_bot_response(self, bot, chat_history):

        agent = self.model.agents.get(bot.lower())
        
        if bot == "All":
            pass
            #response, chat_history = self.get_response_all(chat_history)
            #Todo
        
        response = self.model.get_response(agent, chat_history)
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
        #TODO

    def close_app(self):
        #called from the gui
        #self.model.save_history()
        self.on_exit()
