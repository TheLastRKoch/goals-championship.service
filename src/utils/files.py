import csv
from io import StringIO

class UtilFile:

    def read_text_file(self, path):
        with open(path) as f:
            return f.read()

    def write_text_file(self, path, text):
        with open(path, 'w') as f:
            f.write(text)

    def json_to_csv(self, json):
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=json[0].keys())
        writer.writeheader()
        writer.writerows(json)
        return output.getvalue()
