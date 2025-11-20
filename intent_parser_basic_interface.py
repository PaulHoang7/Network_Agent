import re

def parse_interface_basic(text):
    text = text.lower()

    # interface name
    iface = re.search(r"interface (\w+\d+\/\d+)", text)
    iface = iface.group(1) if iface else "g0/0"

    # ip address
    ip = re.search(r"(\d+\.\d+\.\d+\.\d+)", text)
    mask = re.search(r"(\d+\.\d+\.\d+\.\d+)(?!.*\d)", text)

    # The first IP in text = interface IP
    # The second IP in text = mask
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
