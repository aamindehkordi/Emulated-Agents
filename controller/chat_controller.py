import controller.base_controller as base_controller
class ChatController(base_controller.BaseController):
    def __init__(self, view):
        super().__init__(view)
        self.view.send_button.config(command=self.send_message)
        self.view.input_entry.bind("<Return>", lambda event: self.send_message())

    def send_message(self):
        # Implementation of send_message
        pass
    
    def on_send_button_click(self):
        """
        Handles the send button click event in the chat GUI.
        """
        pass

    def on_user_dropdown_change(self):
        """
        Handles the user dropdown change event in the chat GUI.
        """
        pass

    def on_target_user_dropdown_change(self):
        """
        Handles the target user dropdown change event in the chat GUI.
        """
        pass
