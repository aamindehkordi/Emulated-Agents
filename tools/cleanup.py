import csv
import re
from better_profanity import profanity
import pandas as pd

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
