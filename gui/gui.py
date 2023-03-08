import tkinter as tk
import requests

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

        # create send button
        self.send_button = tk.Button(self.input_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.LEFT, padx=5, pady=5)

    def send_message(self):
        message = self.input_entry.get()

        # make API request and get response
        response = requests.get("https://api.example.com/chatroom", params={"message": message})
        if response.status_code == 200:
            response_text = response.json()["response"]
        else:
            response_text = "Error: Could not get response from API."

        # display message and response in chat history
        self.chat_history.insert(tk.END, "You: {}\n".format(message))
        self.chat_history.insert(tk.END, "Bot: {}\n".format(response_text))

        # clear input entry
        self.input_entry.delete(0, tk.END)


