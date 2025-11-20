import re

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

    # BUILD RULE STRUCTURE (VALIDATOR COMPATIBLE)
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
