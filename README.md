# Senior Project

This senior project aims to create an interactive AI chatroom with three distinct modes, simulating a conversation with an AI version of friends in a group. The project includes a text-based chat GUI, a zoom call simulation, and a photobooth-style live webcam conversation.

## Modes

1. **Text-based Chat GUI**: In this mode, users can type a message and receive a response from an AI version of someone in the friend group. The system should be able to semantically understand/guess who should respond. Users can also toggle a continuous conversation mode where the AI friends keep responding to each other until the stop button is pressed.

2. **Zoom Call Simulation**: In this mode, a looping short video of all AI friends is displayed in a layout resembling a Zoom call. Each AI friend has its own voice synthesis and lip filter, making it look like they are talking while they speak. The AI friends can engage in a continuous conversation with each other.

3. **Photobooth-style Live Webcam**: In this mode, a live webcam detects the user in front of the computer and selects their AI and voice synthesis. The user speaks, and the AI version of themselves talks back to them through their mirrored webcam feed.

## Project Structure

The project follows the Model-View-Controller (MVC) architecture:

- `./controller`: Contains the controller classes for each mode and a common controller.
- `./model`: Contains the model components, including chat, user selection, continuous conversation, voice synthesis, lip sync, and user recognition.
- `./view`: Contains the GUI classes for each mode and a common GUI class.

## Next Steps

1. Implement the user selection and continuous conversation functionality in the text-based chat GUI.
2. Plan and implement speech synthesis for each AI friend.
3. Develop the zoom call simulation and photobooth-style live webcam modes, incorporating voice synthesis and lip sync.
4. Implement user recognition for the photobooth-style live webcam mode.

## Future Enhancements

As the project progresses, new features and enhancements may be considered, such as improving the AI friends' conversational abilities, refining the user experience, and incorporating additional modes or functionalities.

## How to Run

1. Clone the repository to your local machine.
2. Install the required packages by running `pip install -r requirements.txt`.
3. Run `python main.py` to start the application.
