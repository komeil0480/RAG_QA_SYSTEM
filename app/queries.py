from fastapi import APIRouter, HTTPException, Query
from embedding_utils.embedding_utils import *
from mongo_db import mongo_db
from models.openAI import *
from bson import ObjectId
import time
from datetime import datetime
# Initialize router
router = APIRouter()

documents_collection = mongo_db.get_document_collection()
logs_collection = mongo_db.get_query_collection()
@router.get("/search")
async def search(
    query: str = Query(..., description=f"Enter your prompt."),
    embedding_model: str = Query(..., description=f"Embedding model name. Must be chosen from the available models: {', '.join(get_valid_embedding_models())}. --"
                                 "\t\t Note that only documents with the existing embedding type will be searched.")
):
    """
    Endpoint to handle search queries using a specified embedding model.

    Parameters:
    - query: The search query string.
    - embedding_model: The name of the embedding model to use.

    Returns:
    A placeholder response indicating that the parameters were received.
    """
    valid_models = get_valid_embedding_models()
    start_time = time.time()
    # Validate model_name
    if embedding_model not in valid_models:
        raise HTTPException(status_code=400, detail=f"Invalid model_name. Valid options are: {', '.join(valid_models)}")
    
    # Validate the input parameters
    if not query.strip():
        raise HTTPException(status_code=400, detail="Query parameter cannot be empty.")

    if not embedding_model.strip():
        raise HTTPException(status_code=400, detail="Embedding model parameter cannot be empty.")
    # # # Fetch documents with the specified embedding model in their embedding keys
    documents = list(documents_collection.find({f"embedding.{embedding_model}": {"$exists": True}}))
    embeddings, ids = load_documents_and_embeddings(documents)
    # Step 2: Create FAISS index
    faiss_index = create_faiss_index(embeddings)
    embedded_query = generate_embedding(query, embedding_model)
    
    # Step 4: Retrieve top documents
    results = retrieve_documents(faiss_index, embedded_query, ids, top_k=3)
    print("Retrieved Documents:", results)
    
    # Step 5: Combine context for OpenAI
    context = "\n\n".join([f"{documents_collection.find_one({'_id':ObjectId(r['id'])})['text']}" for r in results])
    print("context:",context)
    # Step 6: Query OpenAI
    response = query_openai(query, context)
    print("Response:", response)
    # Log the query
    log_entry = {
        "title": "query_openai",
        "query": query,
        "context": context,
        "timestamp": datetime.utcnow(),
        "duration": time.time() - start_time,
    }
    logs_collection.insert_one(log_entry)
    return response