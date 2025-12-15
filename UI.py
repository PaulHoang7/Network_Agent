# import streamlit as st
# from intent_parser_llm import parse_intent_llm
# from generator import generate_from_template
# from validator import diagnostics
# from reverse_parser import reverse_config
# from qa_rfc_hybrid import rfc_hybrid


# # ---------------------------------------
# #  SETUP GUI
# # ---------------------------------------
# st.set_page_config(page_title="Network Agent (Gemini)", layout="wide")

# st.markdown("""
# <style>

# .chat-box-user {
#     background-color: #4CAF50;           /* Xanh lá đậm */
#     color: white;                         /* Chữ trắng */
#     padding: 12px 16px;
#     border-radius: 12px;
#     margin: 8px 0px;
#     font-size: 17px;
# }

# .chat-box-bot {
#     background-color: #2F2F2F;            /* Xám đậm */
#     color: #F8F8F8;                       /* Chữ sáng */
#     padding: 12px 16px;
#     border-radius: 12px;
#     margin: 8px 0px;
#     font-size: 17px;
# }

# .chat-input {
#     font-size: 18px !important;
# }

# </style>
# """, unsafe_allow_html=True)


# # ---------------------------------------
# #  SESSION STATE
# # ---------------------------------------
# if "messages" not in st.session_state:
#     st.session_state.messages = []


# # ---------------------------------------
# #  SIDEBAR
# # ---------------------------------------
# st.sidebar.title("⚙️ Network Agent – Mode")
# mode = st.sidebar.radio("Chọn chế độ:", [
#     "Sinh cấu hình mạng",
#     "Reverse config",
#     "Hỏi kiến thức RFC (RAG)",
#     "Hỏi kiến thức mạng (LLM)"
# ])

# st.title("💬 Network Agent — Gemini Edition")


# # ---------------------------------------
# #  DISPLAY CHAT HISTORY
# # ---------------------------------------
# for msg in st.session_state.messages:
#     if msg["role"] == "user":
#         st.markdown(f"<div class='chat-box-user'><b>🧑‍💻 Bạn:</b><br>{msg['content']}</div>", unsafe_allow_html=True)
#     else:
#         st.markdown(f"<div class='chat-box-bot'><b>🤖 Agent:</b><br>{msg['content']}</div>", unsafe_allow_html=True)


# # ---------------------------------------
# #  USER INPUT BOX
# # ---------------------------------------
# user_input = st.chat_input("Nhập yêu cầu...")

# if user_input:
#     # Lưu tin nhắn user
#     st.session_state.messages.append({"role": "user", "content": user_input})

#     # ---------------------------------------
#     #  CHẾ ĐỘ 1 — Sinh cấu hình mạng
#     # ---------------------------------------
#     if mode == "Sinh cấu hình mạng":
#         intent = parse_intent_llm(user_input)

#         if "intent" not in intent:
#             reply = "❌ Không hiểu yêu cầu."
#         else:
#             template_map = {
#                 "vlan": "vlan.j2",
#                 "acl": "acl.j2",
#                 "ospf": "ospf.j2",
#                 "interface_ip": "interface_ip.j2",
#                 "nat": "nat.j2"
#             }

#             template_file = template_map.get(intent["intent"])

#             if not template_file:
#                 reply = f"❌ Không có template cho intent: {intent['intent']}"
#             else:
#                 errs = diagnostics(intent["params"])
#                 if errs:
#                     reply = "❌ Lỗi tham số cấu hình:\n" + "\n".join(errs)
#                 else:
#                     reply = generate_from_template("templates/" + template_file, intent["params"])


#     # ---------------------------------------
#     #  CHẾ ĐỘ 2 — Reverse config
#     # ---------------------------------------
#     elif mode == "Reverse config":
#         reply = reverse_config(user_input)


#     # ---------------------------------------
#     #  CHẾ ĐỘ 3 — Hỏi kiến thức RFC bằng RAG (FAISS)
#     # ---------------------------------------
#     elif mode == "Hỏi kiến thức RFC (RAG)":
#         reply = rfc_hybrid(user_input)


#     # ---------------------------------------
#     #  CHẾ ĐỘ 4 — Hỏi mạng (LLM trực tiếp)
#     # ---------------------------------------
#     elif mode == "Hỏi kiến thức mạng (LLM)":
#         from google.generativeai import GenerativeModel
#         import os
#         import google.generativeai as genai

#         genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
#         gpt = genai.GenerativeModel("gemini-2.5-pro")

#         reply = gpt.generate_content(user_input).text
#     # else:
#     #     reply = parse_intent_llm(user_input)  # Trả về JSON / thông tin từ Gemini


#     # Lưu reply
#     st.session_state.messages.append({"role": "assistant", "content": reply})

#     # Rerun để update UI
#     st.rerun()

import streamlit as st
import os
from dotenv import load_dotenv
from core.pipeline import NetworkRAGPipeline

# Load biến môi trường
load_dotenv()

# --- CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="Network Agent (RAG)",
    page_icon="🌐",
    layout="wide"
)

# --- CSS TÙY CHỈNH ---
st.markdown("""
<style>
    .stChatMessage {
        border-radius: 10px;
        padding: 10px;
    }
    .stChatInput {
        position: fixed;
        bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- TIÊU ĐỀ ---
st.title("🌐 Network Automation Agent")
st.caption("Powered by Gemini 2.5 Pro & FAISS RAG")

# --- SIDEBAR: CẤU HÌNH ---
with st.sidebar:
    st.header("⚙️ Cấu hình")
    
    # Nhập API Key nếu chưa có trong .env
    if not os.getenv("GEMINI_KEYS") and not os.getenv("GEMINI_API_KEY"):
        api_key = st.text_input("Nhập Gemini API Key", type="password")
        if api_key:
            os.environ["GEMINI_KEYS"] = api_key
            st.success("Đã nhận Key!")
    else:
        st.success("✅ Đã load API Key từ hệ thống")

    st.markdown("---")
    if st.button("🗑️ Xóa lịch sử chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("### 📚 Tài nguyên")
    st.markdown("- RFC Knowledge Base: **Loaded**")
    st.markdown("- Templates: **6 files**")

# --- KHỞI TẠO PIPELINE (CACHE) ---
@st.cache_resource
def get_pipeline():
    try:
        return NetworkRAGPipeline()
    except Exception as e:
        st.error(f"Không thể khởi tạo Agent: {e}")
        return None

# Chỉ load pipeline 1 lần duy nhất
pipeline = get_pipeline()

# --- KHỞI TẠO SESSION STATE (LỊCH SỬ CHAT) ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Chào bạn! Tôi là trợ lý mạng Cisco. Tôi có thể giúp gì cho bạn? (Ví dụ: Cấu hình OSPF, VLAN, ACL...)"}
    ]

# --- HIỂN THỊ LỊCH SỬ CHAT ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- XỬ LÝ INPUT NGƯỜI DÙNG ---
if prompt := st.chat_input("Nhập yêu cầu cấu hình mạng..."):
    # 1. Hiển thị tin nhắn người dùng
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Agent xử lý
    if pipeline:
        with st.chat_message("assistant"):
            with st.status("🤖 Agent đang suy nghĩ...", expanded=True) as status:
                try:
                    st.write("🔍 Đang phân tích ý định...")
                    # Gọi pipeline chạy
                    response = pipeline.run(prompt)
                    status.update(label="✅ Đã xử lý xong!", state="complete", expanded=False)
                    st.markdown(response)
                    
                    # Lưu vào lịch sử
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
                except Exception as e:
                    status.update(label="❌ Có lỗi xảy ra", state="error")
                    st.error(f"Lỗi: {e}")
    else:
        st.error("Vui lòng kiểm tra API Key để khởi động Agent.")
