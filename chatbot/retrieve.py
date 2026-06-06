from chunking import TextChunker
from qdrant import CreateVectorStore
from embedding import EmbeddingModel
from langchain_community.retrievers import BM25Retriever
from langchain_core.retrievers import BaseRetriever
from langchain_core.documents import Document
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from typing import List, Any

class retriever:
    def __init__(self, path: str, k: int):
        self.path = path
        self.k = k
        self._docs = None

    def _get_docs(self):
        if self._docs is None:
            chunker = TextChunker()
            text = chunker.load_docs(self.path)
            self._docs = chunker.chunking_for_each_major(text)
        return self._docs

    def get_retriever(self):
        docs = self._get_docs()
        embedding = EmbeddingModel().get()

        vector_store = CreateVectorStore().create_vector_store(
            docs, embedding, recreate=False
        )
        vector_retriever = vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": self.k}
        )

        bm25_retriever = BM25Retriever.from_documents(docs)
        bm25_retriever.k = self.k

        return HybridRetriever(bm25=bm25_retriever, vector=vector_retriever, k=self.k)

    def get_chunks(self):
        return self._get_docs()


class HybridRetriever(BaseRetriever):
    bm25: Any   
    vector: Any 
    k: int

    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        bm25_docs = self.bm25.invoke(query)
        vector_docs = self.vector.invoke(query)

        scores = {}
        for rank, doc in enumerate(bm25_docs):
            key = doc.page_content
            scores[key] = scores.get(key, 0) + 1 / (rank + 60)

        for rank, doc in enumerate(vector_docs):
            key = doc.page_content
            scores[key] = scores.get(key, 0) + 1 / (rank + 60)

        all_docs = {doc.page_content: doc for doc in bm25_docs + vector_docs}
        ranked = sorted(all_docs.values(), key=lambda d: scores[d.page_content], reverse=True)
        return ranked[:self.k]

    def invoke(self, input: Any, config: Any = None, **kwargs) -> List[Document]:
        query = input if isinstance(input, str) else input.get("query", "")
        return self._get_relevant_documents(query, run_manager=None)