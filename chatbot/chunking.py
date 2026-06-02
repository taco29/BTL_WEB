from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

headers_to_split_on = [
    ("##", "Header 2"),
    ("###", "Header 3"),
    ("####", "Header 4")
]

class TextChunker:
    def __init__(self):
        self.header_splitter = MarkdownHeaderTextSplitter(headers_to_split_on= headers_to_split_on)
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    def load_docs(self, path: str) -> str:
        loader = TextLoader(path, encoding='utf-8')
        return loader.load()[0].page_content
    
    def chunking(self, text: str) -> list:
        header_splits = self.header_splitter.split_text(text)
        final_splits = self.text_splitter.split_documents(header_splits)
        return final_splits

# chunker = TextChunker()
# text_data = chunker.load_docs("./data/data.md")
# docs = chunker.chunking(text_data)
# for i, doc in enumerate(docs):
#     print(f"CHUNK {i}")
#     print("METADATA:")
#     for key, value in doc.metadata.items():
#         print(f"   - {key}: {value}")
#     print("\n noi dung:")
#     print(doc.page_content)
#     print("\n\n")