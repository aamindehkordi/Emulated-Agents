"""
./controller/base_controller.py
"""
from view.base_gui import BaseGUI
from view.discord_gui import DiscordGUI

class BaseController:
    def __init__(self, model):
        self.continuous_controller = None
        self.model = model
        self.base_gui = BaseGUI(self)
        self.chat_gui = DiscordGUI(self)
        self.chat_gui.withdraw()  # Hide the chat_gui initially

    def get_bot_response(self, bot, chat_history):
        agent = self.model.agents.get(bot.lower())
        response = self.model.get_chat_response(agent, chat_history)
        chat_history.append({'role': 'assistant', 'content': f"{response}"})

        return response


    def switch_to_chat_mode(self):
        self.model.mode = 0
        self.base_gui.withdraw()
        self.chat_gui.deiconify()

    def switch_to_base_mode(self):
        self.chat_gui.withdraw()
        self.base_gui.deiconify()

    def switch_to_zoom_mode(self):
        self.model.mode = 2
        self.base_gui.withdraw()
        # self.zoom_gui.deiconify()

    def switch_to_photobooth_mode(self):
        self.model.mode = 1
        self.base_gui.withdraw()
        # self.photobooth_gui.deiconify()
