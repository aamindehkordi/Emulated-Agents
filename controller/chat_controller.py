"""
./controller/chat_controller.py
"""
from .base_controller import BaseController
from controller.continuous_controller import ContinuousController
from concurrent.futures import ThreadPoolExecutor


class ChatController(BaseController):
    def __init__(self, model):
        super().__init__(model)
        self.model = model
        self.chat_gui.set_controller(self)
        self.continuous_controller = None  # Initialize the continuous_controller as None


    def activate_autonomous_mode(self):
        self.continuous_controller = ContinuousController(self)
        self.continuous_controller.start_autonomous_conversation()

    def send_message(self, user, bot, message):
        chat_history = self.chat_gui.get_chat_history()
        if bot == "All":
            self.activate_autonomous_mode()
            return

        response = self.get_bot_response(bot, chat_history)
        print(response)
        return response




