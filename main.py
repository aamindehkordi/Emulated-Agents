"""
./main.py
"""
import tkinter as tk
from controller.base_controller import BaseController
from model.chat_model import ChatModel
from view.base_gui import BaseGUI


class MainApp:
    def __init__(self):
        self.view = BaseGUI()
        print("GUI initialized")
        self.model = ChatModel()
        print("Model initialized")
        self.controller = BaseController(self.model, self.view)
        print("Controller initialized")
        self.view.create_main_frame()

    def on_closing(self):
        self.view.destroy()
        root = tk.Tk()
        root.destroy()
        exit()

    def run(self):
        self.view.mainloop()


if __name__ == "__main__":
    app = MainApp()
    app.run()
