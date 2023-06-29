import json

class file:
    def read_from_file(filename):
        filer_name = "save.json"
        with open(filer_name, "r") as file:
            data = json.load(file)
        return data

    def save_to_file(save):
        filename = "save.json"
        with open(filename, "w") as file:
            json.dump(save, file)