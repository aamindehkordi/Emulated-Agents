"""
./controller/base_controller.py
This module provides the BaseController class, a base class for various controllers in the application.

Classes in this module include:
- BaseController: The base class for other controllers, with common functionality.
"""
import tkinter as tk
from view.base_gui import BaseGUI
from view.discord_gui import DiscordGUI
from model.base_model import BaseModel
# Import the ZoomGUI and PhotoboothGUI when they are implemented
# from view.zoom_gui import ZoomGUI
# from view.photobooth_gui import PhotoboothGUI

class BaseController:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the root window
        self.model = BaseModel()
        self.base_gui = BaseGUI(self)
        self.chat_gui = DiscordGUI(self)
        self.chat_gui.withdraw()  # Hide the chat_gui initially

        # Uncomment these lines when the ZoomGUI and PhotoboothGUI are implemented
        # self.zoom_gui = ZoomGUI(self)
        # self.zoom_gui.withdraw()
        #
        # self.photobooth_gui = PhotoboothGUI(self)
        # self.photobooth_gui.withdraw()

    def run(self):
        self.root.mainloop()

    def switch_to_chat_mode(self):
        self.base_gui.withdraw()
        self.chat_gui.deiconify()
        
    def switch_to_base_mode(self):
        self.chat_gui.withdraw()
        self.base_gui.deiconify()
        
    def switch_to_zoom_mode(self):
        self.base_gui.withdraw()
        #self.zoom_gui.deiconify()
        
    def switch_to_photobooth_mode(self):
        self.base_gui.withdraw()
        #self.photobooth_gui.deiconify()
    
    def on_exit(self):
        """
        Handles the exit event for the application.
        """
        pass