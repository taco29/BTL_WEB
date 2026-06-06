from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

headers_to_split_on = [
    ("#", "Header 1"),
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

    def chunking_for_each_major(self, text: str) ->list:
        """
        - section ngành : mỗi ngành 1 dòng
        - còn lại: recursive
        """
        header_splits = self.header_splitter.split_text(text)
        final_docs = []

        for doc in header_splits:
            lines = doc.page_content.split("\n")
            list_lines =[l for l in lines if l.strip().startswith("- -")]

            if len(list_lines) >= 3:
                intro_lines = []
                for line in lines:
                    if line.strip().startswith("- -"):
                        break
                    intro_lines.append(line)
                intro = '\n'.join(intro_lines).strip()

                for line in list_lines:
                    content = f"{intro}\n{line}".strip() if intro else line
                    final_docs.append(Document(page_content=content, metadata= doc.metadata))
            else:
                sub_docs = self.text_splitter.split_documents([doc])
                final_docs.extend(sub_docs)
        return final_docs
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
# from langchain_core.documents import Document
# chunker = TextChunker()
# text = chunker.load_docs(r"C:\Users\Admin\Code\webweb\data\data.md")
# docs = chunker.chunking_for_each_major(text)

# for i, doc in enumerate(docs):
#     if 'UDU' in doc.page_content or 'định hướng ứng dụng' in doc.page_content.lower():
#         print(f"--- CHUNK {i} ---")
#         print("METADATA:", doc.metadata)
#         print("CONTENT:", doc.page_content)
#         print()