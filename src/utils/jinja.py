
from jinja2 import Environment, BaseLoader

class UtilsJinja:
    def render(self, text, **kwargs):
        template = Environment(loader=BaseLoader).from_string(text)
        return template.render(**kwargs)