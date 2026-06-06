import os
from retrieve import retriever
from gen import AnswerGenerator
from dotenv import load_dotenv

load_dotenv(override=True)
API_KEY = os.getenv("GOOGLE_API_KEY")

class ChatBot:
    def __init__(self, data_path: str, k: int = 6):
        self.retriever = retriever(data_path, k=k).get_retriever()
        self.generator = AnswerGenerator()

    def ask(self, question: str) -> str:
        result = self.generator.answer(self.retriever, question)
        return result["result"]


def main():
    path = r"./data/data.md"
    bot = ChatBot(path)

    print("Chatbot tuyển sinh PTIT (gõ 'exit' để thoát)\n")
    while True:
        question = input("Bạn: ").strip()
        if not question:
            continue
        if question.lower() == "exit":
            break
        answer = bot.ask(question)
        print(f"PTIT: {answer}\n")

    # print("\nSOURCES:")
    # for doc in result["source_documents"]:
    #     print("-", doc.metadata)
    #     print(doc.page_content[:200], "...\n")

    # print("\n--- CHUNKS IN THE DOCUMENT ---")
    # docs = retriever(path, k=3).get_chunks()
    # for i, doc in enumerate(docs):
    #     print(f"Chunk {i+1}:")
    #     print(doc.page_content)
    # print("--------------------")   
if __name__ == "__main__":
    main()