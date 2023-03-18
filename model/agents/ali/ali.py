"""
This module provides the get_response_ali+ function for the ali+ agent.

Functions in this module include:
- get_response_ali+(chat_history): returns the generated response from the ali+ agent based on the chat history
"""

from model.openai_api import get_response


def get_response_ali(history):
  msgs=[
  #{'role':'user', 'content':'Ok let\'s move on'},
  *history
  ]
  
  answer, tokens = get_response('ali', msgs)
  
  return  answer, tokens

