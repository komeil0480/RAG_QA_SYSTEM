from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from mongo_db import mongo_db

# Initialize router
router = APIRouter()
logs_collection = mongo_db.get_query_collection()

@router.get("/")
def fetch_logs(limit: int = 10):
    """
    Fetch query logs from MongoDB.
    :param limit: Number of logs to retrieve.
    """
    try:
        logs = list(logs_collection.find().sort("timestamp", -1).limit(limit))
        for log in logs:
            log["_id"] = str(log["_id"])  # Convert ObjectId to string
        return {"logs": logs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")
