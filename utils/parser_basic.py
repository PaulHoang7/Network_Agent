import re

# ==========================================
# 1. PARSER CHO ACL (Advanced Access Control List)
# ==========================================
def parse_acl_basic(text):
    text = text.lower()

    # ACTION
    action = "deny" if ("chặn" in text or "block" in text or "deny" in text) else "permit"

    # PROTOCOL
    if "tcp" in text:
        protocol = "tcp"
    elif "udp" in text:
        protocol = "udp"
    else:
        protocol = "ip"

    # SRC IP
    src = re.search(r"từ (\d+\.\d+\.\d+\.\d+)", text)
    if not src:
        src = re.search(r"from (\d+\.\d+\.\d+\.\d+)", text)
    src_ip = src.group(1) if src else "any"

    # DST IP
    dst = re.search(r"đến (\d+\.\d+\.\d+\.\d+)", text)
    if not dst:
        dst = re.search(r"to (\d+\.\d+\.\d+\.\d+)", text)
    dst_ip = dst.group(1) if dst else "any"

    # PORT
    p = re.search(r"port (\d+)", text)
    port = p.group(1) if p else "any"

    # INTERFACE
    iface = re.search(r"interface (\w+\d+\/\d+)", text)
    iface = iface.group(1) if iface else "g0/0"

    # DIRECTION
    if "in" in text or "inbound" in text:
        direction = "in"
    else:
        direction = "out"

    # BUILD RULE STRUCTURE
    rules = [{
        "action": action,
        "protocol": protocol,
        "src": src_ip,
        "src_wildcard": "0.0.0.0" if src_ip != "any" else "",
        "dst": dst_ip,
        "dst_wildcard": "0.0.0.0" if dst_ip != "any" else "",
        "port": port
    }]

    return {
        "intent": "advanced_acl",
        "params": {
            "acl_name": "ACL_AUTO",
            "rules": rules,
            "interface": iface,
            "direction": direction
        }
    }


# ==========================================
# 2. PARSER CHO INTERFACE CONFIG
# ==========================================
def parse_interface_basic(text):
    text = text.lower()

    # interface name
    iface = re.search(r"interface (\w+\d+\/\d+)", text)
    iface = iface.group(1) if iface else "g0/0"

    # ip address extraction
    # Logic: The first IP in text = interface IP, the second IP = mask
    ip_list = re.findall(r"\d+\.\d+\.\d+\.\d+", text)

    if len(ip_list) >= 2:
        ip_addr = ip_list[0]
        subnet = ip_list[1]
    else:
        ip_addr = "0.0.0.0"
        subnet = "255.255.255.0"

    # Description
    desc = re.search(r"mô tả ([\w\-]+)", text)
    if not desc:
        desc = re.search(r"description ([\w\-]+)", text)
    description = desc.group(1) if desc else "NO-DESC"

    return {
        "intent": "set_interface_ip",
        "params": {
            "interface": iface,
            "ip": ip_addr,
            "mask": subnet,
            "description": description
        }
    }


# ==========================================
# 3. PARSER CHO NAT DYNAMIC
# ==========================================
def parse_nat_dynamic_basic(text):
    text = text.lower()

    # start_ip
    start = re.search(r"pool (\d+\.\d+\.\d+\.\d+)", text)
    start_ip = start.group(1) if start else "0.0.0.0"

    # end_ip
    end = re.search(r"đến (\d+\.\d+\.\d+\.\d+)", text)
    if not end:
        end = re.search(r"to (\d+\.\d+\.\d+\.\d+)", text)
    end_ip = end.group(1) if end else start_ip

    # netmask
    mask = re.search(r"netmask (\d+\.\d+\.\d+\.\d+)", text)
    netmask = mask.group(1) if mask else "255.255.255.0"

    # acl number
    acl = re.search(r"acl (?:số )?(\d+)", text)
    acl_number = acl.group(1) if acl else "10"

    # ACL source
    acl_src = re.search(r"từ (\d+\.\d+\.\d+\.\d+)", text)
    acl_src_ip = acl_src.group(1) if acl_src else "any"

    # wildcard
    wildcard = re.search(r"wildcard (\d+\.\d+\.\d+\.\d+)", text)
    wildcard_ip = wildcard.group(1) if wildcard else "0.0.0.255"

    # ACL destination
    acl_dst = re.search(r"đến (\w+)", text)
    acl_dst_ip = "any"

    return {
        "intent": "nat_dynamic",
        "params": {
            "start_ip": start_ip,
            "end_ip": end_ip,
            "netmask": netmask,
            "acl_number": acl_number,
            "src": acl_src_ip,
            "src_wildcard": wildcard_ip,
            "dst": acl_dst_ip,
            "dst_wildcard": "",
            "protocol": "ip"
        }
    }