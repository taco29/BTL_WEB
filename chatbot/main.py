import os
import sys
import warnings
import json

# Đảm bảo stdout dùng UTF-8 để in tiếng Việt trên Windows
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

warnings.filterwarnings("ignore", category=UserWarning)


os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
os.environ["HF_HUB_DISABLE_WARNINGS"] = "1"
os.environ["TQDM_DISABLE"] = "1"

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
    # Đường dẫn tuyệt đối đến data.md, không phụ thuộc vào thư mục làm việc
    script_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(script_dir, "..", "data", "data.md")
    bot = ChatBot(path)
    print("READY", flush=True)

    for line in sys.stdin:
        question = line.strip()
        if not question: 
            continue
        try:
            answer = bot.ask(question)
            print(json.dumps({"answer": answer}, ensure_ascii=False), flush=True)
        except Exception as e:
            print(json.dumps({"error": str(e)}, ensure_ascii=False), flush=True)
        
    # if len(sys.argv) > 1:
    #     question = " ".join(sys.argv[1:])
    #     answer = bot.ask(question)
    #     print(answer)
    #     return

    # Chế độ interactive
    print("Chatbot tuyển sinh UDU (gõ 'exit' để thoát)\n")
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