from .base_controller import BaseController
import model.chat as chat

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


    def get_bot_response(self, bot, chat_history):
        if bot == "All":
            response, chat_history = chat.get_response_all(chat_history)
        else:
            bot_response_function = {
                "Ali": chat.get_response_ali,
                "Nathan": chat.get_response_nathan,
                #"Kyle": chat.get_response_kyle,
                "Robby": chat.get_response_robby,
                "Jett": chat.get_response_jett,
                "Kate": chat.get_response_kate,
                "Cat": chat.get_response_cat,
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
