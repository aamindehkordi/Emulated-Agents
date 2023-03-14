import tkinter as tk
import model.chat as chat
import view.gui as gui

class ChatGUI(gui.BaseGUI):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        master.title("Chatroom")
        self.create_widgets()

    def create_widgets(self):
        # Your existing widget creation code, moved into a separate method
        # ...
        pass

    def send_message(self):
        user = self.user_var.get()
        bot = self.bot_var.get()
        message = self.input_entry.get()

        if message.strip() == "":
            return
        message = message.replace('\n', ' ')

        self.master.config(cursor="wait")

        self.display_message(user, message, "user")
        self.clear_input()

        # Get the response from the chat model and display it
        response = self.get_response_from_model(user, bot)
        self.display_message(bot, response, "assistant")

        self.master.config(cursor="")

    def get_response_from_model(self, user, bot):
        # Your existing chat model interaction code
        # ...
        return response

    def display_message(self, user, message, role):
        tag = f"{role}_message"
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.insert(tk.END, "{}: {}\n".format(user, message), tag)
        self.chat_history.insert(tk.END, "\n", "newline")
        self.chat_history.config(state=tk.DISABLED)
        self.chat_history.yview_moveto(1.0)

    def clear_input(self):
        self.input_entry.delete(0, tk.END)

