#!/bin/bash

# List of agent names
agents=("ali" "jett" "nathan" "kate" "robby" "cat")

# Path to the chat.py file
chat_py_path="./model/chat.py"

# Create the agents directory if it doesn't exist
mkdir -p ./model/agents

for agent in "${agents[@]}"; do
    # Create a new agent file
    agent_file="./model/agents/${agent}.py"
    touch "${agent_file}"
    
    # Move the corresponding get_response_* function from chat.py to the new agent file
    sed -n "/^def get_response_${agent}(/,/^$/p" "${chat_py_path}" >> "${agent_file}"
    
    # Remove the get_response_* function from chat.py
    sed -i.bak "/^def get_response_${agent}(/,/^$/d" "${chat_py_path}"
done

# Remove the backup file created by sed
rm "${chat_py_path}.bak"
