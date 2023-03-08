import json

def read_file_lines(filename):
    """
    Opens the given file and returns the contents.
    """
    with open(filename, "r") as f:
        return f.readlines()
    
def write_to_file(filename, text):
    """
    Writes the given text to the given file.
    """
    with open(filename, "w") as f:
        f.write(text)
        
def create_jsonl_file(filename, messages):
    """
    Creates a JSONL file from the given list of messages.
    """
    with open(filename, "w") as f:
        for message in messages:
            f.write(json.dumps(message) + "\n")
# Open the input file
#fn = "./data/preprocessed/messages.txt"
"""
# Loop over the lines and create a list of JSON objects
output = []
current_message = ''
for line in lines:
    line = line.strip()
    if not line:
        # Skip empty lines
        continue
    if ':' in line:
        # Start a new message
        if current_message:
            # Add the previous message to the output list
            output.append({'prompt': prompt + '\n\n###\n\n', 'completion': current_message.strip() + ' ###\n'})
            current_message = ''
        prompt, message = line.split(':', 1)
        current_message = message
    else:
        # Continue the current message
        current_message += ' ' + line

# Add the final message to the output list
if current_message:
    output.append({'prompt': prompt + '\n\n###\n\n', 'completion': current_message.strip() + ' \n###\n'})

# Write the output to a JSONL file
with open('./data/processed/messages.jsonl', 'w') as f:
    for item in output:
        f.write(json.dumps(item) + '\n')
"""