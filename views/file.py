import json
import os

class file:
    def read_from_file(filename):
        filer_name = "save.json"
        isFile = os.path.isfile(filename)
        if (not isFile):
            new_num = 0
            with open('save.json', 'w') as f:
                json.dump(new_num, f)
                print("new save.json created")
                return new_num
        else:
            with open(filer_name, "r") as file:
                data = json.load(file)
        return data

    def save_to_file(save):
        filename = "save.json"
        with open(filename, "w") as file:
            json.dump(save, file)