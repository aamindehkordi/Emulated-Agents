"""
./model/tools/process.py
"""
import csv
import json
import os
import re
from uuid import uuid4

from better_profanity import profanity

from model.base_model import BaseModel as Base


def read_file_lines(filename):
    """
    Opens the given file and returns the contents.
    """
    with open(filename, "r") as f:
        return f.readlines()


def write_to_file(filename, text):
    """
    Writes the given text to the given file.
    """
    with open(filename, "w") as f:
        f.write(text)


def create_jsonl_file(filename, messages):
    """
    Creates a JSONL file from the given list of messages.
    """
    with open(filename, "w") as f:
        for message in messages:
            f.write(json.dumps(message) + "\n")

def is_link(message: str) -> bool:
    url_pattern = re.compile(
        r'((http|ftp|https)://[-\w@:%.+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_+.~#?&/=]*))|'  # General URLs
        r'(www\.[^\s]+)|'  # www links
        r'(\S+cdn\.discordapp\.com\S+)'  # Discord CDN links
    )
    return bool(url_pattern.search(message))


def csv_to_local_nexus_chunks_filtered(csv_file: str, output_directory: str, chunk_size: int) -> None:
    """Convert a CSV file of Discord chat logs to a local nexus with filtered message chunks.

    Args:
        csv_file (str): The input CSV file containing Discord chat logs.
        output_directory (str): The output directory where the JSON files will be saved.
        chunk_size (int): The number of messages stored in each JSON file.
    """
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    profanity.load_censor_words()

    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
        total_messages = len(rows)
        print(f'Total rows: {total_messages}')

        chat_history = []
        for idx, row in enumerate(rows):
            print(f'Row content: {row}')
            # Validate the message and skip if it's not valid
            message = row['Message'].strip()
            if not message or is_link(message) or profanity.contains_profanity(message):
                continue

            # Store message metadata if the message is valid
            message_data = {
                'id': str(uuid4()),
                'timestamp': row['Date/Time'],
                'user': row['Name'],
                'message': message
            }
            chat_history.append(message_data)
            print(f'Processed row {idx + 1}')

            # Save the chat history to a JSON file every `chunk_size` messages
            if (idx + 1) % chunk_size == 0 or idx == total_messages - 1:
                json_output = os.path.join(output_directory, f'chunk_{(idx + 1) // chunk_size}.json')
                print(f'Saving chunk to {json_output}')
                with open(json_output, 'w', encoding='utf-8') as jsonfile:
                    json.dump(chat_history, jsonfile, ensure_ascii=False, indent=4)
                chat_history = []


def main():
    # Example usage:
    csv_to_local_nexus_chunks_filtered('/Users/ali/Library/CloudStorage/OneDrive-Personal/Desktop/Other/Coding/' + \
                                       'School/Senior Project/model/history/backup.csv',
                                       '/Users/ali/Library/CloudStorage' + \
                                       '/OneDrive-Personal/Desktop/Other/Coding/School/Senior Project/model/history/nexus',
                                       9)


if __name__ == '__main__':
    main()
