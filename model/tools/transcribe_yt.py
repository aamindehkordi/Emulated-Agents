import os
import sys
import whisper
from pytube import YouTube

def download_audio_from_youtube(url):
    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=True).first()
    stream.download(filename="temp_audio.wav", output_path=".", skip_existing=False)
    return "temp_audio.wav"

def transcribe_audio(file_path):
    model = whisper.load_model("large")
    audio = whisper.load_audio(file_path)
    result = model.transcribe(audio)
    return result["text"]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python youtube_transcript.py <youtube_url>")
        sys.exit(1)

    youtube_url = sys.argv[1]                            
    audio_file = download_audio_from_youtube(youtube_url)
    transcript = transcribe_audio(audio_file)
    print("Transcript:")
    print(transcript)

    os.remove(audio_file)