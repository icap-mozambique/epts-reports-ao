import json

class FileUtil:

    @staticmethod
    def load_credentias():
        with open('../data/external/credentials.json', 'r') as file:
            data = json.load(file)
        return data
    
    @staticmethod
    def load_logging_config():
        with open('../resources/logging_config.json', 'r') as file:
            data = json.load(file)
        return data