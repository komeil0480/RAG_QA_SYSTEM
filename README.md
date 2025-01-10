# Simple RAG (Retrieval-Augmented Generation) API

This is a simple RAG API project designed for document management, query handling, and retrieval-augmented generation. It uses Docker for easy deployment and supports customizable embedding models.

---

## Features

- **Document Management**: Upload, retrieve, delete, and manage documents via API.
- **Customizable Embedding Models**: Users can select their preferred embedding model by updating the `.env` file.
- **Seeders**:
  1. Populate the dataset with data collected from Wikipedia (without embedding).
  2. Add 10 simple sentences to the database with LaBSE embeddings.
- **Query API**: Uses Faiss for finding similar documents, adds them to the context, and generates prompts with OpenAI API integration.
- **Logging System**: Tracks all activities for better monitoring.

---

## Prerequisites

1. **Docker**: Ensure Docker and Docker Compose are installed.
2. **OpenAI API Key**: Required for the query API. Add the key to the `.env` file.

---

## Setup and Deployment

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name

OPENAI_API_KEY=your_openai_api_key
EMBEDDING_MODEL_LIST=LaBSE,other_model_name

docker-compose up
