"""
This module provides the get_response_jett+ function for the jett+ agent.

Functions in this module include:
- get_response_jett+(chat_history): returns the generated response from the jett+ agent based on the chat history
"""

from model.openai_api import get_response

def get_response_jett(history):
  msgs=[
  #{'role':'user', 'content':'Ok let\'s move on'},
  *history
  ]
  
  answer, tokens = get_response('jett', msgs)
  
  return  answer, tokens

