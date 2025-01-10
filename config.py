# config.py
from dotenv import load_dotenv
import os
import json

# Load the environment variables from .env
load_dotenv()

OPENAIKEY = os.getenv("OPENAIKEY")

# MongoDB Configuration
MONGO_USERNAME = os.getenv("MONGO_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
MONGO_QUERY_CL = os.getenv("MONGO_QUERY_CL")
MONGO_DOC_CL = os.getenv("MONGO_DOC_CL")

# MongoDB Connection URI
MONGO_URI = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}"



# Load and parse the EMBEDDING_MODELS_DICT
embedding_models_dict = json.loads(os.getenv('EMBEDDING_MODELS_DICT', '{}'))
