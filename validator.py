import ipaddress

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
    return all(str(p).isdigit() and 0 < int(p) <= 48 for p in ports)

def validate_acl(rules):
    for rule in rules:
        src = rule.get("src", "")
        dst = rule.get("dst", "")

        # any is always valid
        if src == "any" or dst == "any":
            continue

        if not validate_ip(src):
            return False
        if not validate_ip(dst):
            return False
    return True


def diagnostics(intent_data):
    intent = intent_data["intent"]
    params = intent_data["params"]
    errors = []

    # VLAN
    if intent == "create_vlan":
        if not validate_vlan(params.get("vlan_id", 0)):
            errors.append("VLAN ID không hợp lệ (1–4094).")

    # ACL
    if intent == "advanced_acl":
        # Nếu không có rules, tạo rules rỗng
        if "rules" not in params:
            params["rules"] = []
        if not validate_acl(params["rules"]):
            errors.append("ACL chứa IP không hợp lệ.")

    # OSPF
    if intent == "setup_ospf_advanced":
        if not validate_ip(params.get("router_id", "0.0.0.0")):
            errors.append("Router-ID không hợp lệ.")
    
    # Interface IP        
    if intent == "set_interface_ip":
        if "ip" not in params:
            params["ip"] = "0.0.0.0"
        if "mask" not in params:
            params["mask"] = "255.255.255.0"
        if "interface" not in params:
            params["interface"] = "g0/0"
        if "description" not in params:
            params["description"] = "NO-DESC"


    return errors

    
