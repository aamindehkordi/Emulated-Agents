class BaseController:
    def __init__(self, gui):
        self.gui = gui

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
