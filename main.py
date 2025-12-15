# from intent_parser_llm import parse_intent_llm
# from planner import plan
# from generator import generate_from_template
# from validator import diagnostics

# def generate_config(user_text):

#     # Step 1: dùng LLM phân tích intent
#     intent_data = parse_intent_llm(user_text)

#     # Step 2: validation & diagnostic
#     errors = diagnostics(intent_data)
#     if errors:
#         return "❌ Lỗi:\n" + "\n".join(errors)

#     # Step 3: chọn template phù hợp
#     template_file = plan(intent_data)
#     if not template_file:
#         return "❌ Không tìm thấy template cho intent: " + intent_data["intent"]

#     # Step 4: sinh cấu hình
#     config = generate_from_template("templates/" + template_file, intent_data["params"])

#     return config


# # test CLI
# if __name__ == "__main__":
#     user = input("Nhập yêu cầu: ")
#     print(generate_config(user))

import os
import sys
import logging
from dotenv import load_dotenv
from core.pipeline import NetworkRAGPipeline

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load .env
load_dotenv()

def main():
    if not os.getenv("GEMINI_KEYS") and not os.getenv("GEMINI_API_KEY"):
        logger.error("❌ Chưa cấu hình GEMINI_KEYS trong file .env")
        sys.exit(1)

    try:
        logger.info("🚀 Đang khởi tạo Network Agent Pipeline...")
        pipeline = NetworkRAGPipeline()
        logger.info("✅ Hệ thống sẵn sàng!")

        print("\n" + "="*50)
        print("🌐 NETWORK AGENT CLI (Gõ 'exit' để thoát)")
        print("="*50 + "\n")

        while True:
            try:
                user_input = input("\nUser >> ").strip()
                if user_input.lower() in ["exit", "quit"]:
                    print("Tạm biệt! 👋")
                    break
                
                if not user_input:
                    continue

                print("⏳ Agent đang xử lý...")
                response = pipeline.run(user_input)
                
                print(f"\n🤖 Assistant:\n{response}")
                print("-" * 50)

            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.error(f"Lỗi runtime: {e}")

    except Exception as e:
        logger.critical(f"Không thể khởi động hệ thống: {e}")

if __name__ == "__main__":
    main()