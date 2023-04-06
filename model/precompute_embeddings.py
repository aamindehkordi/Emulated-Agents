import os
import json
from glob import glob
from model.tools.david import gpt3_embedding

nexus_path = "./model/history/nexus"
embeddings_path = "./model/history/embeddings.json"

embeddings = {}

for json_file in glob(os.path.join(nexus_path, "*.json")):
    with open(json_file, "r") as f:
        chunks = json.load(f)

    for chunk in chunks:
        uuid = chunk["id"]
        message = chunk["message"]
        embedding = gpt3_embedding(message)
        embeddings[uuid] = embedding

with open(embeddings_path, "w") as f:
    json.dump(embeddings, f)
