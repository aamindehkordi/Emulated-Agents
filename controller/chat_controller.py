# ./controller/chat_controller.py
from .base_controller import BaseController
from model.tools.code_extractor import FileSearcher
import ast

class ChatController(BaseController):
    def __init__(self):
        super().__init__()
        self.token_count = 0

    def send_message(self, user, bot, message):
        if message.strip() == "":
            return

        message = message.replace('\n', ' ')

        #Chat History from the gui
        chat_history = self.chat_gui.get_chat_history()

        # Pass the selected_classes from the GUI to the get_bot_response method
        response = self.get_bot_response(bot, chat_history, self.chat_gui.selected_classes)
        return response

    def get_bot_response(self, bot, chat_history, class_list=[]):

        agent = self.model.agents.get(bot.lower())
        
        if bot == "All":
            response, chat_history = self.get_response_all(chat_history)

        elif bot == "developer":
            relevantCode = "\n"
            for path, data in self.file_dict.items():
                content = data['content']
                for class_name in class_list:
                    if class_name in content:
                        relevantCode += f"```{path[1:]}\n{data['code']}\n```\n"
            
            chat_history.append({'role': 'user', 'content': f"Here is a relevant code snippet:{relevantCode}"})
            response, tokens = self.get_response_developer(agent, chat_history)
            self.token_count = self.token_count + tokens[0]
            chat_history.append({'role': 'assistant', 'content': f"{response}"})
            return response
        
        response, tokens = self.model.get_response(agent, chat_history)
        self.token_count = self.token_count + tokens[0]
        chat_history.append({'role': 'assistant', 'content': f"{response}"})

        return response    

    
    def get_response_developer(self, agent, history):
    # Create a dictionary of filename and file contents
      fs = FileSearcher(exclude=[
      '*/.git/*',
      '*/__pycache__/*',
      '*/.DS_Store',
      '*/data/*',
      '*/.idea/*',
      '*/*.mov',
      '*/.vscode/*',
      '*/videos/*',
      '.idea',
      '.vscode',
      'data',
      'videos',
      '.git',
      '.DS_Store',
      '__pycache__',
      '*.pyc'
      ])
      # generate a string of file paths
      file_paths = '\n'.join([path for path in fs.search()])
    
      msgs=[
          {'role':'user', 'content':f"Let me start by showing you the project structure: \n``` \n. = \"/Users/ali/Library/CloudStorage/OneDrive-Personal/Desktop/Other/Coding/School/Senior Project\" \n{file_paths} \n``` \n"}
          ]
      
      
      msgs += history # type: ignore

      answer, tokens = self.model.get_response(agent, msgs) # type: ignore
      return answer, tokens
  
  
    def get_all_classes(self):
        self.file_dict = {}
        fs = FileSearcher()
        name_dict = fs.find_py_files(".")
        for name, path in name_dict.items():
            file_content = fs.read_file_content(path)
            relevant_code = fs.extract_relevant_code(file_content)
            self.file_dict[path] = {'content': file_content, 'code': relevant_code}
        all_classes = []
        for data in self.file_dict.values():
            code = data['code']
            parsed_ast = ast.parse(code)  # Parse the code string into an AST
            classes = [node.name for node in ast.walk(parsed_ast) if isinstance(node, ast.ClassDef)]  # Extract class names from the AST
            all_classes.extend(classes)
        return all_classes
    
        
    
    #TODO
    def get_response_all(self,history):
        """
            Get Responses from all agents and formats them into a chat history list
            
            *args:
            history: list of chat history
            
            *returns:
            updated history in this format {'role':'user', 'content':f"{user}: {message}"}
        """
        user_list = ['nathan', 'ali', 'jett', 'kate', 'robby', 'cat'] #add more users here
        responses = []
        #Get responses from all agents
        for user in user_list:
            response, tokens = self.model.get_response(user, history)
            self.token_count += tokens # type: ignore
            history.append({'role':'assistant', 'content':f"{user}: {response}"})
            
        #Update history
        history = [*history, *responses]
        
        # Clean up responses for display
        for response in responses:
            response['content'] = response['content'].replace('{user}:', '')
        
        return responses, history

    def close_app(self):
        #called from the gui
        #self.model.save_history()
        self.on_exit()
        
    