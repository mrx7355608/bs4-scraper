import requests
import time
from bs4 import BeautifulSoup as bs4


class FetchUrls:
    def __init__(self):
        self.session = requests.Session()

    def get_soup(self, url):
        time.sleep(1)

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        }
        response = self.session.get(url, headers=headers)
        soup = bs4(response.content, "lxml")
        return soup
