from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from datetime import datetime
# import time
# from models.hugging_face_model import HuggingFaceAPIModel
# from pymongo import MongoClient
# from app.documents import retrieval_pipeline  # Reuse Chroma pipeline
# from mongo_db import mongo_db

# # Initialize router
router = APIRouter()

# logs_collection = mongo_db.get_query_collection()

# # Initialize Hugging Face model
# huggingface_model = HuggingFaceAPIModel(
#     model_name="deepset/roberta-base-squad2",
#     api_token="your-huggingface-api-token"
# )

# class Query(BaseModel):
#     question: str
#     top_k: int = 3

# @router.post("/")
# def answer_query(query: Query):
#     """
#     Retrieve relevant documents and generate an answer to the query.
#     """
#     start_time = time.time()
#     try:
#         # Retrieve documents
#         retrieved_docs = retrieval_pipeline.retrieve(query.question, top_k=query.top_k)
#         context = " ".join([doc for doc, _ in retrieved_docs])

#         # Generate answer
#         input_text = f"Question: {query.question}\nContext: {context}"
#         response = huggingface_model.query(input_text)

#         # Log query
#         log_entry = {
#             "title": "answer_query",
#             "query": query.question,
#             "context": context,
#             "response": response,
#             "timestamp": datetime.utcnow(),
#             "duration": time.time() - start_time
#         }
#         logs_collection.insert_one(log_entry)

#         return {"answer": response}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error: {e}")
