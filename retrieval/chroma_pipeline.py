import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer


class ChromaPipeline:
    def __init__(self, embedding_model_name: str = "all-MiniLM-L6-v2"):
        """
        Initializes the Chroma pipeline with a sentence embedding model.
        :param embedding_model_name: Name of the pre-trained sentence embedding model.
        """
        print(f"Loading embedding model: {embedding_model_name}")
        #self.embedding_model = SentenceTransformer(embedding_model_name)
        self.embedding_model = embedding_model_name

        # Initialize Chroma client
        self.chroma_client = chromadb.Client(Settings(
            persist_directory="./chroma_storage",  # Directory for storing embeddings
            anonymized_telemetry=False
        ))

        # Create or get the collection
        self.collection = self.chroma_client.get_or_create_collection(
            name="documents",
            embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(self.embedding_model)
        )

    def add_documents(self, documents: list):
        """
        Adds documents to the Chroma collection.
        :param documents: List of documents (strings) to index.
        """
        print("Adding documents to Chroma...")
        for i, doc in enumerate(documents):
            self.collection.add(
                ids=[f"doc_{i}"],
                documents=[doc]
            )
        print(f"Added {len(documents)} documents to Chroma.")

    def retrieve(self, query: str, top_k: int = 5) -> list:
        """
        Retrieves the top-k most similar documents for the given query.
        :param query: Input query string.
        :param top_k: Number of top documents to retrieve.
        :return: List of tuples (document, score).
        """
        print(f"Querying: {query}")
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k
        )

        # Extract documents and scores from the query results
        documents = results.get("documents", [[]])[0]
        scores = results.get("distances", [[]])[0]
        return list(zip(documents, scores))
