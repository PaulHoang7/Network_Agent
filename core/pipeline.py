# # Gọn hơn nhiều
# from agents import ClarifierAgent, RetrieverAgent, GeneratorAgent, SynthesizerAgent
# from core.llm import get_gemini_model
# from utils.translator import Translator
# class NetworkRAGPipeline:
#     def __init__(self):
#         # 1. Khởi tạo LLM chung
#         self.llm = get_gemini_model()
        
#         # 2. Khởi tạo Translator (truyền LLM vào)
#         self.translator = Translator(self.llm)

#         # 3. Khởi tạo các Agent
#         self.clarifier = ClarifierAgent()
#         self.retriever = RetrieverAgent()
#         self.generator = GeneratorAgent()
#         self.synthesizer = SynthesizerAgent()

#     def run(self, user_input):
#         # --- BƯỚC 0: DỊCH ĐẦU VÀO (VI -> EN) ---
#         # query_en: để máy hiểu, original_lang: để nhớ ngôn ngữ trả lời
#         query_en, original_lang = self.translator.process_query(user_input)
        
#         # --- BƯỚC 1: CLARIFY (Dùng query_en) ---
#         clarify_result = self.clarifier.clarify(query_en)
#         if not clarify_result["success"]:
#             # Nếu lỗi, trả về lỗi (có thể dịch lỗi này nếu muốn)
#             return self.translator.translate_response(f"❌ {clarify_result['error']}", original_lang)
        
#         intent_data = clarify_result["data"]
        
#         # --- BƯỚC 2: RETRIEVE ---
#         resources = self.retriever.retrieve(intent_data, query_en)
#         if not resources["template_file"]:
#              msg = f"❌ Xin lỗi, tôi chưa có template cho hành động: {intent_data['intent']}"
#              return self.translator.translate_response(msg, original_lang)

#         # --- BƯỚC 3: GENERATE ---
#         config_text, error = self.generator.generate(
#             resources["template_file"], 
#             intent_data["params"]
#         )
#         if error:
#             return self.translator.translate_response(f"❌ Lỗi sinh cấu hình: {error}", original_lang)

#         # --- BƯỚC 4: SYNTHESIZE ---
#         # Agent 4 tổng hợp câu trả lời bằng Tiếng Anh (dựa trên RFC tiếng Anh)
#         english_response = self.synthesizer.synthesize(
#             query_en,
#             config_text,
#             resources["rfc_context"]
#         )
        
#         # --- BƯỚC 5: DỊCH ĐẦU RA (EN -> VI) ---
#         final_response = self.translator.translate_response(english_response, original_lang)
        
#         return final_response

from agents import ClarifierAgent, RetrieverAgent, GeneratorAgent, SynthesizerAgent
from core.llm import get_gemini_model
from utils.translator import Translator

class NetworkRAGPipeline:
    def __init__(self):
        # 1. Khởi tạo LLM chung (Chỉ tạo 1 lần duy nhất để quản lý Key)
        self.llm = get_gemini_model()
        
        # 2. Khởi tạo Translator
        self.translator = Translator(self.llm)

        # 3. Khởi tạo các Agent (Truyền llm vào nếu Agent hỗ trợ, 
        # nhưng với code hiện tại của bạn thì Agent tự gọi get_gemini_model bên trong, 
        # nên để như cũ cũng không sao. Ở đây mình giữ nguyên cách gọi của bạn để tránh sửa các file Agent).
        self.clarifier = ClarifierAgent()
        self.retriever = RetrieverAgent()
        self.generator = GeneratorAgent()
        self.synthesizer = SynthesizerAgent()

    def run(self, user_input):
        # --- BƯỚC 0: DỊCH ĐẦU VÀO (VI -> EN) ---
        # Mục đích: Để tìm kiếm trong FAISS và chọn Template chuẩn xác hơn
        query_en, original_lang = self.translator.process_query(user_input)
        
        # --- BƯỚC 1: CLARIFY (Dùng query tiếng Anh) ---
        clarify_result = self.clarifier.clarify(query_en)
        
        if not clarify_result["success"]:
            # Nếu lỗi, trả về lỗi (Dịch lỗi sang ngôn ngữ gốc của user)
            return self.translator.translate_response(f"❌ {clarify_result['error']}", original_lang)
        
        intent_data = clarify_result["data"]
        
        # --- BƯỚC 2: RETRIEVE ---
        resources = self.retriever.retrieve(intent_data, query_en)
        
        if not resources["template_file"]:
             msg = f"❌ Xin lỗi, tôi chưa có template cấu hình cho hành động: {intent_data['intent']}"
             return self.translator.translate_response(msg, original_lang)

        # --- BƯỚC 3: GENERATE ---
        config_text, error = self.generator.generate(
            resources["template_file"], 
            intent_data["params"]
        )
        
        if error:
            return self.translator.translate_response(f"❌ Lỗi sinh cấu hình: {error}", original_lang)

        # --- BƯỚC 4: SYNTHESIZE (TỔNG HỢP) ---
        # LƯU Ý QUAN TRỌNG: 
        # Ở bước này, Agent 4 đã được cấu hình (trong prompt) để trả lời bằng Tiếng Việt.
        # Nên kết quả trả về ở đây đã là Tiếng Việt chuẩn.
        final_response = self.synthesizer.synthesize(
            user_input,      # Đưa câu gốc tiếng Việt vào để Agent nắm ngữ cảnh
            config_text,
            resources["rfc_context"]
        )
        
        # --- BƯỚC 5: TRẢ VỀ KẾT QUẢ ---
        # Không cần dịch lại nữa (Bỏ bước translate_response)
        return final_response