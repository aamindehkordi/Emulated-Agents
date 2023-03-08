import whisper

def transcribe(input_filename, model_size):
    model = whisper.load_model(model_size)
    result = model.transcribe(input_filename)
    return result
