"""
./controller/base_controller.py
"""

class BaseController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.set_controller(self)

    def get_bot_response(self, bot, chat_history, user):
        agent = self.model.agents.get(bot.lower())
        response = self.model.get_chat_response(agent, chat_history, user)
        chat_history.append({"role": "assistant", "content": f"{response}"})

        return response

    def switch_to_base_mode(self):
        self.model.mode = 0
        self.view.withdraw()
        from view.discord_gui import BaseGUI
        self.view = BaseGUI()
        self.view.create_main_frame()

    def switch_to_chat_mode(self):
        self.model.mode = 0
        self.view.withdraw()
        from view.discord_gui import DiscordGUI
        from controller.chat_controller import ChatController
        from model.chat_model import ChatModel
        self.model = ChatModel()
        self.view = DiscordGUI()
        controller = ChatController(self.model, self.view)
        self.view.set_controller(controller)
        self.view.create_main_frame()

    def switch_to_zoom_mode(self):
        self.model.mode = 1
        self.view.destroy()
        from view.zoom_gui import ZoomGUI
        self.view = ZoomGUI()
        self.view.set_controller(self)
        self.view.create_main_frame()
        self.view.run()
