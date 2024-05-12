class ProductScraper:
    def __init__(self):
        pass

    def scrape_specifications(self, soup):
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

    def scrape_name(self, soup):
        product_name = soup.find("h1", {"class": "name"}).text
        return product_name

    def scrape_code(self, soup):
        product_code = soup.find(
            "span", {"class": "lr-product-info--item sku js-code-switch"}
        ).text
        return product_code

    def scrape_image(self, soup):
        image_div = soup.find("div", {"class": "lr-img-wp"})
        image_link = image_div.find("img").get("data-src") or "not available"
        return image_link

    def scrape_price(self, soup):
        price = (
            soup.find("span", {"class": "listed-price"}).text.strip() or "not available"
        )
        return price

    def extract_color_data(self, soup, content, color, length):
        variant = {}
        color_based_data = {}

        name = self.scrape_name(soup)
        code = self.scrape_code(soup)
        price = self.scrape_price(soup)
        image = self.scrape_image(soup)
        specifications = self.scrape_specifications(soup)

        color_based_data["product_name"] = name
        color_based_data["color_name"] = color
        color_based_data["product_code"] = code
        color_based_data["price"] = price
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
