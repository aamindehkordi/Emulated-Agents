import whisper

model = whisper.load_model("medium")

# load audio and pad/trim it to fit 30 seconds
audio = whisper.load_audio("./data/videos/faded/1.mp3")
result = model.transcribe("./data/videos/faded/1.mp3")
# make log-Mel spectrogram and move to the same device as the model
#mel = whisper.log_mel_spectrogram(audio).to(model.device)

# detect the spoken language
#_, probs = model.detect_language(mel)
#print(f"Detected language: {max(probs, key=probs.get)}")

# decode the audio
#options = whisper.DecodingOptions(language="en", fp16=False)
#result1 = whisper.decode(model, mel, options)

# Save the result to a text file
print(result)
with open("result.txt", "w") as f:
    f.write(result[text])
    
# Print the result
#print(result1)