'''JMESPath utility module.

This module provides utility functions for searching JSON data using JMESPath
expressions.
'''

import jmespath


class UtilsJMESpath:
    '''Utility class for JMESPath operations.'''

    def expression(self, query, json_data):
        '''Executes a JMESPath expression against a JSON object.

        Args:
            query (str): The JMESPath query string.
            json_data (dict or list): The JSON data to search.

        Returns:
            any: The result of the JMESPath search.
        '''
        engine = jmespath.compile(query)
        return engine.search(json_data)
