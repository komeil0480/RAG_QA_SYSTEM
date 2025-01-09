# mongo_db.py
from pymongo import MongoClient
from config import MONGO_URI, MONGO_DB_NAME, MONGO_QUERY_CL, MONGO_DOC_CL

class MongoDB:
    def __init__(self):
        # Initialize the MongoDB client and connect to the database
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[MONGO_DB_NAME]
        self.queryCL = self.db[MONGO_QUERY_CL]
        self.mongoDocCL = self.db[MONGO_DOC_CL]
        print(f"Connected to MongoDB database: {MONGO_DB_NAME}")

    def get_db(self):
        # Return the connected database instance
        return self.db
    def get_query_collection(self):
        # Return the connected database instance
        return self.queryCL
    def get_document_collection(self):
        # Return the connected database instance
        return self.mongoDocCL

# Initialize the MongoDB connection when the app starts
mongo_db = MongoDB()
