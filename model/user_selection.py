from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def extract_embedding(text):
    embedding = model.encode([text])
    return embedding

def calculate_similarity(message, response):
    message_embedding = extract_embedding(message)
    response_embedding = extract_embedding(response)

    similarity = cosine_similarity(message_embedding, response_embedding)
    return similarity[0][0]

def predict_user(chat_history, user_list, responses):
    last_message = chat_history[-1]['content']
    similarities = [calculate_similarity(last_message, response) for response in responses]
    
    highest_similarity_index = np.argmax(similarities)
    selected_user = user_list[highest_similarity_index]
    
    return selected_user
