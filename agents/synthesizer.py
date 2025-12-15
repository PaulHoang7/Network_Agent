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
        - Hiển thị đoạn cấu hình CLI trong block code.
        - Giải thích ngắn gọn các lệnh chính dựa trên kiến thức RFC (nếu có).
        - Đưa ra cảnh báo an toàn nếu cần.
        """
        
        response = self.model.generate_content(prompt)
        return response.text