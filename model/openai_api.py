import openai
openai.api_key_path = "./key_openai.txt"

import whisper

#Not an api but makes more sense to put it here
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

def get_response(user, history):
  """
    Gets appropriate user chat response based off the chat history.
    
    *args:
    user: a string of the user's name
    history: chat history from this session
  
    *returns:
    response: a string containing the chat response
  """
  #Read Agent Prompt from file
  with open(f"model/agents/{user}/{user}_prompt.txt", encoding='utf-8') as f:
    agentPrompt = f.read()
  
  #Read general knowledge from file
  with open("model/agents/general_knowledge.txt", encoding='utf-8') as f:
    general = f.read()
    
  msgs = [
    {'role':'user', 'content': f'{agentPrompt}\n{general}'},
    *history
  ]
  
  response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo-0301", # the name of the model to use
  messages=msgs,
  temperature=1, #What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. We generally recommend altering this or top_p but not both.
  top_p=1, #An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.
  n=2, #How many chat completion choices to generate for each input_msg message.
  stream=False, #If set, partial message deltas will be sent, like in ChatGPT. Tokens will be sent as data-only server-sent events as they become available, with the stream terminated by a data: [DONE] message.
  stop= "null",
  max_tokens=200,
  presence_penalty=0,  
  frequency_penalty=0,
  )
  
  answer = response["choices"][1]["message"]["content"] # type: ignore
  
  #Failsafe
  """
  if "language model" in answer or "OpenAI" in answer or "I was created" in answer:
    answer = "Really bro. That's what you want to talk about? Talk about something else."
  """
  return  answer