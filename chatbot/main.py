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

# Khai báo cờ ngắt toàn cục để chặn giọng nói cũ
stop_speaking_event = threading.Event()

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
            
        import re
        import subprocess
        from queue import Queue, Empty
        
        # Chia nhỏ đoạn text thành từng câu dựa trên dấu chấm, phẩy, hỏi chấm, chấm than
        sentences = re.split(r'(?<=[.!?])\s+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        pygame.mixer.init()
        # Chọn giọng đọc: vi-VN-NamMinhNeural (Nam) hoặc vi-VN-HoaiMyNeural (Nữ)
        voice = "vi-VN-NamMinhNeural" 
        
        audio_queue = Queue()
        
        # Hàm chạy ngầm (Producer) để gọi edge-tts liên tục
        def producer():
            for i, sentence in enumerate(sentences):
                if stop_speaking_event.is_set():
                    break
                    
                if not sentence:
                    continue
                    
                filename = f"temp_{int(time.time())}_{i}.mp3"
                
                # Cần escape dấu ngoặc kép trong text
                safe_text = sentence.replace('"', '')
                
                # Chèn tham số --rate=+20% để tăng tốc độ nói
                result = subprocess.run(
                    ["edge-tts", "--rate=+20%", "--text", safe_text, "--voice", voice, "--write-media", filename],
                    capture_output=True, text=True
                )
                
                if stop_speaking_event.is_set():
                    # Xóa file vừa tạo nếu bị ngắt ngang
                    if os.path.exists(filename):
                        try: os.remove(filename)
                        except: pass
                    break
                
                if os.path.exists(filename):
                    audio_queue.put(filename)
                else:
                    print(f"\n(Lỗi tạo âm thanh cho câu: {result.stderr})")
            
            # Đánh dấu đã tải xong toàn bộ các câu
            audio_queue.put(None)
            
        # Kích hoạt luồng Producer
        threading.Thread(target=producer, daemon=True).start()
        
        # Vòng lặp Consumer: Lấy audio ra và phát
        while True:
            if stop_speaking_event.is_set():
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.stop()
                break
                
            try:
                # Dùng timeout để liên tục kiểm tra cờ ngắt trong lúc đợi file mới
                filename = audio_queue.get(timeout=0.1)
            except Empty:
                continue
                
            if filename is None: # Tín hiệu kết thúc
                break
                
            if os.path.exists(filename):
                pygame.mixer.music.load(filename)
                pygame.mixer.music.play()
                
                # Đợi cho phát xong câu hiện tại
                while pygame.mixer.music.get_busy():
                    if stop_speaking_event.is_set():
                        pygame.mixer.music.stop()
                        break
                    time.sleep(0.01)
                    
                # Giải phóng file âm thanh đang mở để có quyền xóa file
                if hasattr(pygame.mixer.music, 'unload'):
                    pygame.mixer.music.unload()
                else:
                    # Nếu pygame phiên bản cũ không có hàm unload
                    pygame.mixer.quit()
                    pygame.mixer.init()
                    
                # Xóa file ngay sau khi đọc xong
                try:
                    os.remove(filename)
                except Exception:
                    pass
                    
        # Dọn dẹp nốt các file thừa trong hàng đợi nếu bị ngắt
        while not audio_queue.empty():
            f = audio_queue.get()
            if f and os.path.exists(f):
                try: os.remove(f)
                except: pass
                
        pygame.mixer.quit()
    except Exception as e:
        print(f"\n(Lỗi phát âm thanh: {e})")
        print(f"Đoạn text gây lỗi: '{text}'\n")


def main():
    path = r".\data\data.md"
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