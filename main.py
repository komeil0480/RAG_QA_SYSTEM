# from retrieval.chroma_pipeline import ChromaPipeline
# from models.hugging_face_model import HuggingFaceAPIModel

# def main():
#     # Step 1: Initialize Chroma pipeline
#     retrieval_pipeline = ChromaPipeline(embedding_model_name="all-MiniLM-L6-v2")

#     # Step 2: Add documents to the retrieval pipeline
#     documents = [
#         "Retrieval-Augmented Generation combines retrieval and generation.",
#         "Chroma is a vector database optimized for document retrieval.",
#         "Hugging Face provides state-of-the-art NLP models.",
#         "Docker is a tool to containerize applications.",
#         "FastAPI is a modern web framework for building APIs."
#     ]
#     retrieval_pipeline.add_documents(documents)

#     # Step 3: Initialize Hugging Face API model
#     huggingface_model = HuggingFaceAPIModel(
#         model_name="deepset/roberta-base-squad2",
#         api_token="your-huggingface-api-token"  # Replace with your actual token
#     )

#     # Step 4: User query
#     query = "What is Chroma?"

#     # Step 5: Retrieve relevant documents
#     retrieved_docs = retrieval_pipeline.retrieve(query, top_k=3)
#     context = " ".join([doc for doc, _ in retrieved_docs])

#     # Step 6: Generate answer using Hugging Face API
#     input_text = f"{context}\nQuestion: {query}"
#     print(input_text)
#     answer = huggingface_model.query(input_text)

#     # Step 7: Print the answer
#     print(f"Question: {query}")
#     print(f"Answer: {answer}")

# if __name__ == "__main__":
#     main()
