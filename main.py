from intent_parser_llm import parse_intent_llm
from planner import plan
from generator import generate_from_template
from validator import diagnostics

def generate_config(user_text):

    # Step 1: dùng LLM phân tích intent
    intent_data = parse_intent_llm(user_text)

    # Step 2: validation & diagnostic
    errors = diagnostics(intent_data)
    if errors:
        return "❌ Lỗi:\n" + "\n".join(errors)

    # Step 3: chọn template phù hợp
    template_file = plan(intent_data)
    if not template_file:
        return "❌ Không tìm thấy template cho intent: " + intent_data["intent"]

    # Step 4: sinh cấu hình
    config = generate_from_template("templates/" + template_file, intent_data["params"])

    return config


# test CLI
if __name__ == "__main__":
    user = input("Nhập yêu cầu: ")
    print(generate_config(user))
