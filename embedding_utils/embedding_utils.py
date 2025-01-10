# embedding_utils.py

from sentence_transformers import SentenceTransformer
from fastapi import HTTPException
from config import embedding_models_dict 
import numpy as np
import faiss

# Dependency to fetch valid embedding model keys dynamically
def get_valid_embedding_models():
    return list(embedding_models_dict.keys())
# Function to generate embedding based on the model name
def generate_embedding(text: str, model_name: str):
    try:
        model = SentenceTransformer(embedding_models_dict.get(model_name))
        return model.encode(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating embedding: {e}")
def load_documents_and_embeddings(documents):
    """
    Returns a tuple of embeddings (numpy array) and document IDs.
    """
    embeddings = []
    ids = []
    for doc in documents:
        embeddings.append(np.array(doc["embedding"]["LaBSE"], dtype="float32"))  # Ensure it's a numpy array
        ids.append(str(doc["_id"]))  # Use _id as a unique identifier
    return np.array(embeddings), ids

def create_faiss_index(embeddings):
    """
    Create and return a FAISS index for the embeddings.
    """
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index
def retrieve_documents(index, query_embedding, ids, top_k=5):
    """
    Retrieve top K documents from the FAISS index.
    """
    distances, indices = index.search(query_embedding.reshape(1, -1), top_k)
    results = [{"id": ids[i], "distance": distances[0][idx]} for idx, i in enumerate(indices[0])]
    return results