import ipaddress

# --- CÁC HÀM VALIDATE CƠ BẢN ---

def validate_vlan(vlan_id):
    try:
        return 1 <= int(vlan_id) <= 4094
    except:
        return False

def validate_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except:
        return False

def validate_ports(ports):
    # Kiểm tra danh sách port (vd: [1, 2, 3])
    return all(str(p).isdigit() and 0 < int(p) <= 48 for p in ports)

def validate_acl(rules):
    for rule in rules:
        src = rule.get("src", "")
        dst = rule.get("dst", "")

        # 'any' luôn hợp lệ
        if src == "any" or dst == "any":
            continue

        # Kiểm tra IP nguồn và đích
        if not validate_ip(src):
            return False
        if not validate_ip(dst):
            return False
    return True


# --- HÀM CHẨN ĐOÁN CHÍNH (DIAGNOSTICS) ---

def diagnostics(intent_data):
    """
    Kiểm tra logic của dữ liệu Intent đã được parse.
    Trả về danh sách lỗi (list string) nếu có.
    """
    intent = intent_data.get("intent")
    params = intent_data.get("params", {})
    errors = []

    # 1. Kiểm tra VLAN
    if intent == "create_vlan":
        if not validate_vlan(params.get("vlan_id", 0)):
            errors.append(f"VLAN ID '{params.get('vlan_id')}' không hợp lệ (Phải từ 1–4094).")

    # 2. Kiểm tra ACL
    if intent == "advanced_acl":
        # Nếu không có rules, tạo rules rỗng để tránh lỗi key error
        if "rules" not in params:
            params["rules"] = []
        
        if not validate_acl(params["rules"]):
            errors.append("ACL chứa địa chỉ IP không đúng định dạng.")

    # 3. Kiểm tra OSPF
    if intent == "setup_ospf_advanced":
        router_id = params.get("router_id", "0.0.0.0")
        if not validate_ip(router_id):
            errors.append(f"Router-ID '{router_id}' không hợp lệ.")
    
    # 4. Kiểm tra Interface IP        
    if intent == "set_interface_ip":
        # Điền giá trị mặc định nếu thiếu (Self-healing)
        if "ip" not in params:
            params["ip"] = "0.0.0.0"
        if "mask" not in params:
            params["mask"] = "255.255.255.0"
        if "interface" not in params:
            params["interface"] = "g0/0"
        if "description" not in params:
            params["description"] = "NO-DESC"
        
        # Validate IP và Mask vừa điền
        if not validate_ip(params["ip"]):
            errors.append(f"IP Address '{params['ip']}' không hợp lệ.")
        if not validate_ip(params["mask"]):
            errors.append(f"Subnet Mask '{params['mask']}' không hợp lệ.")

    return errors

# import ipaddress

# def validate_vlan(vlan_id):
#     try:
#         return 1 <= int(vlan_id) <= 4094
#     except:
#         return False

# def validate_ip(ip):
#     try:
#         ipaddress.ip_address(ip)
#         return True
#     except:
#         return False

# def validate_acl(rules):
#     for rule in rules:
#         src = rule.get("src", "")
#         dst = rule.get("dst", "")
#         if src == "any" or dst == "any": continue
#         if not validate_ip(src): return False
#         if not validate_ip(dst): return False
#     return True

# def diagnostics(intent_data):
#     intent = intent_data.get("intent")
#     params = intent_data.get("params", {})
#     errors = []

#     if intent == "create_vlan":
#         if not validate_vlan(params.get("vlan_id", 0)):
#             errors.append(f"VLAN ID '{params.get('vlan_id')}' không hợp lệ.")

#     if intent == "advanced_acl":
#         if "rules" not in params: params["rules"] = []
#         if not validate_acl(params["rules"]):
#             errors.append("ACL chứa IP không hợp lệ.")
            
#     if intent == "set_interface_ip":
#         if "ip" not in params: params["ip"] = "0.0.0.0"
#         if "mask" not in params: params["mask"] = "255.255.255.0"
#         if not validate_ip(params["ip"]): errors.append(f"IP {params['ip']} lỗi.")

#     return errors