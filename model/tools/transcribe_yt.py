import os
import sys
import whisper
from pytube import YouTube

def download_audio_from_youtube(url):
    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=True).first()
    fn = "temp.wav"
    stream.download(filename=fn, output_path=".", skip_existing=False)
    return fn

def transcribe_audio(file_path):
    model = whisper.load_model("medium")
    audio = whisper.load_audio(file_path)
    result = model.transcribe(audio)
    return result["text"]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python youtube_transcript.py <youtube_url>")
        sys.exit(1)

    youtube_url = sys.argv[1]  
    try:                          
        audio_file = download_audio_from_youtube(youtube_url)
        transcript = transcribe_audio(audio_file)
        os.remove(audio_file)   
    except Exception as e:
        print(e)
        try:
            transcript = transcribe_audio(youtube_url)
        except Exception as el:
            print("L bozo")
            transcript = "Error: Could not transcribe audio."
    print("Transcript:")
    print(transcript)
