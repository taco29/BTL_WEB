import threading
import os
import warnings
import threading


os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

warnings.filterwarnings("ignore", category=UserWarning)


os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
os.environ["HF_HUB_DISABLE_WARNINGS"] = "1"
os.environ["TQDM_DISABLE"] = "1"

from retrieve import retriever
from gen import AnswerGenerator
from dotenv import load_dotenv

from voice.tts import speak_text, stop_speaking_event
from voice.normalize_text import clean_text_for_speech

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
        
        # Kích hoạt cờ ngắt để dừng ngay lập tức luồng TTS hiện tại (nếu có)
        stop_speaking_event.set()
        
        if not question:
            continue
        if question.lower() == "exit":
            break
        answer = bot.ask(question)
        print(f"PTIT: {answer}\n")

        # Tắt cờ ngắt trước khi đọc luồng mới
        stop_speaking_event.clear()
        
        # Chuẩn hóa văn bản trước khi đưa vào hàm nói
        cleaned_answer = clean_text_for_speech(answer)
        threading.Thread(target=speak_text, args=(cleaned_answer,), daemon=True).start()

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