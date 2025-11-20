from jinja2 import Template

def generate_from_template(template_path, data):
    with open(template_path, "r") as f:
        content = f.read()
    
    template = Template(content)
    return template.render(**data)
