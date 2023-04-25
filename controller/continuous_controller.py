"""
./controller/continuous_controller.py
"""
import queue
import random
import threading
import time
from controller.base_controller import BaseController

class ContinuousController(BaseController):
    def __init__(self, model, view):
        super().__init__(model, view)
        self.model = model
        self.view = view
        self.autonomous_mode_active = False
        self.message_queue = queue.Queue()

    def toggle_autonomous_mode(self):
        self.autonomous_mode_active = not self.autonomous_mode_active
        if self.autonomous_mode_active:
            self.start_autonomous_conversation()

    def start_autonomous_conversation(self):
        self.autonomous_mode_active = True
        threading.Thread(target=self.run_autonomous_conversation, daemon=True).start()
        self.view.after(100, self.check_message_queue)

    def run_autonomous_conversation(self):
        while self.autonomous_mode_active:
            response = self.autonomous_conversation_step()
            self.message_queue.put(response)
            time.sleep(2)

    def autonomous_conversation_step(self):
        chat_history = self.view.get_chat_history()
        bot = self.select_next_speaker()
        user = self.view.user_var.get()
        response = self.get_bot_response(bot, chat_history, user)
        return response

    def select_next_speaker(self):
        available_agents = list(self.model.agents.keys())
        selected_agent = random.choice(available_agents)
        print("Selected agent: ", selected_agent)
        return selected_agent

    def check_message_queue(self):
        try:
            message = self.message_queue.get_nowait()
            self.view.append_message({'role': 'assistant', 'content': f"{message}"})
        except queue.Empty:
            pass

        if self.autonomous_mode_active:
            self.view.after(100, self.check_message_queue)
