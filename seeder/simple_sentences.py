import pymongo
import json
from datetime import datetime
import time
import sys
import os
# Append the root directory to sys.path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_dir)
from mongo_db import mongo_db

documents_collection = mongo_db.get_document_collection() 
# Load the sentence embeddings from your JSON file
with open("sentence_embeddings.json", "r") as file:
    data = json.load(file)

# Start timing the insertion
start_time = time.time()

# Prepare document data
for sentence, embedding in zip(data["sentences"], data["embeddings"]):
    document_data = {
        "text": sentence,
        "embedding": {"LaBSE": embedding},
        "timestamp": datetime.utcnow(),
        "duration": time.time() - start_time,
    }
    
    # Insert the document into MongoDB
    result = documents_collection.insert_one(document_data)

    # Output the result for each sentence
    print(f"Data inserted for sentence '{sentence}' with ID: {result.inserted_id}")
