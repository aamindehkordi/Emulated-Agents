# Senior Project

The primary objective of this project is to develop a sophisticated, AI-powered chatbot capable of replicating the speech patterns of individuals with high accuracy. To achieve this, we aim to leverage existing AI technologies and integrate them with a user-friendly chat application for seamless digital conversations. The current version of our project has successfully implemented a graphical user interface (GUI) using TKinter and optimized the AI's response generation by effectively managing token usage from OpenAI's ChatGPT.
This project is a chatbot application built using the OpenAI GPT-3.5-turbo model. The project is structured using the Model-View-Controller (MVC) pattern to separate the concerns of the application and make it more modular and maintainable.

## Modes

1. **Text-based Chat GUI**: In this mode, users can type a message and receive a response from an AI version of someone in the friend group. The system should be able to semantically understand/guess who should respond. Users can also toggle a continuous conversation mode where the AI friends keep responding to each other until the stop button is pressed.

2. **Zoom Call Simulation**: In this mode, a looping short video of all AI friends is displayed in a layout resembling a Zoom call. Each AI friend has its own voice synthesis and lip filter, making it look like they are talking while they speak. The AI friends can engage in a continuous conversation with each other.

3. **Photobooth-style Live Webcam**: In this mode, a live webcam detects the user in front of the computer and selects their AI and voice synthesis. The user speaks, and the AI version of themselves talks back to them through their mirrored webcam feed.

## Project Structure

The project follows the Model-View-Controller (MVC) architecture:

### Model

The Model directory contains all the logic for the communication pattern emulation application.

- `agent.py`: Contains the Agent class, which represents an individual AI friend in the chat.
- `base_model.py`: Contains the base class for models.
- `chat_model.py`: Contains the model class for the chatbot application. It connects the chatbot model with the GUI view.
- `TBA`: More not yet developed for verbal communication pattern responses rather than text patterns
- `/Agents`: Contains agent-specific initialization yaml files.
- `/tools`: Contains helper functions for different aspects of the project.

### View

The View directory contains all the user interface components.

- `base_gui.py`: Contains the base class for the GUI.
- `discord_gui.py`: Contains the Discord-style GUI implementation.
- `zoom_gui.py`: Contains the Zoom-style GUI implementation. *unused/empty*
- `photobooth_gui.py`: Contains the Photobooth-style GUI implementation. *unused/empty*
- `TBA`

### Controller

The Controller directory contains the logic to connect the Model and the View.

- `base_controller.py`: Contains the base class for controllers.
- `chat_controller.py`: Contains the controller class for the chatbot application. It connects the chatbot model with the GUI view.
- `zoom_controller.py`: Contains the controller class for the Zoom GUI. *unused/empty*
- `photobooth_controller.py`: Contains the controller class for the Photobooth GUI. *unused/empty*
- `TBA`

### File Structure
```
.
./controller
./controller/chat_controller.py
./controller/zoom_controller.py
./controller/photobooth_controller.py
./controller/__pycache__
./controller/base_controller.py
./model
./model/tools
./model/tools/__pycache__
./model/tools/process.py
./model/Agents
./model/Agents/general.yaml
./model/Agents/robby.yaml
./model/Agents/dan.yaml
./model/Agents/jett.yaml
./model/Agents/nathan.yaml
./model/Agents/cat.yaml
./model/Agents/ali.yaml
./model/Agents/kate.yaml
./model/Agents/kyle.yaml
./model/__pycache__
./model/base_model.py
./model/agent.py
./model/chat_model.py
./view
./view/base_gui.py
./view/discord_gui.py
./view/__pycache__
./view/zoom_gui.py
./view/photobooth_gui.py
./README.md
./key_openai.txt
./.gitignore
./.git
./main.py
```

## Next Steps

- [ ] Timestamps - GUI/ Model
- [ ] Autoscroll - GUI
- [ ] Entry box expansion - GUI
- [ ] GUI appearance - GUI
- [ ] GUI functionality - GUI
- [ ] Chat bubbles - GUI
- [ ] Menu bar - GUI
- [ ] Preferences menus - GUI
- [ ] Themes - GUI
- [ ] Threading - GUI/MODEL/CONTROLLER
- [ ] Continuous Conversation - CONTROLLER
- [ ] Facetime - CONTROLLER/ GUI
- [ ] Zoom GUI - CONTROLLER/ GUI
- [ ] TTS - MODEL
- [ ] Live Webcam - CONTROLLER/ GUI
- [ ] Lip Filter - CONTROLLER/ GUI
- [ ] Prerecorded Zoom clips - CONTROLLER/ GUI
