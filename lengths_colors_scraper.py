from bs4 import Tag


class LengthsAndColorsScraper:

    def __init__(self):
        self.BASE_URL = "https://www.cablestogo.com"

    def extract_lengths_with_links(self, soup):
        details = {"lengths": [], "lengths_links": []}
        length_div = soup.find(
            "div", {"class": "lr-variant-selector lr-variant-type--text"}
        )

        for li in length_div.ul:
            # Extract length
            if self.is_valid_li(li):
                lngth = li.text.strip()
                details["lengths"].append(lngth)

                # get link of the current length page
                anchor = li.find("a")
                if self.is_valid_anchor_tag(anchor):
                    link = anchor.get("href")
                    details["lengths_links"].append(self.BASE_URL + link)

        return details

    def extract_colors_with_links(self, soup):
        variants_details = {"colors": [], "colors_links": []}
        colors_div = soup.find(
            "div", {"class": "lr-variant-selector lr-variant-type--color"}
        )

        if not colors_div:
            return None

        for li in colors_div.ul:
            if not li:
                continue

            anchor = li.find("a")
            if self.is_anchor_tag(anchor):
                color = anchor.get("title")
                color_link = anchor.get("href")

                if color_link:
                    variants_details["colors"].append(color)
                    variants_details["colors_links"].append(self.BASE_URL + color_link)

        del variants_details["colors"][-1]
        del variants_details["colors_links"][-1]

        return variants_details

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
