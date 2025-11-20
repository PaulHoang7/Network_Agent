import streamlit as st
from main import generate_config
from reverse_parser import explain_config

st.set_page_config(page_title="AI Network Config Agent", layout="wide")

st.title("🧠 AI Network Configuration Agent")

mode = st.radio("Chọn chế độ:", ["Sinh cấu hình từ yêu cầu", "Giải thích cấu hình (Reverse Config)"])

user_text = st.text_area("Nhập nội dung yêu cầu:", height=200)

if st.button("Thực thi"):
    if not user_text.strip():
        st.warning("Vui lòng nhập nội dung trước!")
    else:
        if mode == "Sinh cấu hình từ yêu cầu":
            output = generate_config(user_text)
            st.subheader("📌 Cấu hình được sinh ra:")
            st.code(output, language="text")

        elif mode == "Giải thích cấu hình (Reverse Config)":
            explanation = explain_config(user_text)
            st.subheader("📌 Giải thích cấu hình:")
            st.write(explanation)
