from typing import Tuple
from langdetect import detect, DetectorFactory
# from config.settings import settings # Tạm bỏ nếu chưa có
# from config.logging_config import get_logger # Tạm bỏ nếu chưa có
import logging

# Setup logger đơn giản
logger = logging.getLogger(__name__)
DetectorFactory.seed = 0

class Translator:
    def __init__(self, llm):
        self.llm = llm
        # Cấu hình cứng hoặc lấy từ env
        self.data_language = "en"  # Dữ liệu RFC và Config của mình là tiếng Anh
        self.auto_translate = True
        self.cache = {}
        logger.info("Translator initialized")

    def detect_language(self, text: str) -> str:
        try:
            lang = detect(text)
            return lang
        except Exception as e:
            logger.warning(f"Language detection failed: {e}")
            return self.data_language

    def translate(self, text: str, target_lang: str, context: str = "general") -> str:
        # Cache key để tiết kiệm tiền API
        cache_key = f"{text}:{target_lang}:{context}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        language_names = {
            'en': 'English',
            'vi': 'Vietnamese',
            # Các ngôn ngữ khác nếu cần
        }
        lang_name = language_names.get(target_lang, target_lang)

        # --- SỬA PROMPT CHO NETWORK ---
        if context == "query":
            # Dịch câu hỏi đầu vào
            prompt = f"""Translate the following text to {lang_name}.

IMPORTANT RULES:
1. DO NOT add or remove any information.
2. Keep the exact same meaning and structure.
3. PRESERVE all technical terms related to **Computer Networking, Cisco IOS commands, IP addresses, and RFC standards**.
4. Do not translate terms like 'VLAN', 'OSPF', 'ACL', 'Interface', 'NAT'.
5. Provide ONLY the translation, nothing else.

Text to translate:
{text}

Translation:"""
        
        elif context == "response":
            # Dịch câu trả lời đầu ra
            prompt = f"""Translate to {lang_name}, maintain formatting (markdown/code blocks) and structure:

{text}

Translation:"""
        else:
            prompt = f"Translate to {lang_name}: {text}"

        try:
            # Gọi Gemini
            response = self.llm.generate_content(prompt)
            translated = response.text.strip()
            
            # Lưu cache
            self.cache[cache_key] = translated
            return translated
        except Exception as e:
            logger.error(f"Translation failed: {e}")
            return text

    def process_query(self, query: str) -> Tuple[str, str]:
        """
        Nhận câu hỏi -> Phát hiện ngôn ngữ -> Dịch sang Tiếng Anh (nếu cần)
        Trả về: (query_english, original_lang)
        """
        detected_lang = self.detect_language(query)
        
        # Nếu user hỏi tiếng Việt -> Dịch sang Anh để tìm RFC/Template tốt hơn
        if self.auto_translate and detected_lang != self.data_language:
            print(f"🌐 [Translator] Dịch câu hỏi: {detected_lang} -> {self.data_language}")
            translated_query = self.translate(query, self.data_language, context="query")
            return translated_query, detected_lang
        
        return query, detected_lang

    def translate_response(self, response: str, target_lang: str) -> str:
        """
        Dịch câu trả lời cuối cùng về ngôn ngữ gốc của user
        """
        if target_lang == self.data_language:
            return response

        print(f"🌐 [Translator] Dịch câu trả lời: {self.data_language} -> {target_lang}")
        return self.translate(response, target_lang, context="response")