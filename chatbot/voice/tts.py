import os
import re
import time
import threading
import pygame
from queue import Queue, Empty

# Khai báo cờ ngắt toàn cục để chặn giọng nói cũ
stop_speaking_event = threading.Event()

# Khởi tạo mô hình AI tiếng Việt dùng chung (Singleton)
tts_engine = None

def get_tts_engine():
    global tts_engine
    if tts_engine is None:
        print("\n[Hệ thống] Đang khởi động mô hình AI Giọng nói (VieNeu-TTS)... Lần đầu sẽ tốn xíu thời gian để nạp vào RAM nhé!")
        try:
            from vieneu import Vieneu
            tts_engine = Vieneu(emotion="natural")
            print("[Hệ thống] Nạp mô hình AI Giọng nói thành công! Sẵn sàng phát âm.")
        except Exception as e:
            print(f"[Hệ thống] Lỗi tải mô hình AI Giọng nói: {e}")
            return None
    return tts_engine

def speak_text(text: str):
    try:
        # Nếu đoạn text trống (sau khi chuẩn hóa), bỏ qua
        if not text or not text.strip():
            return
            
        # Chia nhỏ đoạn text thành từng câu dài (dấu chấm, hỏi chấm, chấm than)
        # Lưu ý: Không cắt theo dấu phẩy vì đoạn quá ngắn đọc sẽ xong trước khi CPU kịp render đoạn tiếp theo, gây ra độ trễ giữa các chữ.
        sentences = re.split(r'(?<=[.!?\n])\s+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        pygame.mixer.init()
        
        audio_queue = Queue()
        
        # Hàm chạy ngầm (Producer) để tạo file audio liên tục
        def producer():
            engine = get_tts_engine()
            
            for i, sentence in enumerate(sentences):
                if stop_speaking_event.is_set():
                    break
                    
                if not sentence:
                    continue
                    
                # Vieneu sinh ra định dạng WAV
                filename = f"temp_{int(time.time())}_{i}.wav"
                safe_text = sentence.replace('"', '')
                
                success = False
                if engine is not None:
                    try:
                        # Lấy giọng "Ly" (Trúc Ly - nữ miền Bắc)
                        voice_data = engine.get_preset_voice("Ly")
                        
                        audio = engine.infer(text=safe_text, voice=voice_data)
                        engine.save(audio, filename)
                        if os.path.exists(filename) and os.path.getsize(filename) > 0:
                            audio_queue.put(filename)
                            success = True
                    except Exception as e:
                        print(f"\n[Giọng nói] Lỗi quá tải mô hình VieNeu-TTS: {e}")
                
                # Nếu VieNeu bị lỗi (do tràn RAM, cấu hình yếu, v.v.), tự động chuyển sang dùng Google TTS (gTTS)
                if not success and not stop_speaking_event.is_set():
                    print(f"\n[Giọng nói] Đang dùng giọng Google dự phòng cho câu: '{safe_text}'")
                    try:
                        from gtts import gTTS
                        fallback_filename = f"temp_{int(time.time())}_{i}.mp3"
                        tts = gTTS(text=safe_text, lang='vi')
                        tts.save(fallback_filename)
                        if os.path.exists(fallback_filename) and os.path.getsize(fallback_filename) > 0:
                            audio_queue.put(fallback_filename)
                    except Exception as e:
                        print(f"\n[Giọng nói] Google TTS cũng bị lỗi: {e}")
            
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
