from core.llm import get_gemini_model

class SynthesizerAgent:
    def __init__(self):
        self.model = get_gemini_model()

    def synthesize(self, user_query, config_text, rfc_context):
        print(f"✍️ [Agent 4] Tổng hợp câu trả lời...")
        
        prompt = f"""
        Bạn là trợ lý mạng Cisco hữu ích.
        
        1. YÊU CẦU: {user_query}
        
        2. CẤU HÌNH ĐỀ XUẤT (CLI):
        {config_text}
        
        3. THAM KHẢO RFC (RAG CONTEXT):
        {rfc_context}
        
        NHIỆM VỤ:
        - Hãy trả lời hoàn toàn bằng **TIẾNG VIỆT**.
        - Đầu tiên: Hiển thị đoạn code cấu hình trong block code (```).
        - Tiếp theo: Giải thích ngắn gọn tác dụng của các lệnh chính (bằng tiếng Việt).
        - Cuối cùng: Nếu có thông tin từ RFC, hãy trích dẫn ngắn gọn (đã dịch sang tiếng Việt) để giải thích tại sao lại cấu hình như vậy.
        - Nếu cấu hình có rủi ro bảo mật (ví dụ 'permit any'), hãy cảnh báo.
        """
        
        response = self.model.generate_content(prompt)
        return response.text