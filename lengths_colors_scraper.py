from bs4 import Tag
from typing import List


class LengthsAndColorsScraper:

    def __init__(self):
        self.BASE_URL = "https://www.cablestogo.com"

    def extract_lengths_with_links(self, soup):
        lengths = []
        lengths_links = []
        length_div = soup.find(
            "div", {"class": "lr-variant-selector lr-variant-type--text"}
        )

        for li in length_div.ul:
            # Extract length
            if self.is_valid_li(li):
                lngth = li.text.strip()
                lengths.append(lngth)

                # get link of the current length page
                anchor = li.find("a")
                if self.is_valid_anchor_tag(anchor):
                    link = anchor.get("href")
                    lengths_links.append(self.BASE_URL + link)

        return lengths, lengths_links

    def extract_colors_with_links(self, soup):
        colors = []
        colors_links = []

        colors_div = soup.find(
            "div", {"class": "lr-variant-selector lr-variant-type--color"}
        )

        if not colors_div:
            return colors, colors_links

        for li in colors_div.ul:
            if not li:
                continue

            anchor = li.find("a")
            if self.is_anchor_tag(anchor):
                color = anchor.get("title")
                color_link = anchor.get("href")

                if color_link:
                    colors.append(color)
                    colors_links.append(self.BASE_URL + color_link)

        del colors[-1]
        del colors_links[-1]

        return colors, colors_links

    def is_valid_anchor_tag(self, anchor_tag):
        if isinstance(anchor_tag, Tag) and anchor_tag.get("href"):
            return True
        else:
            return False

    def is_valid_li(self, li):
        if li:
            length = li.text.strip()
            if not length or length == "0.5 ft":
                return False
            else:
                return True
        else:
            return False
