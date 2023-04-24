"""
./view/discord_gui.py
"""
import tkinter as tk
from tkinter import ttk
from tkinter import StringVar
from view.base_gui import BaseGUI

class DiscordGUI(BaseGUI):
    def __init__(self, controller, theme="equilux", font=("Arial", 12), padx=10, pady=10):
        super().__init__(controller, theme, font, padx, pady)
        self.geometry("1400x600")
        self.title("AI Friends Chat Mode")
        self.chat_history_list = []
        self.user_var = StringVar()
        self.user_options = []
        self.bot_var = StringVar()
        self.bot_options = []


    def update_user_bot(self):
        # Update user_var and bot_var based on the new selection
        self.user_var.set(self.user_dropdown.get())
        self.bot_var.set(self.bot_dropdown.get())

        # Return the new values
        user = self.user_var.get()
        bot = self.bot_var.get()
        message = self.message_entry.get("1.0", tk.END)
        return user, bot, message

    def on_enter_pressed(self, event):
        # if shift is not pressed, send message
        if not event.state & 0x1:
            self.send_message()
            return "break"
        else:
            self.message_entry.insert(tk.END, "")

    def send_message(self):
        # get user typing and requested user response
        user, bot, message = self.update_user_bot()
        print(f"User: {user}, Bot: {bot}, Message: {message}")
        if message:
            # get chat history
            msg = {'role': 'user', 'content': f"{user}: {message}"}
            self.chat_history_list.append(msg)

            # clear input entry and insert user message
            self.clear_input()
            self.display_message(user, message)

            # get response from selected bot
            response = self.controller.send_message(user, bot, self.get_chat_history())

            # display response in chat history
            self.display_response(response)

    def append_message(self, message):
        # append message to chat history
        self.chat_history_list.append(message)
        self.display_response(message['content'])

    def create_main_frame(self):
        # create main frame
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(expand=True, fill=tk.BOTH, padx=self.padx, pady=self.pady)

        # create chat history frame
        self.chat_history = tk.Text(self.main_frame, wrap=tk.WORD, font=self.font, state=tk.DISABLED,
                                    bg=self.primary_color, fg=self.text_color)
        self.chat_history.pack(expand=True, fill=tk.BOTH, padx=self.padx, pady=self.pady)

        # create input frame
        self.input_frame = ttk.Frame(self.main_frame)
        self.input_frame.pack(fill=tk.X, padx=self.padx, pady=self.pady)

        # create input field
        self.message_entry = tk.Text(self.input_frame, wrap=tk.WORD, font=self.font, height=3, bg=self.tertiary_color,
                                     fg=self.text_color)
        self.message_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(self.padx, 0), pady=self.pady)
        self.message_entry.bind("<Return>", self.on_enter_pressed)

        # Set default text for input entry
        self.message_entry.config(fg=self.text_color)

        self.message_entry.bind("<FocusIn>", self.remove_default_text)

        self.message_entry.bind("<FocusOut>", self.add_default_text)

        # create send button
        self.send_button = ttk.Button(self.input_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT, padx=self.padx, pady=self.pady)

        # create reset chat button
        self.reset_button = tk.Button(self.main_frame, text="Reset Chat", command=self.reset_chat)
        self.reset_button.pack(side=tk.BOTTOM, padx=self.padx, pady=self.pady)

        # Create selectors for user typing and requested user response
        self.user_var = tk.StringVar(value="Ali")
        self.user_options = ["Ali", "Nathan", "Kyle", "Robby", "Jett", "Kate", "Cat"]
        self.bot_var = tk.StringVar(value="Nathan")
        self.bot_options = ["Nathan", "Ali", "Kyle", "Robby", "Jett", "Kate", "Cat", "All"]
        self.user_dropdown = self.create_dropdown(self.input_frame, "User typing:", self.user_options, self.user_var)
        self.bot_dropdown = self.create_dropdown(self.input_frame, "Requested user response:", self.bot_options,
                                                 self.bot_var)

    def create_dropdown(self, parent, label_text, options, default_value):
        # create dropdown menu with label
        label = tk.Label(parent, text=label_text, font=self.font, bg=self.secondary_color, fg=self.text_color)
        label.pack(side=tk.LEFT, padx=(self.padx, 0), pady=self.pady)

        # create dropdown menu with options (ComboBox)
        dropdown = ttk.Combobox(parent, textvariable=default_value, values=options, state="readonly")
        dropdown.bind("<<ComboboxSelected>>", self.update_user_bot)
        dropdown.pack(side=tk.LEFT, padx=(0, self.padx), pady=self.pady)

        # Set default value
        dropdown.current(0)

        return dropdown

    def display_message(self, user, message):
        # display user message in chat history
        tag = "user_message"
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.insert(tk.END, "{}: {}\n".format(user, message), tag)
        self.chat_history.insert(tk.END, "\n", "newline")
        self.chat_history.config(state=tk.DISABLED)
        self.chat_history.yview_moveto(1.0)

    def display_response(self, response):
        # display bot response in chat history
        tag = "bot_message"
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.insert(tk.END, "{}\n".format(response), tag)
        self.chat_history.insert(tk.END, "\n", "newline")
        self.chat_history.config(state=tk.DISABLED)
        self.chat_history.yview_moveto(1.0)

    def set_controller(self, controller):
        # Set the controller
        self.controller = controller
        self.send_button.config(
            command=self.send_message)  # Update the send button's command with the controller's send_message method

    def remove_default_text(self, event):
        # Remove default text when user clicks on entry
        if self.message_entry.get("1.0", tk.END).strip() == "Type here to chat":
            self.message_entry.delete("1.0", tk.END)
            self.message_entry.config(fg=self.text_color)

    def add_default_text(self, event):
        # Add default text back if user leaves entry blank
        if self.message_entry.get("1.0", tk.END).strip() == "":
            self.message_entry.insert("1.0", "Type here to chat")
            self.message_entry.config(fg=self.tertiary_color)

    def reset_chat(self):
        # Clear chat history text widget
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.delete('1.0', tk.END)
        self.chat_history.config(state=tk.DISABLED)

        # Clear chat_history_list
        self.chat_history_list = []

    def set_tags(self):
        # configure tags for chat history
        self.chat_history.tag_config("user_message", foreground=self.text_color, background=self.secondary_color,
                                     spacing1=5, spacing3=5)
        self.chat_history.tag_config("bot_message", foreground=self.tertiary_color, spacing1=5, spacing3=5)
        self.chat_history.tag_config("newline", foreground=self.primary_color)

    def get_chat_history(self):
        # Return the chat history
        return self.chat_history_list

    def clear_input(self):
        # Clear the input entry
        self.message_entry.delete("1.0", tk.END)

    def run(self):
        # Run the GUI
        self.set_tags()
        super().run()


if __name__ == "__main__":
    # Example usage
    class DummyController:
        @staticmethod
        def send_message(message):
            print(f"User: {message}")


    dummy_controller = DummyController()
    discord_gui = DiscordGUI(dummy_controller)
    discord_gui.set_controller(dummy_controller)
    discord_gui.mainloop()
