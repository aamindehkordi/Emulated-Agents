"""
This module provides the get_response_kate+ function for the kate+ agent.

Functions in this module include:
- get_response_kate+(chat_history): returns the generated response from the kate+ agent based on the chat history
"""

from model.openai_api import get_response

def get_response_kate(history):
    
  msgs=[
  #{'role':'user', 'content':'Ok let\'s move on'},
  *history
  ]
  
  answer, tokens = get_response('kate', msgs)
  
  return  answer, tokens

