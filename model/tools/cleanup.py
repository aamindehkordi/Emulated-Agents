"""
This module provides functions to clean up the chatbot's response.

Functions in this module include:
- cleanup_response(response): takes a raw chatbot response and returns a cleaned-up version
- compress_mov_files(input_dir, output_dir, video_codec='libx264', audio_codec='aac', crf=23, preset='fast', audio_bitrate='128k'): compresses all .mov files in the input directory using ffmpeg and saves them in the output directory
- extract_messages_csv(filename): extracts the messages from a .csv file and returns them as a list
- save_messages_csv(filename, messages): saves a list of messages to a .csv file
- filter_profanity(messages): filters out profanity from a list of messages
filter_unnecessary_content(message): filters out unnecessary content from a message
"""

import os
import re

import ffmpeg
import pandas as pd
from better_profanity import profanity


def compress_mov_files(input_dir, output_dir, video_codec='libx264', audio_codec='aac',
                       crf=23, preset='fast', audio_bitrate='128k'):
    """Compresses all .mov files in the input directory using ffmpeg and saves them in the output directory.

    Args:
        input_dir (str): The path to the directory containing the .mov files to compress.
        output_dir (str): The path to the directory where the compressed files will be saved.
        video_codec (str): The video codec to use for compression (default is 'libx264').
        audio_codec (str): The audio codec to use for compression (default is 'aac').
        crf (int): The Constant Rate Factor (CRF) to use for video compression (default is 23).
        preset (str): The compression preset to use (default is 'fast').
        audio_bitrate (str): The audio bitrate to use for compression (default is '128k').

    Returns:
        None
    """
    # Loop through the files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith('.mov'):
            input_file = os.path.join(input_dir, filename)
            output_file = os.path.join(output_dir, filename)
            (
                ffmpeg
                .input(input_file)
                .output(output_file, vcodec='libx264', crf=23)
                .run()
            )
    print('Finished compressing videos.')


def extract_messages_csv(filename):
    """
    Extracts messages and usernames from a discord history csv file, creating a separate file for each user and their messages.

    Args:
        filename: The filename of the csv file to extract messages from.

    Returns:
        An array of dataframes containing the messages for each username.
    """
    # Read csv file
    df = pd.read_csv(filename)

    # Get unique users
    users = df['Username'].unique()

    # Create a dataframe for each user
    user_dfs = []
    for user in users:
        user_df = df[df['Username'] == user]
        user_dfs.append(user_df)
    return user_dfs


def save_messages_csv(user_dfs):
    """
    Saves only the messages for each user into a separate file.
    
    Args:
        user_dfs: An array of dataframes containing the messages for each username.
    
    Returns:
        None
    """
    # Save each user's messages to a separate file
    messages = []
    for user in user_dfs:
        username = user['Username'].iloc[0]
        messages = user['Content'].tolist()
        # Save messages to file
        with open(f"./data/processed/{username}.txt", "w") as f:
            for message in messages:
                f.write(f"{message}\n")


def filter_profanity(message):
    return not profanity.contains_profanity(message)


def filter_unnecessary_content(message):
    # Check for URLs
    urls = re.findall(r'https?://\S+', message)
    if urls:
        return False

    # Check for image file extensions
    image_extensions = ['jpg', 'jpeg', 'png', 'gif']
    for extension in image_extensions:
        if message.endswith(extension):
            return False
    return True
