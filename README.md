# Senior Project

This senior project aims to create an interactive AI chatroom with three distinct modes, simulating a conversation with an AI version of friends in a group. The project includes a text-based chat GUI, a zoom call simulation, and a photobooth-style live webcam conversation.

This project is a chatbot application built using the OpenAI GPT-3.5-turbo model. The project is structured using the Model-View-Controller (MVC) pattern to separate the concerns of the application and make it more modular and maintainable.

## Modes

1. **Text-based Chat GUI**: In this mode, users can type a message and receive a response from an AI version of someone in the friend group. The system should be able to semantically understand/guess who should respond. Users can also toggle a continuous conversation mode where the AI friends keep responding to each other until the stop button is pressed.

2. **Zoom Call Simulation**: In this mode, a looping short video of all AI friends is displayed in a layout resembling a Zoom call. Each AI friend has its own voice synthesis and lip filter, making it look like they are talking while they speak. The AI friends can engage in a continuous conversation with each other.

3. **Photobooth-style Live Webcam**: In this mode, a live webcam detects the user in front of the computer and selects their AI and voice synthesis. The user speaks, and the AI version of themselves talks back to them through their mirrored webcam feed.

## Project Structure

The project follows the Model-View-Controller (MVC) architecture:

### Model

The Model directory contains all the logic related to the chatbot and its interaction with the OpenAI API.

- `openai_api.py`: Handles the interaction with the OpenAI API.
- `agents`: Contains agent-specific logic and prompt files.
  - Each agent has its own subdirectory with a Python file (e.g., `ali.py`, `jett.py`) containing the agent's `get_response_*` function, and a text file (e.g., `ali_prompt.txt`, `jett_prompt.txt`) containing the agent's prompt.
  - `general_knowledge.txt`: Contains general knowledge information shared by all agents.

### View

The View directory contains all the user interface components.

- `base_gui.py`: Contains the base class for the GUI.
- `discord_gui.py`: Contains the Discord-style GUI implementation.
- `zoom_gui.py`: Contains the Zoom-style GUI implementation.
- `photobooth_gui.py`: Contains the Photobooth-style GUI implementation.

### Controller

The Controller directory contains the logic to connect the Model and the View.

- `base_controller.py`: Contains the base class for controllers.
- `chat_controller.py`: Contains the controller class for the chatbot application. It connects the chatbot model with the GUI view.
- `zoom_controller.py`: Contains the controller class for the Zoom GUI.
- `photobooth_controller.py`: Contains the controller class for the Photobooth GUI.

## Next Steps

1. Implement the user selection and continuous conversation functionality in the text-based chat GUI.
2. Plan and implement speech synthesis for each AI friend.
3. Develop the zoom call simulation and photobooth-style live webcam modes, incorporating voice synthesis and lip sync.
4. Implement user recognition for the photobooth-style live webcam mode.

## Future Enhancements

1. Implement context management when interacting with the OpenAI API to manage tokens and avoid exceeding API limits.
2. Implement a caching mechanism to store the chatbot's responses, reducing the number of calls to the OpenAI API and saving on costs.
3. Improve the conversation flow by creating a more structured dialog system using state machines or decision trees.
4. Handle different conversation contexts to allow the chatbot to switch between topics and provide more meaningful and engaging conversations.
5. Use pre-processing techniques like spelling correction and text normalization to improve chatbot performance.
6. Utilize a logging system to monitor the chatbot's performance and user interactions.

## How to Run

1. Clone the repository to your local machine.
2. Install the required packages by running `pip install -r requirements.txt`.
3. Run `python main.py` to start the application.
