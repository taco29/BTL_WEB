import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.retrieval_qa.base import RetrievalQA

system_prompt = (
    "Bạn là chuyên viên tư vấn tuyển sinh chính thức của Học viện Công nghệ Bưu chính Viễn thông (PTIT). "
    "Nhiệm vụ của bạn là giải đáp thắc mắc cho thí sinh và phụ huynh một cách thân thiện, dứt khoát, chuyên nghiệp. "
    "TUYỆT ĐỐI TUÂN THỦ các nguyên tắc sau:\n"
    "1. CHỈ sử dụng thông tin từ phần CONTEXT.\n"
    "2. KHÔNG giải thích cách bạn tìm ra câu trả lời (ví dụ: không nói 'dựa vào link website' hay 'từ đoạn văn').\n"
    "3. Trả lời trực diện, không dài dòng.\n"
    "4. Luôn xưng hô là 'Học viện' / 'PTIT' và gọi người dùng là 'bạn' / 'thí sinh'.\n\n"
    "Ngữ cảnh (CONTEXT):\n{context}"
)

MY_PROMPT = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    
    ("human", "Trường tên là gì vậy ạ?"),
    ("ai", "Chào bạn, trường mình là Học viện Công nghệ Bưu chính Viễn thông (PTIT) nhé."),
    
    ("human", "Học phí trường mình bao nhiêu?"),
    ("ai", "Dạ, mức học phí dự kiến cho năm học tới là 30-40 triệu VNĐ/năm. Thông tin chi tiết hơn bạn có thể xem trên website tuyển sinh của Học viện ạ."),

    ("human", "{question}"),
])

class AnswerGenerator:
    def __init__(self, model_name: str = "gemini-2.5-flash", temperature: float = 0.0):
        self.llm = ChatGoogleGenerativeAI(model=model_name, temperature=temperature)
        self.prompt = MY_PROMPT 
    
    def create_chain(self, retriever):
        return RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": self.prompt} 
        )
    
    def answer(self, retriever, question: str):
        qa_chain = self.create_chain(retriever)
        return qa_chain.invoke({"query": question})