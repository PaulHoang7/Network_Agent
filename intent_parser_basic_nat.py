# import re

# def parse_nat_dynamic_basic(text):
#     text = text.lower()

#     # start_ip
#     start = re.search(r"pool (\d+\.\d+\.\d+\.\d+)", text)
#     start_ip = start.group(1) if start else "0.0.0.0"

#     # end_ip
#     end = re.search(r"đến (\d+\.\d+\.\d+\.\d+)", text)
#     if not end:
#         end = re.search(r"to (\d+\.\d+\.\d+\.\d+)", text)
#     end_ip = end.group(1) if end else start_ip

#     # netmask
#     mask = re.search(r"netmask (\d+\.\d+\.\d+\.\d+)", text)
#     netmask = mask.group(1) if mask else "255.255.255.0"

#     # acl number
#     acl = re.search(r"acl (?:số )?(\d+)", text)
#     acl_number = acl.group(1) if acl else "10"

#     # ACL source
#     acl_src = re.search(r"từ (\d+\.\d+\.\d+\.\d+)", text)
#     acl_src_ip = acl_src.group(1) if acl_src else "any"

#     # wildcard
#     wildcard = re.search(r"wildcard (\d+\.\d+\.\d+\.\d+)", text)
#     wildcard_ip = wildcard.group(1) if wildcard else "0.0.0.255"

#     # ACL destination
#     acl_dst = re.search(r"đến (\w+)", text)
#     acl_dst_ip = "any"

#     return {
#         "intent": "nat_dynamic",
#         "params": {
#             "start_ip": start_ip,
#             "end_ip": end_ip,
#             "netmask": netmask,
#             "acl_number": acl_number,
#             "src": acl_src_ip,
#             "src_wildcard": wildcard_ip,
#             "dst": acl_dst_ip,
#             "dst_wildcard": "",
#             "protocol": "ip"
#         }
#     }
