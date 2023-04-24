"""
./controller/chat_controller.py
"""
from controller.base_controller import BaseController
from controller.continuous_controller import ContinuousController
from concurrent.futures import ThreadPoolExecutor


class ChatController(BaseController):
    def __init__(self, model):
        super().__init__(model)
        self.model = model
        self.continuous_controller = None  # Initialize the continuous_controller as None


    def activate_autonomous_mode(self):
        self.continuous_controller = ContinuousController(self)
        self.continuous_controller.start_autonomous_conversation()

    def send_message(self, user, bot, chat_history):
        chat_history = chat_history
        if bot == "All":
            self.activate_autonomous_mode()
            return

        response = self.get_bot_response(bot, chat_history, user)
        print(response)
        return response




