from retrieval.chroma_pipeline import ChromaPipeline

if __name__ == "__main__":
    # Initialize the Chroma pipeline
    retrieval = ChromaPipeline(embedding_model_name="all-MiniLM-L6-v2")

    # Add some sample documents
    documents = [
        "Retrieval-Augmented Generation is a technique that combines retrieval and generation.",
        "Chroma is a vector database optimized for document retrieval.",
        "Hugging Face provides state-of-the-art NLP models.",
        "Docker is a tool to containerize applications.",
        "FastAPI is a modern web framework for building APIs."
    ]
    retrieval.add_documents(documents)

    # Test retrieval
    query = "Tell me about Chroma."
    results = retrieval.retrieve(query, top_k=3)
    
    print("\nTop Retrieved Documents:")
    for doc, score in results:
        print(f"Document: {doc} | Score: {score}")
