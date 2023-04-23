"""
./main.py
"""
import tkinter as tk
from controller.chat_controller import ChatController
from model.chat_model import ChatModel
from view.base_gui import BaseGUI


class MainApp:
    def __init__(self):
        self.chat_model = ChatModel()
        print("Model initialized")
        self.controller = ChatController(self.chat_model)
        print("Controller initialized")
        self.init_base_gui()
        print("GUI initialized")

    def init_base_gui(self):
        self.gui = BaseGUI(self.controller)

    def on_closing(self):
        self.gui.destroy()
        root = tk.Tk()
        root.destroy()
        exit()

    def run(self):
        self.gui.mainloop()


if __name__ == "__main__":
    app = MainApp()
    app.run()
