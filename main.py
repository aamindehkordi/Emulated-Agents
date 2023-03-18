"""
This module serves as the entry point for the application.

It initializes the GUI and controller classes and starts the application loop.

Functions in this module include:
- main(): sets up the application and starts the main loop
"""

import tkinter as tk
from controller.chat_controller import ChatController
from view.discord_gui import ChatGUI


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
    
    # create GUI instance
    root = tk.Tk()
    #chatroom = gui.ChatroomGUI(root)
    
    chat_gui = ChatGUI(root)
    chat_controller = ChatController(chat_gui)

    # Set the controller for the chat_gui
    chat_gui.set_controller(chat_controller)

    chat_gui.run()
    root.mainloop()
        
if __name__ == "__main__":
    main()
