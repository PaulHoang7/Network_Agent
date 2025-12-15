# utils/__init__.py

from .validator import diagnostics, validate_ip, validate_vlan

# SỬA DÒNG NÀY: Dùng "parser_basic" (số ít) để khớp với tên file của bạn
from .parser_basic import (
    parse_acl_basic, 
    parse_interface_basic, 
    parse_nat_dynamic_basic
)