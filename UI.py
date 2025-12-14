import streamlit as st
from intent_parser_llm import parse_intent_llm
from generator import generate_from_template
from validator import diagnostics
from reverse_parser import reverse_config
from qa_rfc_hybrid import rfc_hybrid


# ---------------------------------------
#  SETUP GUI
# ---------------------------------------
st.set_page_config(page_title="Network Agent (Gemini)", layout="wide")

st.markdown("""
<style>

.chat-box-user {
    background-color: #4CAF50;           /* Xanh lá đậm */
    color: white;                         /* Chữ trắng */
    padding: 12px 16px;
    border-radius: 12px;
    margin: 8px 0px;
    font-size: 17px;
}

.chat-box-bot {
    background-color: #2F2F2F;            /* Xám đậm */
    color: #F8F8F8;                       /* Chữ sáng */
    padding: 12px 16px;
    border-radius: 12px;
    margin: 8px 0px;
    font-size: 17px;
}

.chat-input {
    font-size: 18px !important;
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------------
#  SESSION STATE
# ---------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []


# ---------------------------------------
#  SIDEBAR
# ---------------------------------------
st.sidebar.title("⚙️ Network Agent – Mode")
mode = st.sidebar.radio("Chọn chế độ:", [
    "Sinh cấu hình mạng",
    "Reverse config",
    "Hỏi kiến thức RFC (RAG)",
    "Hỏi kiến thức mạng (LLM)"
])

st.title("💬 Network Agent — Gemini Edition")


# ---------------------------------------
#  DISPLAY CHAT HISTORY
# ---------------------------------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='chat-box-user'><b>🧑‍💻 Bạn:</b><br>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-box-bot'><b>🤖 Agent:</b><br>{msg['content']}</div>", unsafe_allow_html=True)


# ---------------------------------------
#  USER INPUT BOX
# ---------------------------------------
user_input = st.chat_input("Nhập yêu cầu...")

if user_input:
    # Lưu tin nhắn user
    st.session_state.messages.append({"role": "user", "content": user_input})

    # ---------------------------------------
    #  CHẾ ĐỘ 1 — Sinh cấu hình mạng
    # ---------------------------------------
    if mode == "Sinh cấu hình mạng":
        intent = parse_intent_llm(user_input)

        if "intent" not in intent:
            reply = "❌ Không hiểu yêu cầu."
        else:
            template_map = {
                "vlan": "vlan.j2",
                "acl": "acl.j2",
                "ospf": "ospf.j2",
                "interface_ip": "interface_ip.j2",
                "nat": "nat.j2"
            }

            template_file = template_map.get(intent["intent"])

            if not template_file:
                reply = f"❌ Không có template cho intent: {intent['intent']}"
            else:
                errs = diagnostics(intent["params"])
                if errs:
                    reply = "❌ Lỗi tham số cấu hình:\n" + "\n".join(errs)
                else:
                    reply = generate_from_template("templates/" + template_file, intent["params"])


    # ---------------------------------------
    #  CHẾ ĐỘ 2 — Reverse config
    # ---------------------------------------
    elif mode == "Reverse config":
        reply = reverse_config(user_input)


    # ---------------------------------------
    #  CHẾ ĐỘ 3 — Hỏi kiến thức RFC bằng RAG (FAISS)
    # ---------------------------------------
    elif mode == "Hỏi kiến thức RFC (RAG)":
        reply = rfc_hybrid(user_input)


    # ---------------------------------------
    #  CHẾ ĐỘ 4 — Hỏi mạng (LLM trực tiếp)
    # ---------------------------------------
    elif mode == "Hỏi kiến thức mạng (LLM)":
        from google.generativeai import GenerativeModel
        import os
        import google.generativeai as genai

        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        gpt = genai.GenerativeModel("gemini-2.5-pro")

        reply = gpt.generate_content(user_input).text
    # else:
    #     reply = parse_intent_llm(user_input)  # Trả về JSON / thông tin từ Gemini


    # Lưu reply
    st.session_state.messages.append({"role": "assistant", "content": reply})

    # Rerun để update UI
    st.rerun()
