import os
import warnings


os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

warnings.filterwarnings("ignore", category=UserWarning)


os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
os.environ["HF_HUB_DISABLE_WARNINGS"] = "1"
os.environ["TQDM_DISABLE"] = "1"

from retrieve import retriever
from gen import AnswerGenerator
from dotenv import load_dotenv

import threading
import edge_tts
import asyncio
import pygame
import time
from normalize_text import clean_text_for_speech


load_dotenv(override=True)
API_KEY = os.getenv("GOOGLE_API_KEY")

class ChatBot:
    def __init__(self, data_path: str, k: int = 6):
        self.retriever = retriever(data_path, k=k).get_retriever()
        self.generator = AnswerGenerator()

    def ask(self, question: str) -> str:
        result = self.generator.answer(self.retriever, question)
        return result["result"]


def speak_text(text: str):
    try:
        # Nếu đoạn text trống (sau khi chuẩn hóa), bỏ qua
        if not text or not text.strip():
            return
            
        pygame.mixer.init()
        # Chọn giọng đọc: vi-VN-NamMinhNeural (Nam) hoặc vi-VN-HoaiMyNeural (Nữ)
        voice = "vi-VN-NamMinhNeural" 
        filename = f"temp_{int(time.time())}.mp3"
        
        import subprocess
        
        result = subprocess.run(
            ["edge-tts", "--text", text, "--voice", voice, "--write-media", filename],
            capture_output=True, text=True
        )
        
        if not os.path.exists(filename):
            print(f"\n(Lỗi tạo âm thanh: {result.stderr})")
            return
        
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
            
        pygame.mixer.quit()
        os.remove(filename)
    except Exception as e:
        print(f"\n(Lỗi phát âm thanh: {e})")
        print(f"Đoạn text gây lỗi: '{text}'\n")


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