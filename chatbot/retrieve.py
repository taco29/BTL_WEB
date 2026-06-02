from chunking import TextChunker
from qdrant import CreateVectorStore
from embedding import EmbeddingModel

class retriever:
    def __init__(self, path: str, k: int):
        self.path = path
        self.k = k
    
    def get_retriever(self):
        chunker = TextChunker()
        text = chunker.load_docs(self.path)
        docs = chunker.chunking(text)
        embedding = EmbeddingModel().get()
        vector_store = CreateVectorStore().create_vector_store(docs, embedding)
        return vector_store.as_retriever(search_type="similarity", search_kwargs={"k": self.k})

    def get_chunks(self):
        chunker = TextChunker()
        text = chunker.load_docs(self.path)
        return chunker.chunking(text)