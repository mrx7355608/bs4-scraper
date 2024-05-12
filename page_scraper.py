from bs4 import Tag


class PageScraper:
    BASE_URL = "https://www.cablestogo.com"

    def __init__(self):
        self.lengths_links = []
        self.lengths = []
        self.colors = []
        self.colors_links = []

    def is_valie_anchor_tag(self, anchor_tag):
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

    def extract_lengths_and_links(self, soup):
        # Parse ul of cable lengths
        length_div = soup.find(
            "div", {"class": "lr-variant-selector lr-variant-type--text"}
        )

        for li in length_div.ul:
            # Extract length
            if self.is_valid_li(li):
                lngth = li.text.strip()
                self.lengths.append(lngth)
                # get link of the current length page
                anchor = li.find("a")
                if self.is_valid_anchor_tag(anchor):
                    link = anchor.get("href")
                    self.lengths_links.append(self.BASE_URL + link)

        return

    def extract_color_links(self, soup):
        div = soup.find("div", {"class": "lr-variant-selector lr-variant-type--color"})
        for li in div.ul:
            if not li:
                continue
            anchor = li.find("a")
            if self.is_anchor_tag(anchor):
                color_title = anchor.get("title")
                href = anchor.get("href")

                if href:
                    self.colors.append(color_title)
                    self.colors_links.append(self.BASE_URL + href)

        del self.colors_links[-1]
        del self.colors[-1]

    def empty_lengths(self):
        self.lengths = []

    def empty_lengths_links(self):
        self.lengths_links = []

    def empty_colors(self):
        self.colors = []

    def empty_colors_links(self):
        self.colors_links = []
