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