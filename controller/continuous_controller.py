"""
./controller/continuous_controller.py
"""
import random

from controller.base_controller import BaseController
import threading, time

class ContinuousController(BaseController):
    def __init__(self, chat_controller):
        super().__init__(chat_controller.model)
        self.chat_controller = chat_controller
        self.chat_gui = chat_controller.chat_gui
        self.autonomous_mode_active = False
        self.continuous_history = self.chat_gui.get_chat_history()

    def toggle_autonomous_mode(self):
        self.autonomous_mode_active = not self.autonomous_mode_active
        if self.autonomous_mode_active:
            self.start_autonomous_conversation()

    def start_autonomous_conversation(self):
        self.autonomous_mode_active = True
        self.run_autonomous_conversation()

    def run_autonomous_conversation(self):
        if self.autonomous_mode_active:
            self.autonomous_conversation_step()
            if self.autonomous_mode_active:  # Check if autonomous_mode_active is still True
                self.chat_controller.chat_gui.after(2000,
                                                    self.run_autonomous_conversation)  # Schedule next step after 2 seconds

    def autonomous_conversation_step(self):
        bot = self.select_next_speaker()
        # Generate the response from the selected speaker
        if self.model.mode == 0:
            response = self.chat_controller.get_bot_response(bot, self.chat_controller.chat_gui.get_chat_history())

        # Update the chat history and display the response in the GUI if autonomous_mode_active is True
        if self.autonomous_mode_active:
            self.chat_controller.chat_gui.append_message({'role': 'assistant', 'content': f"{response}"})

    def select_next_speaker(self):
        available_agents = list(self.model.agents.keys())
        selected_agent = random.choice(available_agents)
        print("Selected agent: ", selected_agent)
        return selected_agent
