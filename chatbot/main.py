import os
from retrieve import retriever
from gen import AnswerGenerator
from dotenv import load_dotenv

load_dotenv(override=True)
API_KEY = os.getenv("GOOGLE_API_KEY")

def main():
    path = r"C:\Users\Admin\Code\webweb\data\data.md"
    question = "Ngành Công nghệ thông tin (định hướng ứng dụng) xét tuyển những Tổ hợp nào?"

    my_retriever = retriever(path, k=3).get_retriever()
    result = AnswerGenerator().answer(my_retriever, question)
    print("ANSWER:")
    print(result["result"])

    print("\nSOURCES:")
    for doc in result["source_documents"]:
        print("-", doc.metadata)
        print(doc.page_content[:200], "...\n")

    # print("\n--- CHUNKS IN THE DOCUMENT ---")
    # docs = retriever(path, k=3).get_chunks()
    # for i, doc in enumerate(docs):
    #     print(f"Chunk {i+1}:")
    #     print(doc.page_content)
    # print("--------------------")   
if __name__ == "__main__":
    main()