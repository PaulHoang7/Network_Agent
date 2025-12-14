import google.generativeai as genai
import os


api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("❌ Lỗi: Chưa đặt biến môi trường GEMINI_API_KEY!")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-3-pro-preview")

def reverse_config(config_text):
    """
    Chuyển cấu hình mạng thành giải thích tiếng Việt.
    """
    lines = config_text.strip().split("\n")
    explanation = []

    for line in lines:
        l = line.strip()

        if l.startswith("interface"):
            iface = l.split()[1]
            explanation.append(f"- Interface {iface} được cấu hình.")
        
        elif l.startswith("ip address"):
            _, _, ip, mask = l.split()
            explanation.append(f"- Đặt IP {ip} subnet mask {mask}.")
        
        elif l.startswith("description"):
            desc = l.replace("description", "").strip()
            explanation.append(f"- Mô tả interface: {desc}.")
        
        elif l.startswith("no shutdown"):
            explanation.append("- Interface được bật (no shutdown).")
        
        else:
            explanation.append(f"- Lệnh khác: {l}")

    return "\n".join(explanation)

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
