"""
This module provides the get_response_cat+ function for the cat+ agent.

Functions in this module include:
- get_response_cat+(chat_history): returns the generated response from the cat+ agent based on the chat history
"""

from model.openai_api import get_response

def get_response_cat(history):
  msgs=[
  #{'role':'user', 'content':'Ok let\'s move on'},
  *history
  ]
  
  answer, tokens = get_response(user='cat', history=msgs)
  
  return  answer, tokens