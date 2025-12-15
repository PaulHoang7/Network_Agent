import json
from core.llm import get_gemini_model
from utils import (
    diagnostics, 
    parse_acl_basic, 
    parse_interface_basic, 
    parse_nat_dynamic_basic
)

class ClarifierAgent:
    def __init__(self):
        self.model = get_gemini_model()
        self.allowed_intents = [
            "create_vlan", "setup_ospf_advanced", "advanced_acl", 
            "nat_static", "nat_dynamic", "set_interface_ip"
        ]

    def clarify(self, user_text):
        print(f"🕵️ [Agent 1] Phân tích ý định: '{user_text}'")
        
        prompt = f"""
        Bạn là chuyên gia mạng Cisco. Phân tích yêu cầu: "{user_text}"
        TRẢ VỀ JSON DUY NHẤT:
        {{
            "intent": "...",
            "params": {{ ... }}
        }}
        Intent phải thuộc: {self.allowed_intents}.
        Nếu là VLAN, lấy vlan_id, name.
        Nếu là Interface IP, lấy interface, ip, mask, description.
        ... (giữ nguyên logic prompt cũ của bạn)
        """
        
        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip().replace("```json", "").replace("```", "")
            data = json.loads(text)
            
            # --- Logic Validation ---
            errors = diagnostics(data)
            if errors:
                return {
                    "success": False,
                    "error": "Lỗi tham số: " + " | ".join(errors),
                    "data": data
                }
            
            return {"success": True, "data": data}
            
        except Exception as e:
            return {"success": False, "error": f"Lỗi phân tích: {str(e)}", "data": None}