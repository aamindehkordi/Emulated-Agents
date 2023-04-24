"""
./controller/base_controller.py
"""
from view.base_gui import BaseGUI
from view.discord_gui import DiscordGUI
from view.zoom_gui import ZoomGUI


class BaseController:
    def __init__(self, model):
        self.continuous_controller = None
        self.model = model

        self.view = BaseGUI(self)

    def get_bot_response(self, bot, chat_history, user):
        agent = self.model.agents.get(bot.lower())
        response = self.model.get_chat_response(agent, chat_history, user)
        chat_history.append({"role": "assistant", "content": f"{response}"})

        return response

    def switch_to_base_mode(self):
        self.model.mode = 0
        self.view.withdraw()
        self.view = BaseGUI(self)
        self.view.run()

    def switch_to_chat_mode(self):
        self.model.mode = 0
        self.view.withdraw()
        from controller.chat_controller import ChatController

        self.view = DiscordGUI(ChatController(self.model))
        self.view.run()

    def switch_to_zoom_mode(self):
        self.model.mode = 1
        self.view.destroy()
        self.view = ZoomGUI(self)
        self.view.create_main_frame()
        self.view.run()
