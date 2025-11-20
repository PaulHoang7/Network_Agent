import google.generativeai as genai
import json
from intent_parser_basic_acl import parse_acl_basic
from intent_parser_basic_nat import parse_nat_dynamic_basic
from intent_parser_basic_interface import parse_interface_basic
import os


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-3-pro-preview")

def parse_intent_llm(user_text):

    allowed_intents = [
        "create_vlan",
        "setup_ospf_advanced",
        "advanced_acl",
        "nat_static",
        "nat_dynamic",
        "set_interface_ip"
    ]

    prompt = f"""
Bạn là chuyên gia cấu hình mạng Cisco CCNA/CCNP.

Hãy phân tích yêu cầu dưới đây và TRẢ VỀ JSON DUY NHẤT theo mẫu:

{{
  "intent": "...",
  "params": {{
      ...
  }}
}}

⚠️ Chỉ được dùng 1 trong các intent sau:
{allowed_intents}

Nếu yêu cầu liên quan đến VLAN → intent phải là "create_vlan".
Nếu yêu cầu liên quan đến OSPF nâng cao → "setup_ospf_advanced".
Nếu yêu cầu liên quan ACL nâng cao → "advanced_acl".
Nếu yêu cầu liên quan NAT static → "nat_static".
Nếu yêu cầu liên quan NAT dynamic → "nat_dynamic".
Nếu yêu cầu đặt IP cho interface → "set_interface_ip".

YÊU CẦU:
\"\"\"{user_text}\"\"\"
"""

    response = model.generate_content(prompt)
    text = response.text.strip()

    # Xử lý nếu Gemini trả về ```json
    text = text.replace("```json", "").replace("```", "")

    data = json.loads(text)
    params = data["params"]
    # ACL defaults
    # FALLBACK: Interface IP
    if data["intent"] == "set_interface_ip":
        params = data["params"]
        required = ["interface", "ip", "mask", "description"]

        if any(r not in params for r in required):
            print("⚠ Fallback Interface parser activated!")
            return parse_interface_basic(user_text)

    
    if data["intent"] == "nat_dynamic":
        params = data["params"]

        required = ["start_ip", "end_ip", "netmask", "acl_number", "src", "src_wildcard"]
    
        if any(r not in params for r in required):
            print("⚠ Fallback NAT dynamic parser activated!")
            return parse_nat_dynamic_basic(user_text)
    
    if data["intent"] == "advanced_acl":
        if "rules" not in params or len(params["rules"]) == 0:
            print("⚠ Fallback ACL parser activated!")
            return parse_acl_basic(user_text)
        if "interface" not in params:
            params["interface"] = "g0/0"
        if "direction" not in params:
            params["direction"] = "in"
        if "acl_name" not in params:
            params["acl_name"] = "ACL_AUTO"

    if "networks" not in params:
        params["networks"] = []
        
    if "passive" not in params:
        params["passive"] = []

    if "costs" not in params:
        params["costs"] = {}

    if "process_id" not in params:
        params["process_id"] = 1

    # Nếu Gemini cố tình bịa intent → Sửa lại dựa vào nội dung
    if data["intent"] not in allowed_intents:
        user_lower = user_text.lower()

        if "vlan" in user_lower:
            data["intent"] = "create_vlan"
        elif "ospf" in user_lower:
            data["intent"] = "setup_ospf_advanced"
        elif "acl" in user_lower or "chặn" in user_lower:
            data["intent"] = "advanced_acl"
        elif "nat" in user_lower:
            if "static" in user_lower or "tĩnh" in user_lower:
                data["intent"] = "nat_static"
            else:
                data["intent"] = "nat_dynamic"
        elif "interface" in user_lower:
            data["intent"] = "set_interface_ip"

    return data
