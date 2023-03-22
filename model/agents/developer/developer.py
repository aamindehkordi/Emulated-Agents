from model.openai_api import get_response
import os
import re
import ast

import ast
import astor

class CodeExtractor(ast.NodeVisitor):
    def __init__(self):
        self.relevant_code = ""

    def visit_ClassDef(self, node):
        self.relevant_code += astor.to_source(node) + "\n"

    def visit_FunctionDef(self, node):
        self.relevant_code += astor.to_source(node) + "\n"

    def visit_AsyncFunctionDef(self, node):
        self.relevant_code += astor.to_source(node) + "\n"

def extract_relevant_code(file_content):
    tree = ast.parse(file_content)
    extractor = CodeExtractor()
    extractor.visit(tree)
    return extractor.relevant_code

def find_py_files(directory, min_lines=65):
    py_files = {}
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    content = f.read()
                    lines = content.strip().split('\n')
                    if len(lines) >= min_lines:
                        py_files[file_path] = file_path
    return py_files

def read_file_content(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def get_response_developer(history):
    # Create a dictionary of filename and file contents
    file_dict = {}
    name_dict = find_py_files(".")
    
    for name, path in name_dict.items():
        file_content = read_file_content(path)
        relevant_code = extract_relevant_code(file_content)
        file_dict[path] = relevant_code
    
    msgs=[{'role':'assistant', 'content': "[Pythia](#inner_monologue)\nI am a python assistant and coach. The following is the summary of the project the USER is working on. My job is to help them develop their project in any way I can, including brainstorming, designing, implementing, and testing. We may engage in developmental editing, which includes restructuring or modifying file structure, folders, and developing of classes and their functions. We may also work on finer grained aspects such as debugging, abstracting, summarizing, and so on. I should refer to highly professional python concepts. I should not seek to push the developer, but rather to teach them when I perceive gaps in their understanding. Above all else, my primary mission is to help them produce an amazing senior project.\nUnderstood, I am Pythia, a python assistant and coach. How may I help you?"}, 
          {'role':'user', 'content':f"Hi Pythia I am working on my senior project at University and with the release of a lot of these new AI models, me and my friends have decided to create a creative and humorous deepfake application of our friend group having LLM simulate us. I will share the agent prompts later, however let me begin by showing you the readme: \n```./readme.md \n# Senior Project \nThis senior project aims to create an interactive AI chatroom with three distinct modes, simulating a conversation with an AI version of friends in a group. The project includes a text-based chat GUI, a zoom call simulation, and a photobooth-style live webcam conversation. \nThis project is a chatbot application built using the OpenAI GPT-3.5-turbo model. The project is structured using the Model-View-Controller (MVC) pattern to separate the concerns of the application and make it more modular and maintainable. \n## Modes \n1. **Text-based Chat GUI**: In this mode, users can type a message and receive a response from an AI version of someone in the friend group. The system should be able to semantically understand/guess who should respond. Users can also toggle a continuous conversation mode where the AI friends keep responding to each other until the stop button is pressed. \n2. **Zoom Call Simulation**: In this mode, a looping short video of all AI friends is displayed in a layout resembling a Zoom call. Each AI friend has its own voice synthesis and lip filter, making it look like they are talking while they speak. The AI friends can engage in a continuous conversation with each other. \n3. **Photobooth-style Live Webcam**: In this mode, a live webcam detects the user in front of the computer and selects their AI and voice synthesis. The user speaks, and the AI version of themselves talks back to them through their mirrored webcam feed. \n## Project Structure \nThe project follows the Model-View-Controller (MVC) architecture: \n### Model \nThe Model directory contains all the logic related to the chatbot and its interaction with the OpenAI API. \n- `openai_api.py`: Handles the interaction with the OpenAI API. \n- `agents`: Contains agent-specific logic and prompt files. \n  - Each agent has its own subdirectory with a Python file (e.g., `ali.py`, `jett.py`) containing the agent's `get_response_*` function, and a text file (e.g., `ali_prompt.txt`, `jett_prompt.txt`) containing the agent's prompt. \n  - `general_knowledge.txt`: Contains general knowledge information shared by all agents. \n### View \nThe View directory contains all the user interface components. \n- `base_gui.py`: Contains the base class for the GUI. \n- `discord_gui.py`: Contains the Discord-style GUI implementation. \n- `zoom_gui.py`: Contains the Zoom-style GUI implementation. \n- `photobooth_gui.py`: Contains the Photobooth-style GUI implementation. \n### Controller \nThe Controller directory contains the logic to connect the Model and the View. \n- `base_controller.py`: Contains the base class for controllers. \n- `chat_controller.py`: Contains the controller class for the chatbot application. It connects the chatbot model with the GUI view. \n- `zoom_controller.py`: Contains the controller class for the Zoom GUI. \n- `photobooth_controller.py`: Contains the controller class for the Photobooth GUI. \n## Next Steps \n1. Implement the user selection and continuous conversation functionality in the text-based chat GUI. \n2. Plan and implement speech synthesis for each AI friend. \n3. Develop the zoom call simulation and photobooth-style live webcam modes, incorporating voice synthesis and lip sync. \n4. Implement user recognition for the photobooth-style live webcam mode. \n## Future Enhancements \nAs the project progresses, new features and enhancements may be considered, such as improving the AI friends' conversational abilities, refining the user experience, and incorporating additional modes or functionalities. \n``` \nAll in all what I have planned for this project is for there to be three different modes in the GUI. One mode is what exists now which is a text-based chat GUI in that the user can type a message and get a response from an AI version of someone in the friend group. Right now you have to manually select who the current user is and who will respond, however I want the system to semantically understand/ guess who should respond. I also want a toggle where once a user enters a message the ai responds and the others respond to each other in a while loop until a stop button is pressed. The other two modes have yet to be implemented as they require speech synthesis and we have not yet planned that out, however I will still explain them to you for future context. One mode is a zoom call kind of vibe where a looping short video of all the ai's are laid out and they are always talking to each other. Each one would have their own voice synthesis and a lip filter on top of their video so that they look like they are talking while they speak. The final mode for the project would be a singular live webcam, similar to apple's photobooth, that detects the user that is in front of the computer and selects their Ai and synthesis, the user sitting in front of the computer would speak and when they are done the AI version of themself would talk back to them through their mirrored webcam feed. Let me now begin to show you the contents of each file, this will all just be to give you more context so that you can assist me better for the future of this project. Let's start with the project structure: \n``` \n. = \"/Users/ali/Library/CloudStorage/OneDrive-Personal/Desktop/Other/Coding/School/Senior Project\" \n./controller \n./controller/chat_controller.py \n./controller/zoom_controller.py \n./controller/photobooth_controller.py \n./controller/base_controller.py \n./README.md \n./.gitignore \n./model \n./model/tools \n./model/tools/cleanup.py \n./model/tools/process.py \n./model/agents \n./model/agents/cat \n./model/agents/cat/cat.py \n./model/agents/cat/cat_prompt.txt \n./model/agents/kyle \n./model/agents/kate \n./model/agents/kate/kate_prompt.txt \n./model/agents/kate/kate.py \n./model/agents/jake \n./model/agents/jett \n./model/agents/jett/jett.py \n./model/agents/jett/jett_prompt.txt \n./model/agents/robby \n./model/agents/robby/robby_prompt.txt \n./model/agents/robby/robby.py \n./model/agents/nathan \n./model/agents/nathan/nathan.py \n./model/agents/nathan/nathan_prompt.txt \n./model/agents/general_knowledge.txt \n./model/agents/ali \n./model/agents/ali/ali_prompt.txt \n./model/agents/ali/ali.py \n./model/openai_api.py \n./model/user_selection.py \n./model/deepfake \n./model/deepfake/lip_sync.py \n./model/deepfake/voice_synthesis.py \n./model/deepfake/user_recognition.py \n./model/continuous_conversation.py \n./view \n./view/base_gui.py \n./view/discord_gui.py \n./view/zoom_gui.py \n./view/photobooth_gui.py \n./.git \n./main.py \n./data \n``` \nHere are the py files:"}]
    
    for path, content in file_dict.items():
        msgs.append({'role': 'user', 'content': f"```{path}\n{content}\n```"})
    
    msgs += history

    # Call your get_response function here with the necessary parameters
    answer, tokens = get_response('developer', msgs, model="gpt-4", temperature=0.33, max_tokens=800)
    
    return answer, tokens

