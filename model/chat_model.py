from model.base_model import BaseModel as Base

class ChatModel(Base):

    def __init__(self):
        super().__init__()
        self.mode = 0

    def get_chat_response(self, agent, history):
        """
        Format the query to get the best response from the agent.

        *args:
            agent: Agent object
            history: list of dictionaries containing the chat history

        *returns:
            response: string containing the response from the agent
        """

        # Get the agent's priming and history
        chat_history_list = [{'role': 'system', 'content': agent.general}]
        chat_history_list+= agent.get_priming() + history
        agent.set_msgs(chat_history_list)

        # Get the name of the user of the query
        user_name = chat_history_list[-1]['content'][0:chat_history_list[-1]['content'].find(':')]

        # Generate the response from the agent
        output, tokens = self.generate(agent, user=str(user_name), model=agent.model)
        print(output)
        print(agent.msgs)

        # Return the response
        return output

