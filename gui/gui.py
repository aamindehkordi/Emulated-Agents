import tkinter as tk
import api.chat as chat

class ChatroomGUI:

    def __init__(self, master):
        self.master = master
        master.title("Chatroom")

        # create chatroom frame
        self.chatroom_frame = tk.Frame(master)
        self.chatroom_frame.pack()

        # create chat history text widget
        self.chat_history = tk.Text(self.chatroom_frame, height=20, width=50)
        self.chat_history.pack(side=tk.LEFT, padx=5, pady=5)

        # create input frame
        self.input_frame = tk.Frame(master)
        self.input_frame.pack()

        # create input label
        self.input_label = tk.Label(self.input_frame, text="Type your message here:")
        self.input_label.pack(side=tk.LEFT, padx=5, pady=5)

        # create input entry
        self.input_entry = tk.Entry(self.input_frame, width=40)
        self.input_entry.pack(side=tk.LEFT, padx=5, pady=5)

        # create selector for user typing
        self.user_label = tk.Label(self.input_frame, text="Select user typing:")
        self.user_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.user_var = tk.StringVar(master)
        self.user_var.set("Ali")
        self.user_options = ["Ali", "Nathan", "Kyle", "Robby", "Jett", "Kate", "Cat"]
        self.user_dropdown = tk.OptionMenu(self.input_frame, self.user_var, *self.user_options)
        self.user_dropdown.pack(side=tk.LEFT, padx=5, pady=5)

        # create selector for requested user response
        self.bot_label = tk.Label(self.input_frame, text="Select requested user response:")
        self.bot_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.bot_var = tk.StringVar(master)
        self.bot_var.set("Nathan")
        self.bot_options = ["Ali", "Nathan", "Kyle", "Robby", "Jett", "Kate", "Cat", "all"]
        self.bot_dropdown = tk.OptionMenu(self.input_frame, self.bot_var, *self.bot_options)
        self.bot_dropdown.pack(side=tk.LEFT, padx=5, pady=5)

        # create send button
        self.send_button = tk.Button(self.input_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.LEFT, padx=5, pady=5)

    def send_message(self):
        chatHistory = self.chat_history.get("1.0", tk.END)
        message = self.input_entry.get()
        
        # get user typing and requested user response
        user = self.user_var.get()
        bot = self.bot_var.get()
        temp = ""
        # make API request and get response
        if bot == self.bot_options[0]: # Ali
            temp = chat.get_response_ali(message, chatHistory)
        elif bot == self.bot_options[1]: # Nathan
            temp = chat.get_response_nathan(message, chatHistory)
        elif bot == self.bot_options[3]: # Robby
            temp = chat.get_response_robby(message, chatHistory)  
        """elif bot == self.bot_options[4]: # Jett
            temp = chat.get_response_jett(message, chatHistory)
        elif bot == self.bot_options[5]: # Kate
            temp = chat.get_response_kate(message, chatHistory)
        elif bot == self.bot_options[6]: # Cat
            temp = chat.get_response_cat(message, chatHistory)
        elif bot == self.bot_options[7]: # all
            temp = chat.get_response_all(message, chatHistory)
        """
        response = temp
        # display message and response in chat history
        self.chat_history.insert(tk.END, "{}: {}\n".format(user, message))
        self.chat_history.insert(tk.END, "{}: {}\n".format(bot, response))

        # clear input entry
        self.input_entry.delete(0, tk.END)



