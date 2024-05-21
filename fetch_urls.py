import requests
import time


class FetchUrls:
    def __init__(self,  userAgent: str):
        self.session = requests.Session()
        self.user_agent = userAgent

    def get(self, url):
        time.sleep(1)

        headers = {
            "User-Agent": self.user_agent
        }
        response = self.session.get(url, headers=headers)
        return response.content
