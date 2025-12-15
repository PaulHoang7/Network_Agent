import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("❌ Lỗi: Chưa cấu hình GEMINI_API_KEY trong file .env")

genai.configure(api_key=api_key)

def get_gemini_model():
    return genai.GenerativeModel("gemini-2.5-pro") # Hoặc version bạn đang dùng