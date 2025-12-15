from jinja2 import Template
import os

class GeneratorAgent:
    def generate(self, template_file, params):
        print(f"⚙️ [Agent 3] Sinh cấu hình từ {template_file}...")
        
        template_path = os.path.join("templates", template_file)
        
        if not os.path.exists(template_path):
            return None, f"Không tìm thấy file template: {template_path}"
            
        try:
            with open(template_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            template = Template(content)
            config_text = template.render(**params)
            return config_text, None
        except Exception as e:
            return None, str(e)