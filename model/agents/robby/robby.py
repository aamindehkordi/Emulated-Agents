"""
This module provides the get_response_robby+ function for the robby+ agent.

Functions in this module include:
- get_response_robby+(chat_history): returns the generated response from the robby+ agent based on the chat history
"""

from model.openai_api import get_response

def get_response_robby(history):
  msgs=[
  #{'role':'user', 'content':'Ok let\'s move on'},
  *history
  ]
  
  answer, tokens = get_response('robby', msgs)
  
  return  answer, tokens

