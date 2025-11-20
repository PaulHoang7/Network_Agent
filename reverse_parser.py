import google.generativeai as genai
import os


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-3-pro-preview")

def explain_config(config_text):

    prompt = f"""
Bạn là chuyên gia Cisco CCNA/CCNP.
Hãy phân tích đoạn cấu hình dưới đây và giải thích bằng tiếng Việt:

\"\"\" 
{config_text}
\"\"\"

Yêu cầu:
- Giải thích từng câu lệnh
- Tóm tắt chức năng chung
- Nhận xét nếu có lỗi
"""

    response = model.generate_content(prompt)
    return response.text
