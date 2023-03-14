import whisper

def transcribe_video(fn_in, model="medium", prompt="", language="en", fp16=False, temperature=0):
    """ Transcribes a video file and returns the transcript.
    *args:
        fn_in: Input filename of the video to transcribe.
        model_size: The size of the model to use. Options are "tiny, "small", "base", "medium", and "large".
        prompt: The prompt to use for the model.
        language: The language to use for the model.
        fp16: Whether or not to use fp16 for the model.
    *returns:
        The transcript of the video.
    """
    # Load the model
    model = whisper.load_model(model)

    # Load the audio
    audio = whisper.load_audio(fn_in)
    
    # Transcribe the audio
    result = model.transcribe(audio, prompt=prompt, language=language, fp16=fp16, temperature=temperature)
    
    # Return the result
    return result["text"]

"""
with open("api/agents/general_knowledge.txt", "r") as f:
    general = f.read()

#Test the function
transcript = transcribe_video("/Users/ali/Library/CloudStorage/OneDrive-Personal/Desktop/Other/Coding/School/Senior Project/data/preprocessed/all_updates/1.mov", prompt=str(general+"\n\n The following is a video update a friend group doing a road trip and talking about their experiences: \n"))
print(transcript)
"""