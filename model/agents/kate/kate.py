from model.openai_api import get_response

def get_response_kate(history):
    
  msgs=[
  #{'role':'user', 'content':'Ok let\'s move on'},
  *history
  ]
  
  answer, tokens = get_response('kate', msgs)
  
  return  answer, tokens

