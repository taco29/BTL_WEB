import uuid
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from langchain_qdrant import QdrantVectorStore

class CreateVectorStore:
    def __init__(self, url="http://localhost:8888"):
        self.client = QdrantClient(url)

    def create_vector_store(self, documents, embedding, collection_name="vector_store"):
        ids = [str(uuid.uuid4()) for _ in documents]
        try:
            vector_size = embedding.embedding_dimension
        except Exception:
            try:
                sample = embedding.embed_querry("test")
            except Exception:
                sample = embedding.embed_documents("test")[0]
            vector_size = len(sample)
        
        if not self.client.collection_exists(collection_name):
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config = VectorParams(size= vector_size, distance= Distance.COSINE)
            )
        
        return QdrantVectorStore.from_documents(
            documents=documents,
            embedding=embedding,
            collection_name=collection_name,
            url="http://localhost:8888",
            ids=ids,
        )