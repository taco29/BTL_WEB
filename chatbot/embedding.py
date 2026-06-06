from langchain_huggingface import HuggingFaceEmbeddings

class EmbeddingModel:
    def __init__(
        self,
        model_name: str = 'sentence-transformers/all-MiniLM-L6-v2',
        normalize: bool = True
    ):
        self.model_name = model_name
        self.normalize = normalize
        self.embedding = HuggingFaceEmbeddings(
            model_name = self.model_name,
            encode_kwargs = {'normalize_embeddings': self.normalize}
        )

    def get(self):
        return self.embedding
