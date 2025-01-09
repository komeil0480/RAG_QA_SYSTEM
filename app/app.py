from fastapi import FastAPI
from app.queries import router as queries_router
from app.documents import router as documents_router
from app.embedding import router as embedding_router
from app.logs import router as logs_router

app = FastAPI()

# Include routers
app.include_router(queries_router, prefix="/query", tags=["Query"])
app.include_router(documents_router, prefix="/documents", tags=["Documents"])
app.include_router(embedding_router, prefix="/embedding", tags=["Embedding"])
app.include_router(logs_router, prefix="/logs", tags=["Logs"])
