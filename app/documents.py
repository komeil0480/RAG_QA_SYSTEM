from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from datetime import datetime
import time
from bson import ObjectId
from mongo_db import mongo_db
from embedding_utils.embedding_utils import generate_embedding, get_valid_embedding_models
from typing import List, Optional
# Initialize router
router = APIRouter()

documents_collection = mongo_db.get_document_collection()  # Assuming you have a collection for documents
logs_collection = mongo_db.get_query_collection()

def is_valid_object_id(id: str) -> bool:
    return ObjectId.is_valid(id)

class Document(BaseModel):
    text: str
    embedding_models: list = []  
# API route to upload a document
@router.get("/documents")
async def get_all_documents():
    documents = list(documents_collection.find())
    for document in documents:
        document["_id"] = str(document["_id"])
        if document["embeddings"] is not None:
            document["embeddings"] = list(document["embeddings"].keys())
        # document["_id"] = str(document["_id"])  # Convert ObjectId to string
        # if "embedding" in document and isinstance(document["embedding"], object):
        #     document["embedding"] = list(document["embedding"].keys())
    return documents
@router.get("/documents/{id}", response_model=Optional[dict])
async def get_document_by_id(id: str):
    if not is_valid_object_id(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId format.")
    document = documents_collection.find_one({"_id": ObjectId(id)})
    if document:
        document["_id"] = str(document["_id"])  # Convert ObjectId to string
        return document
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found.")

@router.post("/upload_documents",
             description=f"List of embedding model names. Must be chosen from the available models: {', '.join(get_valid_embedding_models())}.")
async def upload_document(
    doc: Document,
):
    """
    Upload a document and optionally embed it with the provided embedding models.
    - Ensures that all models in `embedding_models` are unique and exist in the valid models list.
    """
    start_time = time.time()
    try:
        # Ensure all models in embedding_models are unique
        if len(doc.embedding_models) != len(set(doc.embedding_models)):
            raise HTTPException(
                status_code=400,
                detail="The embedding_models parameter contains duplicate values. Please ensure all models are unique."
            )

        # Validate that all models exist in the valid models list
        invalid_models = [model for model in doc.embedding_models if model not in get_valid_embedding_models()]
        if invalid_models:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid model(s): {', '.join(invalid_models)}. Valid models are: {', '.join(get_valid_embedding_models())}."
            )

        # Generate embeddings if embedding_models is provided
        embeddings = {}
        for model_name in doc.embedding_models:
            embedding = generate_embedding(doc.text, model_name)
            embeddings[model_name] = embedding.tolist()  # Convert numpy array to list

        # Prepare document data
        document_data = {
            "text": doc.text,
            "embeddings": embeddings if embeddings else {},
            "timestamp": datetime.utcnow(),
            "duration": time.time() - start_time,
        }

        # Insert the document into MongoDB
        documents_collection.insert_one(document_data)

        # Log the query
        log_entry = {
            "title": "upload_document",
            "doc": doc.text,
            "timestamp": datetime.utcnow(),
            "duration": time.time() - start_time,
        }
        logs_collection.insert_one(log_entry)

        return {"message": "Document indexed successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")

@router.delete("/documents/{id}", response_model=dict)
async def delete_document_by_id(id: str):
    if not is_valid_object_id(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ObjectId format.")
    result = documents_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 1:
        return {"message": "Document deleted successfully."}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found.")
