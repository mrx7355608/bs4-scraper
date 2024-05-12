from bs4 import Tag


class PageScraper:
    BASE_URL = "https://www.cablestogo.com"

    def __init__(self):
        self.lengths_links = []
        self.lengths = []
        self.colors = []
        self.colors_links = []

    def is_anchor_tag(self, anchor_tag):
        if isinstance(anchor_tag, Tag):
            return True
        else:
            return False

    def get_text(self, li):
        if li:
            length = li.text.strip()
            if not length or length == "0.5 ft":
                return None
            else:
                return length
        else:
            return None

    def extract_lengths_links(self, li):
        anchor = li.find("a")
        if self.is_anchor_tag(anchor):
            link = anchor.get("href")
            if link:
                self.lengths_links.append(self.BASE_URL + link)

        return

    def extract_lengths_with_links(self, soup):
        # Parse ul of cable lengths
        length_div = soup.find(
            "div", {"class": "lr-variant-selector lr-variant-type--text"}
        )

        # Extract li text and links for length
        for li in length_div.ul:
            length = self.get_text(li)
            if length:
                self.lengths.append(length)
                self.extract_lengths_links(li)

        # last link in the below array is "javascript:void(0)"
        # so I did this to delete it
        # del self.lengths_links[-1]

        return

    def extract_colors_with_links(self, soup):
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

    def empty_lengths_list(self):
        self.lengths = []

    def empty_lengths_links_list(self):
        self.lengths_links = []

    def empty_colors_list(self):
        self.colors = []

    def empty_colors_links_list(self):
        self.colors_links = []
