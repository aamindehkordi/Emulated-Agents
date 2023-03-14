import openai

openai.api_key_path = "./key_openai.txt"
#print(response["choices"][0]["message"]["content"])

def get_response_nathan(history):
  #Read Agent Prompt from file
  with open("api/agents/nathan_prompt.txt", "r") as f:
    agentPrompt = f.read()

  with open("api/agents/general_knowledge.txt", "r") as f:
    general = f.read()
    
  msgs=[
  #{'role':'system', 'content': agentPrompt},
  #{'role':'system', 'content': general},
  {'role':'user', 'content': f'{agentPrompt}\n{general}'},
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
  
  answer = response["choices"][0]["message"]["content"] # type: ignore
  
  #Failsafe
  """
  if "language model" in answer or "OpenAI" in answer or "I was created" in answer:
    answer = "Really bro. That's what you want to talk about? Talk about something else."
  """
  return  answer


def get_response_robby(history):
  #Read Agent Prompt from file
  with open("api/agents/robby_prompt.txt", "r") as f:
    agentPrompt = f.read()

  with open("api/agents/general_knowledge.txt", "r") as f:
    general = f.read()
    
  msgs=[
  #{'role':'system', 'content': agentPrompt},
  #{'role':'system', 'content': general},
  {'role':'user', 'content': f'{agentPrompt}\n{general}'},
  #{'role':'user', 'content':'Ok let\'s move on'},
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
  
  answer = response#["choices"][0]["message"]["content"] # type: ignore
  
  #Failsafe
  """
  if "language model" in answer or "OpenAI" in answer or "I was created" in answer:
    answer = "Really bro. That's what you want to talk about? Talk about something else."
  """
  return  answer

def get_response_ali(history):
  #Read Agent Prompt from file
  with open("api/agents/ali_prompt.txt", "r") as f:
    agentPrompt = f.read()

  with open("api/agents/general_knowledge.txt", "r") as f:
    general = f.read()
    
  msgs=[
  #{'role':'system', 'content': agentPrompt},
  #{'role':'system', 'content': general},
  {'role':'user', 'content': f'{agentPrompt}\n{general}'},
  #{'role':'user', 'content':'Ok let\'s move on'},
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
  
  answer = response#["choices"][0]["message"]["content"] # type: ignore
  
  #Failsafe
  """
  if "language model" in answer or "OpenAI" in answer or "I was created" in answer:
    answer = "Really bro. That's what you want to talk about? Talk about something else."
  """
  return  answer

def get_response_jett(history):
  #Read Agent Prompt from file
  with open("api/agents/jett_prompt.txt", "r") as f:
    agentPrompt = f.read()

  with open("api/agents/general_knowledge.txt", "r") as f:
    general = f.read()
    
  msgs=[
  #{'role':'system', 'content': agentPrompt},
  #{'role':'system', 'content': general},
  {'role':'user', 'content': f'{agentPrompt}\n{general}'},
  #{'role':'user', 'content':'Ok let\'s move on'},
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
  
  answer = response#["choices"][0]["message"]["content"] # type: ignore
  
  #Failsafe
  """
  if "language model" in answer or "OpenAI" in answer or "I was created" in answer:
    answer = "Really bro. That's what you want to talk about? Talk about something else."
  """
  return  answer