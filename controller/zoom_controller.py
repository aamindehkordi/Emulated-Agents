"""
./controller/zoom_controller.py
"""

import controller.base_controller as base_controller
class ZoomController(base_controller.BaseController):
    def __init__(self, view):
        super().__init__(view)
        # Bind buttons or events to controller methods

    # Implement methods to handle events
    def on_start_button_click(self):
        """
        Handles the start button click event in the Zoom GUI.
        """
        pass

    def on_stop_button_click(self):
        """
        Handles the stop button click event in the Zoom GUI.
        """
        pass

    def on_user_join(self, user):
        """
        Handles the event when a user joins the Zoom call.
        
        Args:
            user (str): The user who joined the call.
        """
        pass

    def on_user_leave(self, user):
        """
        Handles the event when a user leaves the Zoom call.
        
        Args:
            user (str): The user who left the call.
        """
        pass
