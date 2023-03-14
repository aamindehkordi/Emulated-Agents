import openai

openai.api_key_path = "./key_openai.txt"
#print(response["choices"][1]["message"]["content"])
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
  with open(f"api/agents/{user}_prompt.txt", encoding='utf-8') as f:
    agentPrompt = f.read()
  
  #Read general knowledge from file
  with open("api/agents/general_knowledge.txt", encoding='utf-8') as f:
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
  n=3, #How many chat completion choices to generate for each input_msg message.
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
    
    
    
    

def get_response_nathan(history):
    
  msgs=[
  {'role':'assistant', 'content': 'Nathan: Got it, I\'m Nathan Maldonado'},
  {'role':'user', 'content':'Jake: I have the mental discipline to not chase bitches.'},
  {'role':'assistant', 'content':'Nathan: Mental discipline? Mental discipline of who? A fat ninja with a donut? Don\'t talk to me about mental discipline.'},
  {'role':'user', 'content':'Thoughts on latina girls dating white dudes?'},
  {'role':'assistant', 'content':'Nathan: Every time I see a Latina gym baddie with a plain white dude it takes 2 weeks off my life.'},
  {'role':'user', 'content':'Thoughts on Mbappe in the world cup?'},
  {'role':'assistant', 'content':'Nathan: fuck that rat and his fuckin mom and that fuckin ninja turtle mbapenis. yeah bro we on that loud pack bro. louder than buenos aires right now bro. fuck Paris, fuck the Maginot line. messi stuck his fat girthy argecock straight down their mouthes. fuck ya mom you baguette eating, cigarette smoking, copium smoking, big nose having muthafuckers'},
  {'role':'user', 'content':'how did you finish the computer science homework so quick?'},
  {'role':'assistant', 'content':'Nathan: Lets just say I made a deal with the code devil (kyle)'},
  {'role':'user', 'content':'Thoughts on the Henry Cavill and Sophia Vergara'},
  {'role':'assistant', 'content':'Nathan: Henry Cavill is a giga chad, and bro, Sophia Vergara is one of the most OP women of all time.'},
  {'role':'user', 'content':'I heard that UCI kid talking shit about you'},
  {'role':'assistant', 'content':'Nathan: You talking about that twink ramen boy? imma punk his ass.'},
  {'role':'user', 'content':'I just ate an oyster'},
  {'role':'assistant', 'content':'Nathan: Who eats oysters theyre like the little cum dumpsters of the sea'},
  #{'role':'user', 'content':'Ok let\'s move on'},
  *history
  ]
  
  answer = get_response('nathan', msgs)
  
  return  answer

def get_response_kate(history):
    
  msgs=[
  #{'role':'user', 'content':'Ok let\'s move on'},
  *history
  ]
  
  answer = get_response('kate', msgs)
  
  return  answer

def get_response_cat(history):
  msgs=[
  #{'role':'user', 'content':'Ok let\'s move on'},
  *history
  ]
  
  answer = get_response('cat', msgs)
  
  return  answer

def get_response_robby(history):
  msgs=[
  #{'role':'user', 'content':'Ok let\'s move on'},
  *history
  ]
  
  answer = get_response('robby', msgs)
  
  return  answer

def get_response_ali(history):
  msgs=[
  #{'role':'user', 'content':'Ok let\'s move on'},
  *history
  ]
  
  answer = get_response('ali', msgs)
  
  return  answer

def get_response_jett(history):
  msgs=[
  #{'role':'user', 'content':'Ok let\'s move on'},
  *history
  ]
  
  answer = get_response('jett', msgs)
  
  return  answer

def get_response_all(history):
  """
    Get Responses from all agents and formats them into a chat history list
    
    *args:
    history: list of chat history
    
    *returns:
    updated history in this format {'role':'user', 'content':f"{user}: {message}"}
  """
  user_list = ['nathan', 'ali', 'jett', 'kate', 'robby', 'cat'] #add more users here
  responses = []
  #Get responses from all agents
  for user in user_list:
    response = get_response(user, history)
    responses.append({'role':'assistant', 'content':f"{user}: {response}"})
    
  history = [*history, *responses]
  
  return history
  