"""
./view/discord_gui.py
This module provides the DiscordGUI class, which is a chat interface that inherits from the BaseGUI.

Classes in this module include:
- DiscordGUI: The chat interface, extending the BaseGUI class.
"""
import tkinter as tk
from tkinter import ttk
from tkinter import StringVar
from view.base_gui import BaseGUI
#Debugging
#from base_gui import BaseGUI

class DiscordGUI(BaseGUI):
    def __init__(self, controller, theme="equilux", font=("Arial", 12), padx=10, pady=10):
        super().__init__(controller, theme, font, padx, pady)
        
        self.geometry("1400x600")
        self.title("AI Friends Chat Mode")

    def create_main_frame(self):
        # create main frame
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(expand=True, fill=tk.BOTH, padx=self.padx, pady=self.pady)

        # create chat history frame
        self.chat_history = tk.Text(self.main_frame, wrap=tk.WORD, font=self.font, state=tk.DISABLED, bg=self.primary_color, fg=self.text_color)
        self.chat_history.pack(expand=True, fill=tk.BOTH, padx=self.padx, pady=self.pady)

        self.chat_history_list = []
        
        # create input frame
        self.input_frame = ttk.Frame(self.main_frame)
        self.input_frame.pack(fill=tk.X, padx=self.padx, pady=self.pady)

        # create input field
        self.message_entry = tk.Text(self.input_frame, wrap=tk.WORD, font=self.font, height=3, bg=self.tertiary_color, fg=self.text_color)
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
        self.user_options = ["Ali", "Nathan", "Kyle", "Robby", "Jett", "Kate", "Cat", "Jake", "developer"]
        self.bot_var = tk.StringVar(value="Nathan")
        self.bot_options = ["Nathan", "Ali", "Kyle", "Robby", "Jett", "Kate", "Cat", "Jake", "developer", "All"]
        self.user_dropdown = self.create_dropdown(self.input_frame, "User typing:", self.user_options, self.user_var)
        self.bot_dropdown = self.create_dropdown(self.input_frame, "Requested user response:", self.bot_options, self.bot_var)


        
        self.create_developer_frame()
        
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

    def update_user_bot(self, event):
        # Update user_var and bot_var based on the new selection
        self.user_var.set(self.user_dropdown.get())
        self.bot_var.set(self.bot_dropdown.get())
        self.developer_mode()

        
    def create_developer_frame(self):
        self.selected_classes = []
        # Create developer class frame
        self.dev_class_frame = tk.Frame(self.main_frame, bg=self.secondary_color)
        self.dev_class_frame.pack(side=tk.RIGHT, padx=20, pady=20)

        # Add a label for the class selection
        self.class_selection_label = tk.Label(self.dev_class_frame, text="Select Classes:", font=("Arial", 14), bg=self.secondary_color, fg=self.tertiary_color)
        self.class_selection_label.pack(side=tk.TOP, padx=10, pady=(0, 10))

        self.check_boxes = []

        # Create a frame for checkboxes
        self.checkboxes_frame = tk.Frame(self.dev_class_frame, bg=self.secondary_color)
        self.checkboxes_frame.pack(side=tk.TOP, padx=5, pady=5)

        # Add a scrollbar if needed
        self.checkbox_canvas = tk.Canvas(self.checkboxes_frame, bg=self.secondary_color, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.checkboxes_frame, orient="vertical", command=self.checkbox_canvas.yview)
        self.checkboxes_scrollable_frame = ttk.Frame(self.checkbox_canvas)

        # Add checkboxes for each class
        self.checkboxes_scrollable_frame.bind("<Configure>", lambda e: self.checkbox_canvas.configure(scrollregion=self.checkbox_canvas.bbox("all")))
        self.checkbox_canvas.create_window((0, 0), window=self.checkboxes_scrollable_frame, anchor="nw")
        self.checkbox_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.checkbox_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Initially hide checkboxes and dev_class_frame
        self.dev_class_frame.pack_forget()
        
    def on_enter_pressed(self, event):
        #if shift is not pressed, send message
        if not event.state & 0x1:
            self.send_message()
            return "break"
        else:
            self.message_entry.insert(tk.END, "")

    def send_message(self):
        # get user typing and requested user response
        user, bot, message = self.get_ubm()
        if message:

            # get chat history
            self.chat_history_list.append({'role': 'user', 'content': f"{user}: {message}"})

            # clear input entry and insert user message
            self.clear_input()
            self.display_message(user, message)
            
            # get response from selected bot
            response = self.controller.send_message(user, bot, message)

            # display response in chat history
            self.display_response(response)

    def get_ubm(self):
        # get user typing and requested user response
        user = self.user_var.get()
        bot = self.bot_var.get()
        # get message from input entry
        message = self.message_entry.get("1.0", tk.END)
        return user, bot, message
    
    def display_message(self, user, message):
        # display user message in chat history
        tag = f"user_message"
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.insert(tk.END, "{}: {}\n".format(user, message), tag)
        self.chat_history.insert(tk.END, "\n", "newline")
        self.chat_history.config(state=tk.DISABLED)
        self.chat_history.yview_moveto(1.0)

    def display_response(self, response):
        # display bot response in chat history
        tag = f"bot_message"
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.insert(tk.END, "{}\n".format(response), tag)
        self.chat_history.insert(tk.END, "\n", "newline")
        self.chat_history.config(state=tk.DISABLED)
        self.chat_history.yview_moveto(1.0)
     
    def set_controller(self, controller):
        # Set the controller
        self.controller = controller
        self.send_button.config(command=self.send_message) # Update the send button's command with the controller's send_message method
        
        # Create class list for the developer agent
        self.class_list = self.controller.get_all_classes() 
        self.class_var = [StringVar() for _ in self.class_list]
        
        # Add checkboxes for each class
        for i, class_name in enumerate(self.class_list):
            cb = ttk.Checkbutton(self.checkboxes_scrollable_frame, text=class_name, variable=self.class_var[i], onvalue=class_name, offvalue="", command=self.update_class_selection)
            cb.pack(side=tk.TOP, padx=(0, 10), pady=5)
            self.check_boxes.append(cb)
        
        # Update the class selection
        self.update_class_selection()
        
    def remove_default_text(self,event):
        # Remove default text when user clicks on entry
        if self.message_entry.get("1.0", tk.END).strip() == "Type here to chat":
            self.message_entry.delete("1.0", tk.END)
            self.message_entry.config(fg=self.text_color)

    def add_default_text(self,event): 
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

    def developer_mode(self, *args):
        # Show developer class selection frame if developer is selected
        selected_bot = self.bot_var.get()
        if selected_bot == "developer":
            self.dev_class_frame.place(relx=0.75, rely=0.25, anchor="center")
        else:
            self.dev_class_frame.place_forget()
    
    def set_tags(self):
        # configure tags for chat history
        self.chat_history.tag_config("user_message", foreground=self.text_color, background=self.secondary_color, spacing1=5, spacing3=5)
        self.chat_history.tag_config("bot_message", foreground=self.tertiary_color, spacing1=5, spacing3=5) 
        self.chat_history.tag_config("newline", foreground=self.primary_color)
        
    def update_class_selection(self):
        # Update the selected classes
        self.selected_classes = [var.get() for var in self.class_var if var.get() != ""]
        #print("Selected classes:", self.selected_classes)  
        
    def get_selected_classes(self):
        # Return the selected classes
        return self.selected_classes
    
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
        def send_message(self, message):
            print(f"User: {message}")
        def get_all_classes(self):
            return ["class1", "class2", "class3"]

    dummy_controller = DummyController()
    discord_gui = DiscordGUI(dummy_controller)
    discord_gui.set_controller(dummy_controller)
    discord_gui.mainloop()
