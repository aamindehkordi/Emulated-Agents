"""
This module provides the BaseController class, a base class for various controllers in the application.

Classes in this module include:
- BaseController: The base class for other controllers, with common functionality.
"""

class BaseController:
    def __init__(self, gui, model):
        self.gui = gui
        self.model = model
        self.token_count = 0

    def update_view(self):
        pass
    
    def on_mode_change(self, mode):
        """
        Handles the mode change event.

        Args:
            mode (str): The new mode (e.g., 'chat', 'zoom', 'photobooth').
        """
        pass

    def on_exit(self):
        """
        Handles the exit event for the application.
        """
        pass
