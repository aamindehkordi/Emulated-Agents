import os
import sys
import whisper
from pytube import YouTube

class YoutubeTranscript:
    @staticmethod
    def download_audio_from_youtube(url):
        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()
        fn = yt.title + ".wav"
        stream.download(filename=fn, output_path=".", skip_existing=False)
        return fn

    @staticmethod
    def transcribe_audio(file_path, write=False):
        model = whisper.load_model("medium")
        audio = whisper.load_audio(file_path)
        result = model.transcribe(audio)
        
        if write:
            #Save the transcript to a file with the same name as the audio file
            fn = file_path.split(".")[0] + ".txt"
            with open(fn, "w") as f:
                f.write(result["text"])
        return result["text"]
    
if __name__ == "__main__":
    lx = YoutubeTranscript()
    if len(sys.argv) < 2:
        print("Usage: python youtube_transcript.py <youtube_url or file_path>")
        sys.exit(1)

    youtube_url = sys.argv[1]  
    try:                          
        audio_file = lx.download_audio_from_youtube(youtube_url)
        transcript = lx.transcribe_audio(audio_file, True)
    except Exception as e:
        print(e)
        try:
            transcript = lx.transcribe_audio(youtube_url, True)
        except Exception as el:
            print("L bozo")
            transcript = "Error: Could not transcribe audio."
    print("Transcript:")
    print(transcript)
