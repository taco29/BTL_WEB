import uuid
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from langchain_qdrant import QdrantVectorStore

class CreateVectorStore:
    def __init__(self, url="http://localhost:8888"):
        self.client = QdrantClient(url)

    def get_vector_size(self, embedding) -> int:
        if hasattr(embedding, "embedding_dimension"):
            return embedding.embedding_dimension

        sample = embedding.embed_documents(["test"])[0]
        return len(sample)

    def create_vector_store(self, documents, embedding, collection_name="vector_store", recreate: bool = False ):
        ids = [str(uuid.uuid4()) for _ in documents]
        vector_size = self.get_vector_size(embedding)

        if recreate and self.client.collection_exists(collection_name):
            self.client.delete_collection(collection_name)

        if not self.client.collection_exists(collection_name):
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
            )

        return QdrantVectorStore.from_documents(
            documents=documents,
            embedding=embedding,
            collection_name=collection_name,
            url="http://localhost:8888",
            ids=ids,
        )