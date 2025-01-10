from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from openai import OpenAI
import logging
from config import embedding_models_dict, OPENAIKEY
from sentence_transformers import SentenceTransformer

router = APIRouter()

@router.get("/", response_class=JSONResponse)
async def health_check():
    embedding_model_1 = SentenceTransformer(embedding_models_dict["all-MiniLM-L6-v2"])
    embedding_model_2 = SentenceTransformer(embedding_models_dict["LaBSE"])
    health_status = {
        "status": "healthy",
        "api": "operational",
        "embedding_model_1": "unknown",
        "embedding_model_2": "unknown",
        "openai_api": "unknown"
    }

    # Check Embedding Model 1
    try:
        test_input = "test"
        embedding_model_1.encode(test_input)
        health_status["embedding_model_1"] = "operational"
    except Exception as e:
        logging.error(f"Embedding Model 1 error: {e}")
        health_status["embedding_model_1"] = "unavailable"

    # Check Embedding Model 2
    try:
        test_input = "test"
        embedding_model_2.encode(test_input)
        health_status["embedding_model_2"] = "operational"
    except Exception as e:
        logging.error(f"Embedding Model 2 error: {e}")
        health_status["embedding_model_2"] = "unavailable"

    # Check OpenAI API
    try:
        test_prompt = "Say hello"
        client = OpenAI(api_key=OPENAIKEY)
        response = client.completions.create(model="GPT-4o",  # Replace with your desired model
        prompt=test_prompt,
        max_tokens=300)
        if response and response.choices:
            health_status["openai_api"] = "operational"
        else:
            health_status["openai_api"] = "unavailable"
    except Exception as e:
        logging.error(f"OpenAI API error: {e}")
        health_status["openai_api"] = "unavailable"

    # Determine overall status
    if all(status == "operational" for status in health_status.values() if status != "unknown"):
        health_status["status"] = "healthy"
    else:
        health_status["status"] = "degraded"

    return health_status
