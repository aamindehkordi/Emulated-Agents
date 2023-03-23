from time import sleep
import openai
import whisper
import os, json

openai.api_key_path = "./key_openai.txt"


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

def get_response(user, history, model="gpt-3.5-turbo", temperature=0.91, top_p=1, n=1, stream=False, stop= "null", max_tokens=350, presence_penalty=0, frequency_penalty=0, debug=False):
  """
    Gets appropriate user chat response based off the chat history.
    
    *args:
    user: a string of the user's name
    history: chat history from this session
    model: the name of the model to use
    temperature: What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. We generally recommend altering this or top_p but not both.
    top_p: An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.
    n: How many chat completion choices to generate for each input_msg message.
    stream: If set, partial message deltas will be sent, like in ChatGPT. Tokens will be sent as data-only server-sent events as they become available, with the stream terminated by a data: [DONE] message.
    stop: Up to 4 sequences where the API will stop generating further tokens.
    max_tokens: The maximum number of tokens to generate.
    presence_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics.
    frequency_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.
  
    *returns:
    response: a string containing the chat response
    token_count: an int containing the number of tokens used
  """
  if str(user) == "developer":
    debug = True
    print("debug mode")
  #Read Agent Prompt from file
  with open(f"model/agents/{user}/{user}_prompt.txt", encoding='utf-8') as f:
    agentPrompt = f.read()
  
  #Read general knowledge from file
  with open("model/agents/general_knowledge.txt", encoding='utf-8') as f:
    general = f.read()
    
  if not debug:
    msgs = [
      {'role':'system', 'content': f'{agentPrompt}\nGeneral information: \n{general}'},
      *history
    ]
  else:
    msgs = [
      {'role':'system', 'content': f'{agentPrompt}'},
      *history
    ]
  
  max_retry = 2
  retry = 0
  while True:
    try:
      response = openai.ChatCompletion.create(
      model=model, # the name of the model to use
      messages=msgs,
      temperature=temperature, #What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. We generally recommend altering this or top_p but not both.
      top_p=top_p, #An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.
      n=n, #How many chat completion choices to generate for each input_msg message.
      stream=stream, #If set, partial message deltas will be sent, like in ChatGPT. Tokens will be sent as data-only server-sent events as they become available, with the stream terminated by a data: [DONE] message.
      stop= stop,
      max_tokens=max_tokens,
      presence_penalty=presence_penalty,
      frequency_penalty=frequency_penalty,
      )
      
      answer = response["choices"][0]["message"]["content"] # type: ignore
      
      if model=="gpt-4":
        prompt_tokens = response['usage']['prompt_tokens'] # type: ignore
        completion_tokens = response['usage']['completion_tokens'] # type: ignore
        total_tokens = response['usage']['total_tokens'] # type: ignore
        tokens = (total_tokens, prompt_tokens, completion_tokens)
        print(f"token cost for last response: {prompt_tokens/1000*0.03 + completion_tokens/1000*0.06}")
        
      if model=="gpt-4-32k":
        prompt_tokens = response['usage']['prompt_tokens'] # type: ignore
        completion_tokens = response['usage']['completion_tokens'] # type: ignore
        total_tokens = response['usage']['total_tokens'] # type: ignore
        tokens = (total_tokens, prompt_tokens, completion_tokens)
        print(f"token cost for last response: {prompt_tokens/1000*0.06 + completion_tokens/1000*0.12}")
      
      else:
        tokens = (response['usage']['total_tokens'],) # type: ignore
        print(f"token cost for last response: {tokens[0]/1000*0.002}")
      
      if debug:
        #write response to history file ./model/agents/{user}/{user}_history.json
        with open(f"model/agents/{user}/{user}_history.json", "w") as f:
          json.dump(answer, f)
          #TODO add permanent history
          
      return answer, tokens
    
    except Exception as oops:
        if 'maximum context length' in str(oops):
            #TODO better solution
            msgs = msgs[1:]
            continue
        retry += 1
        if retry >= max_retry:
            print(f"Exiting due to an error in ChatGPT: {oops}")
            exit(1)
        print(f'Error communicating with OpenAI: {oops}. Retrying in {2 ** (retry - 1) * 5} seconds...')
        sleep(2 ** (retry - 1) * 5)