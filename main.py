import cleanup, process, transcribe

def main():
    """
    Main function.
    """
    # Transcribe audio from 1-5.mp3
    for i in range(1, 6):
        filename = f"./data/videos/faded/{i}.mp3"
        print(f"Transcribing {filename}...")
        result = transcribe.transcribe(filename, "small")
        process.write_to_file(f"./data/processed/faded/{i}.json", result[text])
        print(f"Transcription result: {result}")
    
    # Extract messages
    #messages = cleanup.extract_messages("./data/preproccessed/discord_chat.csv")
    # Print messages
    #for username, text in messages:
    #    if cleanup.filter_profanity(text) and cleanup.filter_unnecessary_content(text):
    #        text = f"{username}: {text}\n"
    #        write_to_file("./data/processed/messages.txt", text)
        
if __name__ == "__main__":
    main()
