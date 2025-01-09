# embedding_utils.py

from sentence_transformers import SentenceTransformer
from fastapi import HTTPException
from config import embedding_models_dict 

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
