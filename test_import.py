import sys
import os

print("Đang kiểm tra môi trường...")
print(f"Thư mục hiện tại: {os.getcwd()}")

try:
    print("\n1. Thử import utils...")
    import utils
    print("✅ Đã tìm thấy package 'utils'")
    
    print("\n2. Thử import parser_basic từ utils...")
    from utils import parse_acl_basic
    print("✅ THÀNH CÔNG! Import được hàm 'parse_acl_basic'")

except ImportError as e:
    print(f"\n❌ LỖI IMPORT: {e}")
    print("👉 Gợi ý: Kiểm tra lại tên file trong utils/ hoặc nội dung file __init__.py")
except Exception as e:
    print(f"\n❌ Lỗi khác: {e}")