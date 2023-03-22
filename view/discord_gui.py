"""
This module provides the DiscordGUI class, which displays a Discord-style chatbot interface.

Classes in this module include:
- DiscordGUI: Displays a Discord-style chatbot interface and handles user input.
"""

import tkinter as tk
from .base_gui import BaseGUI

class ChatGUI(BaseGUI):
    
    def __init__(self, master):
        super().__init__(master)
        self.master.title("Chatroom")
        
        # Create all widgets
        self.create_widgets()

        # Create selectors for user typing and requested user response
        self.user_var = tk.StringVar(value="Ali")
        self.user_options = ["Ali", "Nathan", "Kyle", "Robby", "Jett", "Kate", "Cat", "Jake", "developer"]
        self.bot_var = tk.StringVar(value="Nathan")
        self.bot_options = self.user_options + ["All"]
        self.create_dropdown(self.input_frame, "User typing:", self.user_options, self.user_var)
        self.create_dropdown(self.input_frame, "Requested user response:", self.bot_options, self.bot_var)

        # Create loading label
        self.loading_label = tk.Label(self.input_frame, text="Generating Response...", font=("Arial", 12), bg=self.secondary_color, fg=self.text_color)
        
    def create_widgets(self):
        # Create chatroom frame
        self.chatroom_frame = tk.Frame(self.main_frame, bg=self.primary_color)
        self.chatroom_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Create chat history text widget
        self.chat_history = tk.Text(self.chatroom_frame,height=20, width=70, bg=self.primary_color, fg=self.quinary_color, bd=0, font=("Arial", 13), state=tk.DISABLED)
        self.chat_history.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
        self.chat_history_list = []


        # Create input frame
        self.input_frame = tk.Frame(self.main_frame)
        self.input_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        # Create input entry
        self.input_entry = tk.Entry(self.input_frame, width=40, bd=0, font=("Arial", 13), bg=self.primary_color, fg=self.text_color)
        self.input_entry.pack(side=tk.LEFT, padx=(0, 10), ipady=8)
        self.input_entry.bind("<Return>", lambda event: self.send_message())

        # Set default text for input entry
        self.input_entry.insert(0, 'Type here to chat')
        self.input_entry.config(fg=self.tertiary_color)

        # Remove default text when user clicks on entry
        def remove_default_text(event):
            if self.input_entry.get() == 'Type here to chat':
                self.input_entry.delete(0, tk.END)

        self.input_entry.bind("<FocusIn>", remove_default_text)

        # Add default text back if user leaves entry blank
        def add_default_text(event):
            if not self.input_entry.get():
                self.input_entry.insert(0, 'Type here to chat')

        self.input_entry.bind("<FocusOut>", add_default_text)

        # Bind send_message to return key press
        self.input_entry.bind("<Return>", lambda event: self.send_message())

        # Create send button
        self.send_button = tk.Button(self.input_frame, text="Send", bg=self.primary_color, fg=self.tertiary_color, font=("Arial", 13), bd=0, command=self.send_message)
        self.send_button.pack(side=tk.LEFT, ipadx=10, ipady=8)

        # Create reset chat button
        self.reset_button = tk.Button(self.input_frame, text="Reset Chat", bg=self.primary_color, fg=self.tertiary_color, font=("Arial", 13), bd=0, command=self.reset_chat)
        self.reset_button.pack(side=tk.LEFT, padx=(10, 0), ipadx=10, ipady=8)


    def reset_chat(self):
        # Clear chat history text widget
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.delete('1.0', tk.END)
        self.chat_history.config(state=tk.DISABLED)

        # Clear chat_history_list
        self.chat_history_list = []

    
    def send_message(self):
        # get user typing and requested user response
        user, bot, message = self.get_ubm()

        if message.strip() == "":
            return
        # remove new line character from message
        message = message.replace('\n', ' ')

        # change cursor to a spinning cursor
        self.master.config(cursor="wait")

        # get chat history
        self.chat_history_list.append({'role': 'user', 'content': f"{user}: {message}"})
        chatHistory = self.chat_history_list

        # clear input entry and insert user message
        self.clear_input()
        self.display_message(user, message)

        # get response from selected bot
        response = self.controller.send_message(user, bot, message)

        # display response in chat history
        self.display_response(response)

        # change cursor back to the default cursor
        self.update_cursor()

    def get_ubm(self):
        user = self.user_var.get()
        bot = self.bot_var.get()
        message = self.input_entry.get()
        return user, bot, message
    
    def display_message(self, user, message):
        tag = f"user_message"
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.insert(tk.END, "{}: {}\n".format(user, message), tag)
        self.chat_history.insert(tk.END, "\n", "newline")
        self.chat_history.config(state=tk.DISABLED)
        self.chat_history.yview_moveto(1.0)

    def display_response(self, response):
        tag = f"bot_message"
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.insert(tk.END, "{}\n".format(response), tag)
        self.chat_history.insert(tk.END, "\n", "newline")
        self.chat_history.config(state=tk.DISABLED)
        self.chat_history.yview_moveto(1.0)
        
    def set_controller(self, controller):
        self.controller = controller
        self.send_button.config(command=self.send_message) # Update the send button's command with the controller's send_message method

    def create_dropdown(self, parent, label_text, options, variable):
        # create dropdown menu with label
        label = tk.Label(parent, text=label_text, font=("Arial", 13), bg=self.tertiary_color, fg=self.primary_color )
        label.pack(side=tk.LEFT, padx=(0, 10), pady=5)

        dropdown = tk.OptionMenu(parent, variable, *options)
        dropdown.config(fg=self.primary_color, font=("Arial", 13), bd=0)
        dropdown.pack(side=tk.LEFT, pady=5)
        dropdown["menu"].config(bg="white", fg=self.text_color)

    def set_tags(self):
        # configure tags for chat history
        self.chat_history.tag_config("user_message", foreground=self.text_color, background=self.secondary_color)
        self.chat_history.tag_config("bot_message", foreground=self.tertiary_color)
        self.chat_history.tag_config("newline", foreground=self.primary_color)

    def switch_to_chat(self):
        # Do nothing, already in chat mode
        pass

    def switch_to_zoom(self):
        # Implement switching to zoom mode
        pass

    def switch_to_photobooth(self):
        # Implement switching to photobooth mode
        pass

    def update_cursor(self):
        self.master.config(cursor="")
        
    def get_chat_history(self):
        return self.chat_history_list
    
    def clear_input(self):
        self.input_entry.delete(0, tk.END)
        
    def run(self):
        self.set_tags()
        super().run()
