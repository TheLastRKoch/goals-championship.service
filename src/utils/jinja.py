'''Jinja utility module.

This module provides utility functions for rendering strings as Jinja templates.
'''

from jinja2 import Environment, BaseLoader


class UtilsJinja:
    '''Utility class for Jinja operations.'''

    def render(self, text, **kwargs):
        '''Renders a string as a Jinja template with provided keyword arguments.

        Args:
            text (str): The template string to render.
            **kwargs: The variables to use in the template.

        Returns:
            str: The rendered template string.
        '''
        template = Environment(loader=BaseLoader).from_string(text)
        return template.render(**kwargs)
