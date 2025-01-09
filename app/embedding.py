from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from bson import ObjectId
from pymongo.collection import Collection
from datetime import datetime
from embedding_utils.embedding_utils import generate_embedding, get_valid_embedding_models
from mongo_db import mongo_db

router = APIRouter()
documents_collection: Collection = mongo_db.get_document_collection()

@router.post("/process_embedding")
async def process_embedding(
    model_name: str = Query(..., description=f"embedding model name. Must be chosen from the available models: {', '.join(get_valid_embedding_models())}."),
    document_id: Optional[str] = Query(None, description="The ID of the document to process.")
):
    valid_models = get_valid_embedding_models()
    
    # Validate model_name
    if model_name not in valid_models:
        raise HTTPException(status_code=400, detail=f"Invalid model_name. Valid options are: {', '.join(valid_models)}")
    
    # Helper function to process a single document
    def process_document(doc):
        if model_name not in doc["embeddings"]:
            embedding = generate_embedding(doc["text"], model_name)
            doc["embeddings"][model_name] = embedding.tolist()
            doc["updated_at"] = datetime.utcnow()
            documents_collection.update_one({"_id": doc["_id"]}, {"$set": doc})
    
    # If document_id is provided
    if document_id:
        if not ObjectId.is_valid(document_id):
            raise HTTPException(status_code=400, detail="Invalid document_id format.")
        document = documents_collection.find_one({"_id": ObjectId(document_id)})
        if not document:
            raise HTTPException(status_code=404, detail="Document not found.")
        process_document(document)
        return {"message": f"Embedding for document {document_id} updated successfully."}
    
    # If document_id is not provided, process all documents
    documents = documents_collection.find()
    for document in documents:
        process_document(document)
    
    return {"message": "Embeddings updated for all applicable documents."}
