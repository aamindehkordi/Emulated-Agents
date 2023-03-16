import json
import ffmpeg
import os
from model.openai_api import transcribe_video as whisper

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

def transcribe_updates(video_path, output_path):
    """
    Transcribes update videos from folder path and save transcripts to output path.
    """
    with open("api/agents/general_knowledge.txt", "r") as f:
        general = f.read()
    for filename in os.listdir(video_path):
        if filename.endswith('.mov'):
            transcript = whisper.transcribe_video(os.path.join(video_path, filename), model="large", prompt=str(general+"\n\n The following is a video update a friend group doing a road trip and talking about their experiences: \n"))
            write_to_file(os.path.join(output_path, filename[:-4] + ".txt"), transcript)
            
        print(f'Transcribed {filename}')
    print('Finished transcribing videos.')
    