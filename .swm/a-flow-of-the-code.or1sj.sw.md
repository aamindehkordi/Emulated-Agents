---
id: or1sj
title: A flow of the code
file_version: 1.1.2
app_version: 1.5.5
---

## Introduction

This doc describes the General flow of our system. We will follow its implementation across the various locations so you can understand how the different parts create the full picture.

## Following the flow

<br/>

The main function entry point creates the main class
<!-- NOTE-swimm-snippet: the lines below link your snippet to Swimm -->
### 📄 main.py
```python
51         app = MainApp()
52         app.run()
```

<br/>

In the class init the model, controller, and view modules of the MVC architecture become initialized. We will step through each as we go.
<!-- NOTE-swimm-snippet: the lines below link your snippet to Swimm -->
### 📄 main.py
```python
17     class MainApp:
18         def __init__(self):
19             self.model = BaseModel()
20             self.controller = ChatController(self.model)
21     
22             self.init_base_gui()
23     
24         def init_base_gui(self):
25             self.gui = BaseGUI(self.controller)
26             #self.gui.protocol("WM_DELETE_WINDOW", self.on_closing)
27     
28         def on_closing(self):
29             # Perform cleanup and close the application
30             self.gui.destroy()
31             root = tk.Tk()
32             root.destroy()
33             exit()
34     
35         def run(self):
36             self.gui.mainloop()
```

<br/>

As the base model is initialized it imports the necessary API key's it needs and initializes our vector storage database along with our agents.
<!-- NOTE-swimm-snippet: the lines below link your snippet to Swimm -->
### 📄 model/base_model.py
```python
14     class BaseModel:
15         def __init__(self):
16             self.agents = {}
17             self.initialize_agents()
18             self.key = []
19             with open('./key_openai.txt') as f:
20                 self.key.append(f.readline().strip())
21     
22             # Read the API key and environment from file lines 1 and 2
23             with open('./key_pinecone.txt') as f:
24                 self.key.append(f.readline().strip())
25                 self.environment = f.readline().strip()
26     
27             # initialize pinecone
28             pinecone.init(
29                 api_key=self.key[1],  # find at app.pinecone.io
30                 environment=self.environment  # next to api key in console
31             )
32     
33             self.pine_index = "ai-langchain"
34     
35         def initialize_agents(self):
36             agent_names = ['ali', 'nathan', 'jett', 'kate', 'robby', 'cat', 'kyle', 'jake', 'developer']
37             for name in agent_names:
38                 prompt_path = f"model/prompts/{name}_prompt.txt"
39                 history_path = f"model/history/{name}_history.json"
40                 self.add_agent(name, prompt_path, history_path)
41     
42         def add_agent(self, name, prompt_path, history_path):
43             agent = Agent(name, prompt_path, history_path)
44             self.agents[name] = agent
```

<br/>

Here is the Agent class, it essentially makes it so that only one object is needed to pass around the model rather than a bunch of parameters
<!-- NOTE-swimm-snippet: the lines below link your snippet to Swimm -->
### 📄 model/agent.py
```python
4      class Agent:
5          def __init__(self, name, prompt_path, history_path):
6              self.name = name
7              self.prompt_path = prompt_path
8              self.history_path = history_path
9              self.msgs = []
10             self.model = "gpt-3.5-turbo"
11             self.max_tokens = 350
12     
13         def get_prompt(self):
14             with open(self.prompt_path, 'r', encoding='utf-8') as f:
15                 self.prompt = f.read()
16                 return self.prompt
17     
18         def get_history(self):
19             try:
20                 with open(self.history_path, 'r', encoding='utf-8') as f:
21                     self.history = json.load(f)
22                     return self.history
23             except Exception as e:
24                 print(e)
25                 return []
```

<br/>

<br/>

<br/>

Then the Chat controller gets initialized, there is a bit that it inherits from the base controller however,
<!-- NOTE-swimm-snippet: the lines below link your snippet to Swimm -->
### 📄 controller/chat_controller.py
```python
6      class ChatController(BaseController):
7          def __init__(self, model):
8              super().__init__(model)
9              self.model = model
10             self.chat_gui.set_controller(self)
11             self.token_count = 0
```

<br/>

A lot of the controller code is still WIP though you can see the general initialization regarding the GUI.
<!-- NOTE-swimm-snippet: the lines below link your snippet to Swimm -->
### 📄 controller/base_controller.py
```python
18     class BaseController:
19         def __init__(self, model):
20             self.root = tk.Tk()
21             self.root.withdraw()  # Hide the root window
22             self.model = model
23             self.base_gui = BaseGUI(self)
24             self.chat_gui = DiscordGUI(self)
25             self.chat_gui.withdraw()  # Hide the chat_gui initially
26     
27             # Uncomment these lines when the ZoomGUI and PhotoboothGUI are implemented
28             # self.zoom_gui = ZoomGUI(self)
29             # self.zoom_gui.withdraw()
30             #
31             # self.photobooth_gui = PhotoboothGUI(self)
32             # self.photobooth_gui.withdraw()
33     
34         def run(self):
35             self.root.mainloop()
```

<br/>

Base GUI initialization sets up styling and general functionality like the menu bar,
<!-- NOTE-swimm-snippet: the lines below link your snippet to Swimm -->
### 📄 view/base_gui.py
```python
13     class BaseGUI(ThemedTk):
14         def __init__(self, controller, theme="equilux", font=("Arial", 12), padx=10, pady=10):
15             super().__init__()
16     
17             self.controller = controller
18             self.theme = theme
19             self.font = font
20             self.padx = padx
21             self.pady = pady
22     
23             self.primary_color = "#FFFFFF"  # white
24             self.text_color = "#003049"  # black
25             self.secondary_color = "#669bbc"  # blue
26             self.tertiary_color = "#5B89AE"  # light blue
27             self.quaternary_color = "#ADC4D7"  # some sort of blue
28             self.quinary_color = "#52688F"  # some sort of blue pt 2
29     
30             self.set_theme(self.theme)
31             self.title("AI Friends App")
32             self.geometry("1500x750")
33     
34             self.create_menu_bar()
35             self.create_main_frame()
```

<br/>

And also the main tkinter frame.

This is the first thing one sees when opening the application. It consists of three buttons that lead back to the controller.
<!-- NOTE-swimm-snippet: the lines below link your snippet to Swimm -->
### 📄 view/base_gui.py
```python
69         def create_main_frame(self):
70             main_frame = ttk.Frame(self)
71             main_frame.pack(expand=True, fill=tk.BOTH, padx=self.padx, pady=self.pady)
72     
73             title = ttk.Label(main_frame, text="AI Friends App", font=("Arial", 24))
74             title.pack(pady=(self.pady, 50))
75     
76             chat_button = ttk.Button(main_frame, text="Chat Mode", command=self.controller.switch_to_chat_mode)
77             chat_button.pack(pady=self.pady, ipadx=50, ipady=20)
78     
79             zoom_button = ttk.Button(main_frame, text="Zoom Mode", command=self.controller.switch_to_zoom_mode)
80             zoom_button.pack(pady=self.pady, ipadx=50, ipady=20)
81     
82             photobooth_button = ttk.Button(main_frame, text="Photobooth Mode",
83                                            command=self.controller.switch_to_photobooth_mode)
84             photobooth_button.pack(pady=self.pady, ipadx=50, ipady=20)
85     
86             bottom_frame = ttk.Frame(main_frame)
87             bottom_frame.pack(side=tk.BOTTOM, pady=(50, self.pady))
88     
89             help_button = ttk.Button(bottom_frame, text="Help", command=self.show_help)
90             help_button.pack(side=tk.RIGHT, padx=self.padx)
91     
92             settings_button = ttk.Button(bottom_frame, text="Settings", command=self.settings)
93             settings_button.pack(side=tk.RIGHT, padx=self.padx)
```

<br/>

They essentially just replace the old GUI with the new, let's keep diving through the chat GUI as if the user pressed the chat button.
<!-- NOTE-swimm-snippet: the lines below link your snippet to Swimm -->
### 📄 controller/base_controller.py
```python
37         def switch_to_chat_mode(self):
38             self.base_gui.withdraw()
39             self.chat_gui.deiconify()
40     
41         def switch_to_base_mode(self):
42             self.chat_gui.withdraw()
43             self.base_gui.deiconify()
44     
45         def switch_to_zoom_mode(self):
46             self.base_gui.withdraw()
47             # self.zoom_gui.deiconify()
48     
49         def switch_to_photobooth_mode(self):
50             self.base_gui.withdraw()
51             # self.photobooth_gui.deiconify()
```

<br/>

The discord/ chat GUI can go down a few different branches, but for now let's just pretend the user sent a message to Nathan ( the default user )
<!-- NOTE-swimm-snippet: the lines below link your snippet to Swimm -->
### 📄 view/discord_gui.py
```python
14     
15     class DiscordGUI(BaseGUI):
16         def __init__(self, controller, theme="equilux", font=("Arial", 12), padx=10, pady=10):
17             super().__init__(controller, theme, font, padx, pady)
18             
19             self.geometry("1400x600")
20             self.title("AI Friends Chat Mode")
21     
22         def create_main_frame(self):
23             # create main frame
24             self.main_frame = ttk.Frame(self)
25             self.main_frame.pack(expand=True, fill=tk.BOTH, padx=self.padx, pady=self.pady)
26     
27             # create chat history frame
28             self.chat_history = tk.Text(self.main_frame, wrap=tk.WORD, font=self.font, state=tk.DISABLED, bg=self.primary_color, fg=self.text_color)
29             self.chat_history.pack(expand=True, fill=tk.BOTH, padx=self.padx, pady=self.pady)
30     
31             self.chat_history_list = []
32             
33             # create input frame
34             self.input_frame = ttk.Frame(self.main_frame)
35             self.input_frame.pack(fill=tk.X, padx=self.padx, pady=self.pady)
36     
37             # create input field
38             self.message_entry = tk.Text(self.input_frame, wrap=tk.WORD, font=self.font, height=3, bg=self.tertiary_color, fg=self.text_color)
39             self.message_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(self.padx, 0), pady=self.pady)
40             self.message_entry.bind("<Return>", self.on_enter_pressed)
41     
42             # Set default text for input entry
43             self.message_entry.config(fg=self.text_color)
44     
45             self.message_entry.bind("<FocusIn>", self.remove_default_text)
46     
47             self.message_entry.bind("<FocusOut>", self.add_default_text)
48             
49             # create send button
50             self.send_button = ttk.Button(self.input_frame, text="Send", command=self.send_message)
51             self.send_button.pack(side=tk.RIGHT, padx=self.padx, pady=self.pady)
52             
53             # create reset chat button
54             self.reset_button = tk.Button(self.main_frame, text="Reset Chat", command=self.reset_chat)
55             self.reset_button.pack(side=tk.BOTTOM, padx=self.padx, pady=self.pady)
56     
57             # Create selectors for user typing and requested user response
58             self.user_var = tk.StringVar(value="Ali")
59             self.user_options = ["Ali", "Nathan", "Kyle", "Robby", "Jett", "Kate", "Cat", "Jake", "developer"]
60             self.bot_var = tk.StringVar(value="Nathan")
61             self.bot_options = ["Nathan", "Ali", "Kyle", "Robby", "Jett", "Kate", "Cat", "Jake", "developer", "All"]
62             self.user_dropdown = self.create_dropdown(self.input_frame, "User typing:", self.user_options, self.user_var)
63             self.bot_dropdown = self.create_dropdown(self.input_frame, "Requested user response:", self.bot_options, self.bot_var)
64     
65     
66             
67             self.create_developer_frame()
68             
69         def create_dropdown(self, parent, label_text, options, default_value):
70             # create dropdown menu with label
71             label = tk.Label(parent, text=label_text, font=self.font, bg=self.secondary_color, fg=self.text_color)
72             label.pack(side=tk.LEFT, padx=(self.padx, 0), pady=self.pady)
73             
74             # create dropdown menu with options (ComboBox)
75             dropdown = ttk.Combobox(parent, textvariable=default_value, values=options, state="readonly")
76             dropdown.bind("<<ComboboxSelected>>", self.update_user_bot)
77             dropdown.pack(side=tk.LEFT, padx=(0, self.padx), pady=self.pady)
78             
79             # Set default value
80             dropdown.current(0)
81     
82             return dropdown
83     
84         def update_user_bot(self, event):
85             # Update user_var and bot_var based on the new selection
86             self.user_var.set(self.user_dropdown.get())
87             self.bot_var.set(self.bot_dropdown.get())
88             self.developer_mode()
89     
```

<br/>

From here the controller gets called to send the message.
<!-- NOTE-swimm-snippet: the lines below link your snippet to Swimm -->
### 📄 view/discord_gui.py
```python
131        def send_message(self):
132            # get user typing and requested user response
133            user, bot, message = self.get_ubm()
134            if message:
135    
136                # get chat history
137                self.chat_history_list.append({'role': 'user', 'content': f"{user}: {message}"})
138    
139                # clear input entry and insert user message
140                self.clear_input()
141                self.display_message(user, message)
142                
143                # get response from selected bot
144                response = self.controller.send_message(user, bot, message)
145    
146                # display response in chat history
147                self.display_response(response)
148    
149        def get_ubm(self):
150            # get user typing and requested user response
151            user = self.user_var.get()
152            bot = self.bot_var.get()
153            # get message from input entry
154            message = self.message_entry.get("1.0", tk.END)
155            return user, bot, message
156        
157        def display_message(self, user, message):
158            # display user message in chat history
159            tag = f"user_message"
160            self.chat_history.config(state=tk.NORMAL)
161            self.chat_history.insert(tk.END, "{}: {}\n".format(user, message), tag)
162            self.chat_history.insert(tk.END, "\n", "newline")
163            self.chat_history.config(state=tk.DISABLED)
164            self.chat_history.yview_moveto(1.0)
165    
166        def display_response(self, response):
167            # display bot response in chat history
168            tag = f"bot_message"
169            self.chat_history.config(state=tk.NORMAL)
170            self.chat_history.insert(tk.END, "{}\n".format(response), tag)
171            self.chat_history.insert(tk.END, "\n", "newline")
172            self.chat_history.config(state=tk.DISABLED)
173            self.chat_history.yview_moveto(1.0)
```

<br/>

From here the controller decides who should respond aka which agent should generate a response
<!-- NOTE-swimm-snippet: the lines below link your snippet to Swimm -->
### 📄 controller/chat_controller.py
```python
13         def send_message(self, user, bot, message):
14             if message.strip() == "":
15                 return
16     
17             message = message.replace('\n', ' ')
18     
19             #Chat History from the gui
20             chat_history = self.chat_gui.get_chat_history()
21     
22             # Pass the selected_classes from the GUI to the get_bot_response method
23             response = self.get_bot_response(bot, chat_history, self.chat_gui.selected_classes)
24             return response
25     
26         def get_bot_response(self, bot, chat_history, class_list=None):
27     
28             if class_list is None:
29                 class_list = []
30             agent = self.model.agents.get(bot.lower())
31             
32             if bot == "All":
33                 response, chat_history = self.get_response_all(chat_history)
34     
35             elif bot == "developer":
36                 relevant_code = "\n"
37                 for path, data in self.file_dict.items():
38                     content = data['content']
39                     for class_name in class_list:
40                         if class_name in content:
41                             relevant_code += f"```{path[1:]}\n{data['code']}\n```\n"
42                 
43                 chat_history.append({'role': 'user', 'content': f"Here is a relevant code snippet:{relevant_code}"})
44                 response, tokens = self.get_response_developer(agent, chat_history)
45                 self.token_count = self.token_count + tokens[0]
46                 chat_history.append({'role': 'assistant', 'content': f"{response}"})
47                 return response
48             
49             response, tokens = self.model.get_response(agent, chat_history)
50             self.token_count = self.token_count + tokens[0]
51             chat_history.append({'role': 'assistant', 'content': f"{response}"})
52     
53             return response    
```

<br/>

First the model organizes the order of the prompts, relative info, chat history priming, and querying and then...
<!-- NOTE-swimm-snippet: the lines below link your snippet to Swimm -->
### 📄 model/base_model.py
```python
46         def get_response(self, agent, history, debug=False):
47             """
48                 Gets appropriate user chat response based off the chat history.
49                 
50                 **args:
51                 agent: agent object
52                 history: list of chat history
53                 debug: boolean for debug mode (developer)
54             """
55             if str(agent.name) == "developer":
56                 debug = True
57                 agent.model = "gpt-3.5-turbo-0301"
58                 agent.max_tokens = 810
59                 print("debug mode")
60     
61             agent_prompt = agent.get_prompt()
62             agent_history = [x for x in agent.get_history()] + history  # Long term History TODO
63             query = agent_history.pop()['content']
64     
65             if not debug:
66     
67                 agent.msgs = [
68                     {'role': 'system', 'content': f'{agent_prompt}\n'},
69                     *agent_history
70                 ]
71     
72             else:
73                 agent.msgs = [
74                     {'role': 'system', 'content': f'{agent_prompt}'},
75                     {'role': 'user', 'content': f'{agent_prompt}'},
76                     *agent_history
77                 ]
78     
79             return self.generate_response(query, agent.msgs, agent_prompt)
```

<br/>

({\[<KYLE TALK MORE ON THIS>\]})

<br/>

generates the response
<!-- NOTE-swimm-snippet: the lines below link your snippet to Swimm -->
### 📄 model/base_model.py
```python
161        def generate_response(self, query, agent_msgs, agent_prompt):
162            """
163            """
164            loader = TextLoader('model/prompts/super_prompt.txt')
165            documents = loader.load()
166    
167            text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=50)
168            docs = text_splitter.split_documents(documents)
169    
170            embeddings = OpenAIEmbeddings(openai_api_key=self.key[0])  # type: ignore
171    
172            docsearch = Pinecone.from_documents(docs, embeddings, index_name=self.pine_index)
173            docs = docsearch.similarity_search(query)
174            relevant_doc = docs[0].page_content
175            msg = [
176                {"role": "user", "content": f"""
177                    Maintain your persona and respond appropriately in the following discord conversation.
178                    To assist you in the conversation, you may be provided with some information. 
179                    Only use information from the following information, if the user refers to it.
180                    Do not use multiple lines of information from the document.
181                    Information:\n\n{relevant_doc}\n\n Discord Conversation Hisotry:\n"""},
182                *agent_msgs,
183                {"role": "user", "content": f"{query}"}
184            ]
185    
186            response = openai.ChatCompletion.create(messages=msg, model="gpt-3.5-turbo", temperature=0.91, top_p=1, n=1,
187                                                    stream=False, stop="null", max_tokens=350, presence_penalty=0,
188                                                    frequency_penalty=0)
189            answer = response["choices"][0]["message"]["content"]  # type: ignore
190    
191            tokens = (response['usage']['total_tokens'],)  # type: ignore
192    
193            print(msg, answer, tokens)
194            return answer, tokens
```

<br/>

And then the message gets displayed from the controller into the GUI and the cycle repeats

<br/>

This file was generated by Swimm. [Click here to view it in the app](/repos/Z2l0aHViJTNBJTNBU2VuaW9yLVByb2plY3QlM0ElM0FhYW1pbmRlaGtvcmRp/docs/or1sj).
