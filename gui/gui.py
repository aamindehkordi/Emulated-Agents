import tkinter as tk
import api.chat as chat

class ChatroomGUI:

    def __init__(self, master):
        self.master = master
        master.title("Chatroom")
        
        # set color palette
        self.primary_color = "#fdf0d5"#cream
        self.text_color = "#003049"#black
        self.secondary_color = "#669bbc"#blue
        self.tertiary_color = "#780000"#red

        # create chatroom frame
        self.chatroom_frame = tk.Frame(master, bg=self.primary_color)
        self.chatroom_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # create chat history text widget
        self.chat_history = tk.Text(self.chatroom_frame, height=20, width=70, bg=self.primary_color, bd=0, font=("Arial", 12), state=tk.DISABLED)
        self.chat_history.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)

        # create input frame
        self.input_frame = tk.Frame(master)
        self.input_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        # create input entry
        self.input_entry = tk.Entry(self.input_frame, width=40, bd=0, font=("Arial", 12), bg=self.primary_color, fg=self.text_color)
        self.input_entry.pack(side=tk.LEFT, padx=(0, 10), ipady=8)
        self.input_entry.bind("<Return>", lambda event: self.send_message())

        # create send button
        self.send_button = tk.Button(self.input_frame, text="Send", bg=self.primary_color, fg=self.tertiary_color, font=("Arial", 12), bd=0, command=self.send_message)
        self.send_button.pack(side=tk.LEFT, ipadx=10, ipady=8)

        # create selectors for user typing and requested user response
        self.user_var = tk.StringVar(value="Ali")
        self.user_options = ["Ali", "Nathan", "Kyle", "Robby", "Jett", "Kate", "Cat", "Jake"]
        self.bot_var = tk.StringVar(value="Nathan")
        self.bot_options = self.user_options + ["All"]
        self.create_dropdown(self.input_frame, "User typing:", self.user_options, self.user_var)
        self.create_dropdown(self.input_frame, "Requested user response:", self.bot_options, self.bot_var)

        # create loading label
        self.loading_label = tk.Label(self.input_frame, text="", font=("Arial", 12), bg=self.secondary_color, fg=self.text_color)
        
    def send_message(self):
        # get user typing and requested user response
        user = self.user_var.get()
        bot = self.bot_var.get()
        message = self.input_entry.get()

        if message.strip() == "":
            return
        # remove new line character from message
        message = message.replace('\n', ' ')

        
        # change cursor to a spinning cursor
        self.master.config(cursor="wait")

        # get chat history
        chatHistory = self.chat_history.get("1.0", tk.END)

        # clear input entry and insert user message
        self.input_entry.delete(0, tk.END)
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.insert(tk.END, "{}: {}\n".format(user, message), "user_message")
        self.chat_history.insert(tk.END, "\n", "newline")
        self.chat_history.config(state=tk.DISABLED)


        # get response from selected bot
        if bot == "All":
            response = chat.get_response_all(message, chatHistory)
        else:
            if bot == "Ali":
                response = chat.get_response_ali(message, chatHistory)
            elif bot == "Nathan":
                response = chat.get_response_nathan(message, chatHistory)
            elif bot == "Kyle":
                response = chat.get_response_kyle(message, chatHistory)
            elif bot == "Robby":
                response = chat.get_response_robby(message, chatHistory)
            elif bot == "Jett":
                response = chat.get_response_jett(message, chatHistory)
            elif bot == "Kate":
                response = chat.get_response_kate(message, chatHistory)
            elif bot == "Cat":
                response = chat.get_response_cat(message, chatHistory)

        # display response in chat history
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.insert(tk.END, "{}: {}\n".format(bot, response), "bot_message")
        self.chat_history.insert(tk.END, "\n", "newline")
        self.chat_history.config(state=tk.DISABLED)
        self.chat_history.yview_moveto(1.0)
        
        # change cursor back to the default cursor
        self.master.config(cursor="")


    def create_dropdown(self, parent, label_text, options, variable):
        # create dropdown menu with label
        label = tk.Label(parent, text=label_text, font=("Arial", 12), bg=self.primary_color, fg=self.tertiary_color)
        label.pack(side=tk.LEFT, padx=(0, 10), pady=5)

        dropdown = tk.OptionMenu(parent, variable, *options)
        dropdown.config(fg=self.tertiary_color, font=("Arial", 12), bd=0)
        dropdown.pack(side=tk.LEFT, pady=5)
        dropdown["menu"].config(bg="white", fg=self.text_color)

    def set_tags(self):
        # configure tags for chat history
        self.chat_history.tag_config("user_message", foreground=self.text_color, background=self.secondary_color)
        self.chat_history.tag_config("bot_message", foreground=self.tertiary_color)
        self.chat_history.tag_config("newline", foreground=self.primary_color)

    def run(self):
        # configure tags and start GUI
        self.set_tags()
        self.master.mainloop()
