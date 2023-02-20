import csv
import re
from better_profanity import profanity

def extract_messages(filename):
    """
    Extracts messages and usernames from a discord history csv file.

    Args:
        filename: The filename of the csv file to extract messages from.

    Returns:
        A list of tuples containing (username, message) pairs.
    """
    # Extract message data
    messages = []
    with open(filename, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            username = row["Username"]
            text = row["Content"]
            messages.append((username, text))
    return messages

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

def main():
    """
    Main function.
    """
    # Extract messages
    messages = extract_messages("./data/preproccessed/discord_chat.csv")
    # Print messages
    with open("messages.txt", "w") as f:
        for username, text in messages:
            if filter_profanity(text) and filter_unnecessary_content(text):
                f.write(f"{username}: {text}\n")
        
if __name__ == "__main__":
    main()
