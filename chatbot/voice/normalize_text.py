import re

def clean_text_for_speech(text: str) -> str:
    
    # Xóa các ký tự đặc biệt làm edge-tts bị lỗi (đặc biệt là các loại dấu ngoặc)
    text = re.sub(r'[\*#()\[\]{}]+', ' ', text)
    text = re.sub(r'^\s*[-]\s+', '', text, flags=re.MULTILINE)
    text = text.replace('_', ' ')
    
    # Đọc dấu gạch chéo thành chữ
    # text = text.replace('/', ' trên ')
    
    abbreviations = {
        "THPT": "Trung học phổ thông",
        "ĐGNL": "Đánh giá năng lực",
        "ĐGTD": "Đánh giá tư duy",
        "CT": "chương trình",
        "DM": "danh mục",
        "UDU": "U D U", 
        "PTIT": "P T I T",
        "AIoT": "A I O T",
        "ĐHQGHCM": "Đại học Quốc gia Hồ Chí Minh",
        "ĐHQGHN": "Đại học Quốc gia Hà Nội",
        "ĐHSPHN": "Đại học Sư Phạm Hà Nội",
        "ĐHBDTP": "Đại học Bách khoa Thành phố Hồ Chí Minh",
        "HSG": "Học sinh giỏi"
    }
    
    for abbr, full_form in abbreviations.items():
        text = re.sub(fr'\b{abbr}\b', full_form, text)
    
    # Chuyển đổi mã tổ hợp (A00, D01, X26, ...) thành chữ để tránh edge-tts bị lỗi (NoAudioReceived)
    # Ví dụ: A00 -> A không không, X26 -> X hai sáu
    digit_to_word = {'0': 'không', '1': 'một', '2': 'hai', '3': 'ba', '4': 'bốn', '5': 'năm', '6': 'sáu', '7': 'bảy', '8': 'tám', '9': 'chín'}
    def replace_block(match):
        letter = match.group(1)
        d1 = digit_to_word.get(match.group(2))
        d2 = digit_to_word.get(match.group(3))
        return f"{letter} {d1} {d2}"
        
    text = re.sub(r'\b([A-Za-z])(\d)(\d)', replace_block, text)
    
    text = re.sub(r'\n+', '. ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'[:,]\s*\.', '.', text) # Xóa các lỗi như ":." hoặc ",."
    text = re.sub(r',\s*,', ',', text)
    text = re.sub(r'\.\s*\.', '.', text)
    
    return text
