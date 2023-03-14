# Chatroom Application

This is a chatroom application that allows users to communicate with several bots. The bots generate responses based on the user's message and the conversation history, using an API to perform these tasks. The GUI provides a simple and intuitive way for users to interact with the application and visualize the conversation history.

## Overview

The goal of this project is to create AI chatbots that can interact with users in a way that mimics the communication styles of a group of friends. The chatbots will be trained on a fine-tuned GPT-3 model and will be able to generate responses that are similar to how the friends would actually respond.

## Data Collection

The data for the chatbots will be collected from a variety of sources, including:

- Chat logs from messaging apps
- Audio recordings of real-life conversations
- Text transcriptions of the audio recordings

The chat logs will be taken from a Discord server that the group of friends is already a part of. The audio recordings will be transcribed using automatic speech recognition tools such as Google Cloud Speech-to-Text or Amazon Transcribe or whisper.

## Data Preparation

Once the data has been collected, it will need to be cleaned and formatted for use in training the GPT-3 model. This will involve removing any personal information or irrelevant messages and standardizing the formatting of the text data. Tokenization and preprocessing will also be done using tools like NLTK or spaCy.

## Technologies Used

- Python
- tkinter
- OpenAI API

## Features

- Users can type a message and select a bot to respond.
- Bots generate responses based on the user's message and the conversation history.
- GUI displays conversation history between the user and selected bots.
- Loading animations when the API call is being made.
- User can send a message by pressing the Enter key.
- Aesthetically pleasing color scheme and layout.

## TODO

- Error checking to prevent user from sending empty messages.
- Implement feature to allow bots to communicate with each other.
- Improve error handling for API calls.
- Add option to save conversation history.

## How to Run

1. Clone the repository to your local machine.
2. Install the required packages by running `pip install -r requirements.txt`.
3. Run `python main.py` to start the application.
