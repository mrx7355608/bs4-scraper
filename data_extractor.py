from bs4 import Tag


class DataExtractor:
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
            if not length:
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

        if not length_div:
            return

        # Extract li text and links for length
        for li in length_div.ul:
            length = self.get_text(li)
            if length:
                self.lengths.append(length)
                self.extract_lengths_links(li)

        return

    def extract_colors_with_links(self, soup):
        div = soup.find("div", {"class": "lr-variant-selector lr-variant-type--color"})
        if not div:
            return

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

    # Function to extract color data
    def extract_color_data(self, soup, content, color, length):
        variant = {}
        color_based_data = {}

        product_name = soup.find("h1", {"class": "name"}).text
        product_code = soup.find(
            "span", {"class": "lr-product-info--item sku js-code-switch"}
        ).text
        price = soup.find("span", {"class": "listed-price"}).text or "not available"
        image_div = soup.find("div", {"class": "lr-img-wp"})
        if image_div:
            image = image_div.find("img").get("data-src") or "not available"

        # extract specs
        specs_div = soup.find("div", {"class": "product-classifications"})

        # extract headlines
        all_headlines = soup.find_all("div", {"class": "headline"})
        headlines_list = []
        specifications = []
        for headline in all_headlines:
            headline = headline.text.strip()
            spec_headline = {}
            spec_headline[headline] = []
            headlines_list.append(headline)
            specifications.append(spec_headline)

        # extract specs tables
        all_tables = soup.find_all("table", {"class": "table"})
        for index, table in enumerate(all_tables):
            keys = table.find_all("td", {"class": "attrib"})
            for key in keys:
                value = key.find_next("td").text.strip()
                spec = {"title": key.text.strip(), "value": value}

                headline = headlines_list[index]
                specifications[index][headline].append(spec)

        color_based_data["product_name"] = product_name
        color_based_data["color_name"] = color
        color_based_data["product_code"] = product_code
        color_based_data["price"] = price.strip()
        color_based_data["image_name"] = image
        color_based_data["specifications"] = specifications
        variant["length"] = length
        variant["color"] = color_based_data
        content["variants"].append(variant)
        return

    def extract_product_details(self, soup, content):
        product_name = soup.find("h1", {"class": "name"}).text
        product_code = soup.find(
            "span", {"class": "lr-product-info--item sku js-code-switch"}
        ).text
        product_description = soup.find(
            "div", {"class": "description js-product-description"}
        ).text
        image_div = soup.find("div", {"class": "lr-img-wp"})
        image = image_div.find("img").get("data-src") or "not available"
        category_div = soup.find("div", {"class": "breadcrumb-section"})
        categories = []

        for li in category_div.ol:
            categ = li.text.strip()
            if not categ:
                continue
            else:
                categories.append(categ)
        category_1 = categories[-2]
        category_2 = categories[-1]

        features = []
        features_ul = soup.find("ul", {"class": "list-unstyled lr-features-list"})
        for li in features_ul:
            li_text = self.get_text(li)
            if li_text:
                features.append(li_text)

        # extract specs
        specs_div = soup.find("div", {"class": "product-classifications"})

        # extract headlines
        all_headlines = soup.find_all("div", {"class": "headline"})
        headlines_list = []
        specifications = []
        for headline in all_headlines:
            headline = headline.text.strip()
            spec_headline = {}
            spec_headline[headline] = []
            headlines_list.append(headline)
            specifications.append(spec_headline)

        # extract specs tables
        all_tables = soup.find_all("table", {"class": "table"})
        for index, table in enumerate(all_tables):
            keys = table.find_all("td", {"class": "attrib"})
            for key in keys:
                value = key.find_next("td").text.strip()
                spec = {"title": key.text.strip(), "value": value}

                headline = headlines_list[index]
                specifications[index][headline].append(spec)

        content["product_name"] = product_name
        content["product_code"] = product_code
        content["product_description"] = product_description.strip()
        content["product_features"] = features
        content["image_name"] = image
        content["specifications"] = specifications
        content["category_1"] = category_1
        content["category_2"] = category_2
        return

    def extract_selected_length(self, soup):
        div = soup.find("div", {"class": "lr-variant-selector lr-variant-type--text"})
        li = div.find("li", {"class": "lr-variant-item selected"})
        return li.text.strip()

    def empty_lengths_list(self):
        self.lengths = []

    def empty_lengths_links_list(self):
        self.lengths_links = []

    def empty_colors_list(self):
        self.colors = []

    def empty_colors_links_list(self):
        self.colors_links = []
