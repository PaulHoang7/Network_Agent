# 🧠 AI Network Configuration Agent  
### Sinh cấu hình mạng Cisco bằng tiếng Việt • Hỗ trợ ACL, VLAN, OSPF, NAT, Interface • Reverse Config • Fallback Parser • GUI Streamlit • Docker Support

---

## 🚀 Giới thiệu

**Network Agent** là một ứng dụng AI sử dụng mô hình ngôn ngữ (Gemini/OpenAI) để:

- 📝 Hiểu yêu cầu cấu hình mạng bằng **Tiếng Việt tự nhiên**
- ⚙️ Sinh cấu hình router/switch **Cisco** tự động (IOS)
- 🎯 Hỗ trợ nhiều thành phần:
  - VLAN
  - OSPF nâng cao
  - ACL nâng cao
  - NAT Static / Dynamic + PAT
  - Interface IP  
- 🔄 Reverse Config: AI đọc & giải thích cấu hình Cisco
- 🛠 Có **fallback parser** đảm bảo luôn hoạt động kể cả khi LLM trả về JSON sai
- 🌐 Giao diện GUI bằng **Streamlit**
- 🐳 Hỗ trợ **Docker**, dễ dàng deploy ở mọi nơi

---

## 📂 Cấu trúc thư mục
Network_Agent/
│
├── main.py 
├── gui.py 
├── planner.py 
├── generator.py
├── validator.py 
│
├── intent_parser_llm.py 
├── intent_parser_basic_acl.py 
├── intent_parser_basic_nat.py 
├── intent_parser_basic_interface.py 
├── reverse_parser.py 
│
├── templates/ # Jinja2 templates for config
│ ├── vlan_cisco.txt
│ ├── ospf_cisco_advanced.txt
│ ├── acl_extended.txt
│ ├── nat_static.txt
│ ├── nat_dynamic.txt
│ └── interface_ip.txt
├── requirements.txt
└── Dockerfile

---

## 🔧 Cài đặt

### 1️⃣ Clone repo

```bash
git clone https://github.com/PaulHoang7/Network_Agent.git
cd Network_Agent
2️⃣ Tạo môi trường Python
python -m venv venv
venv/Scripts/activate    # Windows
3️⃣ Cài thư viện
pip install -r requirements.txt
▶ Chạy ứng dụng GUI
streamlit run gui.py

