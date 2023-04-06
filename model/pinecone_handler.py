import os

import pinecone
import json

class PineconeHandler:
    def __init__(self, api_key, environment, index_name):
        pinecone.init(api_key=api_key, environment=environment)
        self.index_name = index_name
        self.vdb = pinecone.Index(index_name=self.index_name)
        self.nexus_path = "./model/history/nexus"
        self.chunks = self.load_chunks()
        if self.is_pinecone_index_empty():
            self.load_precomputed_embeddings()

    def is_pinecone_index_empty(self):
        try:
            # Try fetching the first item from the precomputed embeddings.
            with open('./model/history/embeddings.json', "r") as f:
                embeddings = json.load(f)
            first_key = list(embeddings.keys())[0]
            self.fetch(ids=[first_key])
            return False
        except Exception as e:
            print(e)
            return True

    def load_precomputed_embeddings(self):
        #Check if embeddings.json exists
        if not os.path.exists('./model/history/embeddings.json'):
            return
        else:
            with open('./model/history/embeddings.json', "r") as f:
                embeddings = json.load(f)

            chunk_size = 250
            for i in range(0, len(embeddings), chunk_size):
                chunk_data = [(uuid, embedding) for uuid, embedding in list(embeddings.items())[i:i + chunk_size]]
                self.upsert(chunk_data)

    def upsert(self, data):
        self.vdb.upsert(data)

    def query(self, queries, top_k):
        return self.vdb.query(queries=queries, top_k=top_k)

    def delete_index(self):
        self.vdb.delete()

    def __del__(self):
        self.delete_index()
        pinecone.deinit()

    def fetch(self, ids):
        return self.vdb.fetch(ids=ids)

    def load_chunks(self):
        """
        Load all the chunks from the nexus directory into memory.
        """
        chunks = []
        with os.scandir(self.nexus_path) as it:
            for entry in it:
                if entry.name.endswith(".json"):
                    with open(entry.path, "r") as f:
                        chunk = json.load(f)
                        chunks.append(chunk)
        return chunks

    def get_message(self, vec_id):
        """
        Find and return a message with a specific ID.

        :param vec_id: The ID of the message to be found.
        :return: The message with the specified ID or None if not found.
        """
        for chunk in self.chunks:
            for msg in chunk:
                if msg["id"] == vec_id:
                    return msg
        return None

    def get_next_message(self, time_stamp, vec_id):
        """
        Find and return the next message after the message with the specified ID.

        :param time_stamp: The timestamp of the current message.
        :param vec_id: The ID of the current message.
        :return: The next message after the current message or None if not found.
        """
        last = False
        for chunk in self.chunks:
            for msg in chunk:
                if last:
                    return msg
                if msg["id"] == vec_id:
                    if chunk.index(msg) == len(chunk) - 1:
                        last = True
                        continue
                    else:
                        return chunk[chunk.index(msg) + 1]

        for chunk in self.chunks:
            if chunk[0]["timestamp"] > time_stamp:
                return chunk[0]
        return None


    def save_message(self, message, vector):
        # Save the message to the Pinecone index
        self.upsert([(message["id"], vector)])
        # Save the message to the nexus
        self.save_message_to_nexus(message)

    def save_message_to_nexus(self, message):
        # Get the timestamp of the message
        time_stamp = message["timestamp"]
        # Get the path to the chunk
        chunk_path = os.path.join(self.nexus_path, f"{time_stamp}.json")
        # Check if the chunk exists
        if os.path.exists(chunk_path):
            # If the chunk exists, load it
            with open(chunk_path, "r") as f:
                chunk = json.load(f)
        else:
            # If the chunk does not exist, create it
            chunk = []
        # Append the message to the chunk
        chunk.append(message)
        # Save the chunk
        with open(chunk_path, "w") as f:
            json.dump(chunk, f)

