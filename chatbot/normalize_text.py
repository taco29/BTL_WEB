import re

def clean_text_for_speech(text: str) -> str:
    
    text = re.sub(r'[\*#]+', '', text)
    text = re.sub(r'^\s*[-]\s+', '', text, flags=re.MULTILINE)
    text = text.replace('_', ' ')
    
   
    text = text.replace('/', ' trên ')
    
    abbreviations = {
        "THPT": "Trung học phổ thông",
        "ĐGNL": "Đánh giá năng lực",
        "ĐGTD": "Đánh giá tư duy",
        "CT": "chương trình",
        "DM": "danh mục",
        "UDU": "U D U", 
        "PTIT": "P T I T",
        "AIoT": "A I O T"
    }
    
    for abbr, full_form in abbreviations.items():
        text = re.sub(fr'\b{abbr}\b', full_form, text)
    
    text = re.sub(r'\n+', '. ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r',\s*,', ',', text)
    text = re.sub(r',\s*\.', '.', text)
    
    return text
