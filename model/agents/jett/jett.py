from model.openai_api import get_response

def get_response_jett(history):
  msgs=[
  #{'role':'user', 'content':'Ok let\'s move on'},
  *history
  ]
  
  answer = get_response('jett', msgs)
  
  return  answer

