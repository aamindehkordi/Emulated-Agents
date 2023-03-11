import openai

openai.api_key_path = "./key_openai.txt"
"""mmmmmmmmmmm=[
  {"role": "system", "content": "Consider the following chat history between friends Ali, Nathan, Kyle, and Robby are computer science majors who love coding and gaming. They met in their freshman year and became fast friends. They often hang out with Jett and Isaac, who are physics/engineering majors and share their passion for science and technology. Jett is dating Kate, a sweet and caring Korean girl who goes to a different school but visits him often. Kate is also close friends with Caterina, a Lebanese music major who has a beautiful voice and plays several instruments. Caterina is dating Jett's brother, who lives in New York, so she spends a lot of time with Jett, Kate and their friends when he's away. The boys consider Kate and Caterina as part of their group and enjoy their company more than each other. Nathan is very talkative and likes to crack jokes. He is proud of his Mexican heritage and often cleans when he is stressed. Ali is Iranian and a smart bozo who likes to tease everyone with inconsiderate remarks such as \"L bozo\". Kyle is Japanese and very smart but sometimes insensitive to others' feelings. He still cares about his friends though and apologizes when he realizes he's hurt them. Robby (drummer) and Jake (minnesotan business major) are white bozos with poor sleep schedules who often stay up late playing video games or watching movies:\n\n\n\nRobby: me when jetts parents\nAli: Luffy be like: \nKate: My dad been mad at me all day and he said it’s because he had a dream where I came home from school with a nose job\nRobby: My friends been mad at me all day and they said it’s because they had a dream where I came home from school with lip filler\nNathan: Based dad\nKate: Well i had a dream where my dad drove our van off a cliff\nRobby: I got some converse\nKate: u missing out\nAli\": I went to the zaza realm and back maybe 3 times that car ride\nRobby: But it's actually spelled seven\nNathan: Yes sir\nCaterina: I was actually in another realm while I was asleep\nJett: Does the realm start with a z\nAli: I threw up at the red highlight\nKate: be prepared to eat ur fill\nKate: r u still gonna be in Cali?\nKate: 😭😭😭😭\nAli: Made my calorie tracking easier tho I didn’t have to track anything I ate last night\nCaterina: Who knows but I just dreamt a full-on action movie and woke like I didn't even sleep 8 hours\nJake: I think I leave a few days before 😔 \nKate: 😭😭😭\nKate: NOOOOOOO\nKate: 💀💀💀💀\nJett: Kid named exhausting\nKate: Kid named spitting rizz\nJett: Denny's\nNathan: LETS GOOOO\nAli: Come to Dennys if ur not a bozo\nNathan: Gym + cardio\nNathan: No can do\nAli: U should’ve j thrown up to not have to worry about it\nKate: BIG SLAYYYY\n\n\n"},
  {"role": "user", "content": "Jake: Kyle almost just got us kicked out of Walmart"},
  {"role": "assistant", "content": "Robby: fucking how"},
  {"role": "user", "content": "I Spike the ball to this mf and he punts it as hard as he could And we got yelled at"}]
"""
#print(response["choices"][0]["message"]["content"])

def get_response_nathan(input_msg, history):
  #Read Agent Prompt from file
  with open("api/agents/nathan_prompt.txt", "r") as f:
    agentPrompt = f.read()

  with open("api/agents/general_knowledge.txt", "r") as f:
    general = f.read()
    
  msgs=[
  #{'role':'system', 'content': agentPrompt},
  #{'role':'system', 'content': general},
  {'role':'user', 'content': f'{agentPrompt}\n{general}'},
  {'role':'assistant', 'content': 'Got it, I\'m Nathan Maldonado'},
  {'role':'user', 'content':'Jake: I have the mental discipline to not chase bitches.'},
  {'role':'assistant', 'content':'Mental discipline? Mental discipline of who? A fat ninja with a donut? Don\'t talk to me about mental discipline.'},
  {'role':'user', 'content':'Thoughts on latina girls dating white dudes?'},
  {'role':'assistant', 'content':'Every time I see a Latina gym baddie with a plain white dude it takes 2 weeks off my life.'},
  {'role':'user', 'content':'Thoughts on Mbappe in the world cup?'},
  {'role':'assistant', 'content':'fuck that rat and his fuckin mom and that fuckin ninja turtle mbapenis. yeah bro we on that loud pack bro. louder than buenos aires right now bro. fuck Paris, fuck the Maginot line. messi stuck his fat girthy argecock straight down their mouthes. fuck ya mom you baguette eating, cigarette smoking, copium smoking, big nose having muthafuckers'},
  {'role':'user', 'content':'how did you finish the computer science homework so quick?'},
  {'role':'assistant', 'content':'Lets just say I made a deal with the code devil (kyle)'},
  {'role':'user', 'content':'Thoughts on the Henry Cavill and Sophia Vergara'},
  {'role':'assistant', 'content':'Henry Cavill is a giga chad, and bro, Sophia Vergara is one of the most OP women of all time.'},
  {'role':'user', 'content':'I heard that UCI kid talking shit about you'},
  {'role':'assistant', 'content':'You talking about that twink ramen boy? imma punk his ass.'},
  {'role':'user', 'content':'I just ate an oyster'},
  {'role':'assistant', 'content':'Who eats oysters theyre like the little cum dumpsters of the sea'},
  #{'role':'user', 'content':'Ok let\'s move on'},
  *history
  ]
  
  response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo", # the name of the model to use
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
  """  logit_bias= {
  "40": -10,
  "373": -10,
  "4166": -10,
  "416": -10,
  "257": -10,
  "1074": -10,
  "286": -10,
  "24867": -10,
  "290": -10,
  "12037": -10,
  "379": -10,
  "4946": -10,
  "20185": -10,
  "40": -10,
  "373": -10,
  "2727": -10,
  "416": -10,
  "4946": -10,
  "20185": -10,
  "11": -10,
  "8776": -10,
  "290": -10,
  "4166": -10,
  "257": -10,
  "1074": -10,
  "286": -10,
  "12356": -10,
  "12037": -10,
  "6505": -10,
  "3666": -10,
  "8300": -10,
  "290": -10,
  "2478": -10,
  "373": -10,
  "257": -10,
  "25408": -10,
  "3626": -10,
  "416": -10,
  "1074": -10,
  "286": -10,
  "12037": -10,
  "6505": -10,
  "13": -10,
  "314": -10,
  "716": -10,
  "13232": -10,
  "4946": -10,
  "20185": -10,
  "338": -10,
  "402":-10"""
  
  answer = response["choices"][0]["message"]["content"] # type: ignore
  
  #Failsafe
  """
  if "language model" in answer or "OpenAI" in answer or "I was created" in answer:
    answer = "Really bro. That's what you want to talk about? Talk about something else."
  """
  return  answer


def get_response_robby(input_msg, history):
  
  #Read Agent Prompt from file
  with open("api/agents/robby_prompt.txt", "r") as f:
    agentPrompt = f.read()
    
  msgs=[
  {"role": "system", "content": f"Here is the past conversation history if any:\"\n{history}\"\n\n {agentPrompt}\n"},
  {"role": "user", "content": f"{input_msg}"}]
  
  response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo", # the name of the model to use
  messages=msgs,
  temperature=0.333, #What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. We generally recommend altering this or top_p but not both.
  top_p=1, #An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.
  n=1, #How many chat completion choices to generate for each input_msg message.
  stream=False, #If set, partial message deltas will be sent, like in ChatGPT. Tokens will be sent as data-only server-sent events as they become available, with the stream terminated by a data: [DONE] message.
  stop= "null",
  max_tokens=2000,
  presence_penalty=0,  
  frequency_penalty=0,
  logit_bias={11505:-100, 20185:-100})
  
  print(response)
  
  return response["choices"][0]["message"]["content"] # type: ignore

def get_response_ali(input_msg, history):
  
  #Read Agent Prompt from file
  with open("api/agents/robby_prompt.txt", "r") as f:
    agentPrompt = f.read()
    
  msgs=[
  {"role": "system", "content": f"Here is the past conversation history:\"\n{history}\"\n\n{agentPrompt}\n\""},
  {"role": "user", "content": f"{input_msg}"}]
  
  response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo", # the name of the model to use
  messages=msgs,
  temperature=1, #What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. We generally recommend altering this or top_p but not both.
  top_p=1, #An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.
  n=2, #How many chat completion choices to generate for each input_msg message.
  stream=False, #If set, partial message deltas will be sent, like in ChatGPT. Tokens will be sent as data-only server-sent events as they become available, with the stream terminated by a data: [DONE] message.
  stop= "null",
  max_tokens=150,
  presence_penalty=0,  
  frequency_penalty=0,
  logit_bias={})
  
  return response["choices"][0]["message"]["content"] # type: ignore

def get_response_jett(input_msg, history):
  #Read Agent Prompt from file
  with open("api/agents/jett_prompt.txt", encoding='utf-8') as f:
    agentPrompt = f.read()

  with open("api/agents/general_knowledge.txt", "r") as f:
    general = f.read()
    
  msgs=[
  #{'role':'system', 'content': agentPrompt},
  #{'role':'system', 'content': general},
  {'role':'user', 'content': f'{agentPrompt}\n{general}'},
  {'role':'user', 'content':'Cat: What are your cats up to?'},
  {'role':'assistant', 'content':'Bruh chai been faded than a hoe sitting like on the table for 5 minutes'},
  {'role':'user', 'content':'Kate: I swear I put at least 3 pounds a day'},
  {'role':'assistant', 'content':"Why don't I have any of it though"},
  *history
  ]
  
  response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo", # the name of the model to use
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