import google.generativeai as genai
import os
import logging
from typing import List, Any
from dotenv import load_dotenv

# Setup logger
logger = logging.getLogger(__name__)
load_dotenv()

class AutoRotatingLLM:
    """
    Wrapper cho Google Gemini với tính năng tự động xoay vòng API Key.
    """
    
    def __init__(
        self, 
        model_name: str = "gemini-2.5-pro", # Hoặc gemini-1.5-flash
        api_keys: List[str] = None,
        temperature: float = 0.1
    ):
        self.model_name = model_name
        self.temperature = temperature
        
        # 1. Lấy danh sách Key
        if api_keys:
            self.api_keys = api_keys
        else:
            # Tự động tìm trong .env nếu không truyền vào
            # Ví dụ .env có: GEMINI_KEYS="key1,key2,key3"
            env_keys = os.getenv("GEMINI_KEYS", "")
            if env_keys:
                self.api_keys = [k.strip() for k in env_keys.split(",") if k.strip()]
            else:
                # Fallback: Lấy 1 key đơn lẻ
                single_key = os.getenv("GEMINI_API_KEY")
                if single_key:
                    self.api_keys = [single_key]
                else:
                    raise ValueError("❌ Không tìm thấy API Key nào!")

        self.current_index = 0
        logger.info(f"AutoRotatingLLM initialized with {len(self.api_keys)} keys. Model: {model_name}")

    def _get_current_key(self) -> str:
        return self.api_keys[self.current_index]

    def _rotate_key(self):
        """Chuyển sang key tiếp theo"""
        prev_index = self.current_index
        self.current_index = (self.current_index + 1) % len(self.api_keys)
        logger.warning(f"🔄 Rotating API Key: {prev_index} -> {self.current_index}")

    def _configure_model(self):
        """Cấu hình Gemini với key hiện tại"""
        current_key = self._get_current_key()
        genai.configure(api_key=current_key)
        
        # Cấu hình generation config
        generation_config = {
            "temperature": self.temperature,
        }
        
        return genai.GenerativeModel(
            model_name=self.model_name,
            generation_config=generation_config
        )

    def generate_content(self, prompt: str) -> Any:
        """
        Hàm thay thế cho model.generate_content() gốc.
        Tự động thử key khác nếu gặp lỗi.
        """
        attempts = 0
        max_attempts = len(self.api_keys) # Thử tối đa hết vòng các key

        while attempts < max_attempts:
            try:
                # 1. Cấu hình & lấy model với key hiện tại
                model = self._configure_model()
                
                # 2. Gọi API
                response = model.generate_content(prompt)
                
                # 3. Trả về kết quả (giữ nguyên format của Gemini)
                return response

            except Exception as e:
                error_msg = str(e).lower()
                logger.error(f"⚠️ Key {self.current_index} failed: {e}")

                # Kiểm tra xem có phải lỗi do Key/Quota không
                is_auth_error = any(k in error_msg for k in [
                    "429", "quota", "limit", "403", "api_key", "permission"
                ])

                if is_auth_error:
                    # Nếu lỗi Key -> Xoay Key và thử lại
                    self._rotate_key()
                    attempts += 1
                else:
                    # Nếu lỗi khác (ví dụ prompt quá dài, server sập) -> Ném lỗi luôn
                    raise e
        
        # Nếu đã thử hết key mà vẫn lỗi
        raise Exception("❌ All API keys exhausted or failed!")

# --- Helper để tạo instance nhanh ---
def get_gemini_model():
    """Hàm này các Agent sẽ gọi để lấy model"""
    # Bạn có thể lưu list key vào .env dưới dạng: 
    # GEMINI_KEYS="key_abc123,key_xyz456,key_789JQKA"
    return AutoRotatingLLM()