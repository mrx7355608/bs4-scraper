import requests
import time
import random


class FetchUrls:
    def __init__(self):
        pass

    def get(self, url):
        sleep_time = self.generate_random_number()
        time.sleep(sleep_time)

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        return response

    def generate_random_number(self):
        return random.randint(1, 2)
