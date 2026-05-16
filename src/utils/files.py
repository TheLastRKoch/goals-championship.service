import csv
from io import StringIO


class UtilFile:
    '''Utility class for file-related operations.'''

    def read_text_file(self, path):
        '''Reads a text file and returns its content.

        Args:
            path (str): The path to the text file.

        Returns:
            str: The content of the file.
        '''
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

    def write_text_file(self, path, text):
        '''Appends text to a text file.

        Args:
            path (str): The path to the text file.
            text (str): The text to append.
        '''
        with open(path, 'a', encoding='utf-8') as f:
            f.write(text)

    def json_to_csv(self, json_data):
        '''Converts JSON data to CSV format.

        Args:
            json_data (list): A list of dictionaries representing JSON data.

        Returns:
            str: The CSV formatted string.
        '''
        if not json_data:
            return ''
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=json_data[0].keys())
        writer.writeheader()
        writer.writerows(json_data)
        return output.getvalue()
