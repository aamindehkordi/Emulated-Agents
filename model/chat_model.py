"""
./model/chat_model.py
"""
from model.base_model import BaseModel
import yaml

class ChatModel(BaseModel):

    def __init__(self):
        super().__init__()
        self.mode = 0
        self.chat_history_list = []

        self.path = f"./model/agents"
        with open(f"{self.path}/general.yaml", 'r') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            #self.personal = data["personal"]
            self.relationships = data["Relationships"]
            self.activities = data["Activities"]
            #self.expressions = data["expressions"]
            self.locations = data["Locations"]
            self.general = f"Useful information:\nRelationships: {self.relationships}\nActivities: {self.activities}\nLocations: {self.locations}\n\n"

    def get_chat_response(self, agent, history, user_name):
        """
        Format the query to get the best response from the agent.

        *args:
            agent: Agent object
            history: list of dictionaries containing the chat history

        *returns:
            response: string containing the response from the agent
        """

        # Get the agent's priming and history
        chat_history_list = [{'role': 'system', 'content': self.general}]
        chat_history_list+= agent.get_priming() + history
        agent.set_msgs(chat_history_list)

        # Generate the response from the agent
        output, tokens = self.generate(prompt=agent.msgs, user=str(user_name), model=agent.model, agent=agent)
        print(output)

        # Return the response
        return output

