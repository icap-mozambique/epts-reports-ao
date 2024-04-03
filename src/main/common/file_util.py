import json

class FileUtil:

    @staticmethod
    def load_credentias():
        with open('../data/external/credentials.json', 'r') as file:
            data = json.load(file)
        return data