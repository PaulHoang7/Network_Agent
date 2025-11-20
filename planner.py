def plan(intent_data):

    intent = intent_data["intent"]

    mapping = {
        "create_vlan": "vlan_cisco.txt",
        "configure_vlan": "vlan_cisco.txt",   # NEW (fallback)
        "setup_ospf_advanced": "ospf_cisco_advanced.txt",
        "advanced_acl": "acl_extended.txt",
        "nat_static": "nat_static.txt",
        "nat_dynamic": "nat_dynamic.txt",
        "set_interface_ip": "interface_ip.txt",
    }

    return mapping.get(intent)
