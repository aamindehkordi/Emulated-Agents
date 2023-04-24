"""
./controller/continuous_controller.py
"""
import queue
import random
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from controller.base_controller import BaseController

class ContinuousController(BaseController):
    def __init__(self, chat_controller):
        super().__init__(chat_controller.model)
        self.chat_controller = chat_controller
        self.chat_gui = chat_controller.chat_gui
        self.autonomous_mode_active = False
        self.continuous_history = self.chat_gui.get_chat_history()
        self.message_queue = queue.Queue()

    def toggle_autonomous_mode(self):
        self.autonomous_mode_active = not self.autonomous_mode_active
        if self.autonomous_mode_active:
            self.start_autonomous_conversation()

    def start_autonomous_conversation(self):
        self.autonomous_mode_active = True
        threading.Thread(target=self.run_autonomous_conversation, daemon=True).start()
        self.chat_controller.chat_gui.after(100, self.check_message_queue)

    def run_autonomous_conversation(self):
        while self.autonomous_mode_active:
            response = self.autonomous_conversation_step()
            self.message_queue.put(response)
            time.sleep(2)

    def autonomous_conversation_step(self):
        bot = self.select_next_speaker()
        if self.model.mode == 0:
            response = self.chat_controller.get_bot_response(bot, self.chat_controller.chat_gui.get_chat_history())
        return response

    def select_next_speaker(self):
        available_agents = list(self.model.agents.keys())
        selected_agent = random.choice(available_agents)
        print("Selected agent: ", selected_agent)
        return selected_agent

    def check_message_queue(self):
        try:
            message = self.message_queue.get_nowait()
            self.chat_controller.chat_gui.append_message({'role': 'assistant', 'content': f"{message}"})
        except queue.Empty:
            pass

        if self.autonomous_mode_active:
            self.chat_controller.chat_gui.after(100, self.check_message_queue)
