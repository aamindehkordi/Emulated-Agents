import openai

openai.api_key_path = "./key_openai.txt"

audio_file = open("audio.mp3", "rb")
transcript = openai.Audio.transcribe(
    file = audio_file,# The audio file to transcribe, in one of these formats: mp3, mp4, mpeg, mpga, m4a, wav, or webm.
    model = "whisper-1", # ID of the model to use. Only whisper-1 is currently available.
    prompt="", # An optional text to guide the model's style or continue a previous audio segment. The prompt should match the audio language.
    response_format="json", # json, text, srt, verbose_json, or vtt.
    temperature=0, #The sampling temperature, between 0 and 1. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. If set to 0, the model will use log probability to automatically increase the temperature until certain thresholds are hit.
    language="en", #The language of the input audio. Supplying the input language in ISO-639-1 format will improve accuracy and latency.
    )
