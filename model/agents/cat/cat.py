from model.openai_api import get_response

def get_response_cat(history):
  msgs=[
  #{'role':'user', 'content':'Ok let\'s move on'},
  *history
  ]
  
  answer, tokens = get_response(user='cat', history=msgs)
  
  return  answer, tokens