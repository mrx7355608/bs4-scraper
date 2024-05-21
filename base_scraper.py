class BaseScraper:
    def __init__(self) -> None:
        pass

    def scrape_name(self, soup) -> str:
        product_name = soup.find("h1", {"class": "name"}).text
        return product_name

    def scrape_code(self, soup) -> str:
        product_code = soup.find(
            "span", {"class": "lr-product-info--item sku js-code-switch"}
        ).text
        return product_code

    def scrape_image(self, soup) -> str:
        image_div = soup.find("div", {"class": "lr-img-wp"})
        image_link = image_div.find("img").get("data-src") or "not available"
        return image_link

    def scrape_price(self, soup) -> str:
        price = (
            soup.find("span", {"class": "listed-price"}).text.strip() or "not available"
        )
        return price

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
        return specifications
