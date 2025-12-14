from retrieval_rfc import search_rfc
import google.generativeai as genai
import os

# Load Gemini API Key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("❌ Lỗi: Chưa đặt biến môi trường GEMINI_API_KEY!")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-pro")

def rfc_hybrid(question):
    fname, chunk = search_rfc(question)

    if chunk is None:
        return "❌ Không tìm thấy đoạn RFC liên quan trong database."

    prompt = f"""
Bạn là chuyên gia mạng.

Dưới đây là TRÍCH ĐOẠN TỪ RFC ({fname}). 

--- RFC GỐC ---
{chunk}

--- CÂU HỎI ---
{question}

Hãy giải thích lại đoạn này theo cách:
- Dễ hiểu hơn
- Không được thêm thông tin ngoài RFC
- Giữ nguyên ý gốc của RFC
"""

    response = model.generate_content(prompt)
    return response.text
