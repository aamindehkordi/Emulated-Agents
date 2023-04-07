import os
from glob import glob

import pinecone
import json

from model.tools.david import gpt3_embedding


class PineconeHandler:
    def __init__(self, api_key, environment, index_name):
        pinecone.init(api_key=api_key, environment=environment)
        self.index_name = index_name
        self.vdb = pinecone.Index(index_name=self.index_name)
        self.nexus_path = "./model/history/nexus"
        self.embeddings_path = "./model/history/embeddings.json"
        self.chunks = self.load_chunks()
        try:
            self.load_precomputed_embeddings()
        except Exception as e:
            print(e)
            self.precompute_embeddings()

    def is_pinecone_index_empty(self):
        try:
            # Try fetching the first item from the precomputed embeddings.
            with open(self.embeddings_path, "r") as f:
                embeddings = json.load(f)
            first_key = list(embeddings.keys())[0]
            self.fetch(ids=[first_key])
            return False
        except Exception as e:
            print(e)
            return True
    def precompute_embeddings(self):
        # check if embeddings.json exists
        if os.path.exists(self.embeddings_path):
            return

        embeddings = {}

        for json_file in glob(os.path.join(self.nexus_path, "*.json")):
            with open(json_file, "r") as f:
                chunks = json.load(f)

            for chunk in chunks:
                uuid = chunk["id"]
                message = chunk["message"]
                embedding = gpt3_embedding(message)
                embeddings[uuid] = embedding

        with open(self.embeddings_path, "w") as f:
            json.dump(embeddings, f)

    def load_precomputed_embeddings(self):
        with open('./model/history/embeddings.json', "r") as f:
            embeddings = json.load(f)

        chunk_size = 500
        for i in range(0, len(embeddings), chunk_size):
            chunk_data = [(uuid, embedding) for uuid, embedding in list(embeddings.items())[i:i + chunk_size]]
            self.upsert(chunk_data)

    def upsert(self, data):
        self.vdb.upsert(data)

    def query(self, queries, top_k):
        return self.vdb.query(queries=queries, top_k=top_k)

    def delete_index(self, ids=[]):
        self.vdb.delete(ids=ids)

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
            chunks = [json.load(open(entry.path, "r")) for entry in it if entry.name.endswith(".json")]
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
                    if msg is None:
                        # If the message is not found in the nexus, remove the vector from the database
                        self.remove_vector(id)
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

    def update_embeddings_file(self, message_id, vector):
        with open('./model/history/embeddings.json', "r") as f:
            embeddings = json.load(f)

        embeddings[message_id] = vector

        with open('./model/history/embeddings.json', "w") as f:
            json.dump(embeddings, f)

    def save_message(self, message, vector):
        # Save the message to the Pinecone index
        self.upsert([(message["id"], vector)])
        # Save the message to the nexus
        self.save_message_to_nexus(message)
        # Update the embeddings.json file
        self.update_embeddings_file(message["id"], vector)  # Assuming the vector is a numpy array, convert it to a list

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

