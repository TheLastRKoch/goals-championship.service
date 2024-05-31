class UtilFile:

    def read_text_file(self, path):
        with open(path) as f:
            return f.read()

    def write_text_file(self, path, text):
        with open(path, 'w') as f:
            f.write(text)
