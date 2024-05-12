import csv
import json


class FileHandler:
    def __init__(self):
        pass

    def is_empty_cell(self, cell):
        if cell == "":
            return True
        return False

    def read_from_csv(self, filename):
        urls = []
        with open(filename) as csv_file:
            csv_reader = csv.reader(csv_file)

            for index, lines in enumerate(csv_reader):
                cell = lines[0]
                if index == 0 or self.is_empty_cell(cell):
                    continue
                urls.append(lines[0])

        return urls

    def write_to_json(self, filename, data):
        with open(filename, "a+") as file:
            json.dump(data, file, indent=4)
            print(f"File {filename} has been created")
        return
