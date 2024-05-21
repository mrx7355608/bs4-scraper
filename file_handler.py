from typing import List
import csv
import json


class FileHandler:
    def __init__(self) -> None:
        pass

    def read_urls(self) -> List[str]:
        urls = []
        with open("urls.csv") as file:
            reader = csv.reader(file)
            for index, lines in enumerate(reader):
                if index != 0 and lines[0] != "":
                    urls.append(lines[0])
        return urls

    def save_logs(self, logsList: List[str]):
        with open("logs.txt", "a+") as file:
            for logs in logsList:
                file.write(logs)
        print("[INFO] logs.txt has been created")
        return

    def save_scraped_data(self, data: List[dict]) -> None:
        with open("content.json", "a+") as file:
            json.dumps(data, file, indent=4)
            print("[INFO] content.json has been created")
        return
