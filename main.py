"""
This module serves as the entry point for the application.

It initializes the GUI and controller classes and starts the application loop.

Functions in this module include:
- main(): sets up the application and starts the main loop
"""

import tkinter as tk
from controller.chat_controller import ChatController
from view.base_gui import BaseGUI
from view.discord_gui import DiscordGUI
from model.base_model import BaseModel
import openai

class MainApp:
    def __init__(self):
        self.model = BaseModel()
        self.controller = ChatController(self.model)

        self.init_base_gui()

    def init_base_gui(self):
        self.gui = BaseGUI(self.controller)
        self.gui.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        # Perform cleanup and close the application
        self.gui.destroy()
        root = tk.Tk()
        root.destroy()
        exit()
        
    def run(self):
        self.gui.mainloop()

    
def main():
    """
    Main function.
    """
    # Compress videos
    #cleanup.compress_mov_files('./data/preprocessed/text/allUpdates', './data/processed/videos/all_updates')
    #DONE
    
    # Transcribe videos
    #process.transcribe_updates("data/processed/videos/all_updates", "data/preprocessed/text/all_updates")
    #DONE
    
    app = MainApp()
    app.run()
        
if __name__ == "__main__":
    main()
