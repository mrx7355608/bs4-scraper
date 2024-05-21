from base_scraper import BaseScraper

class VariantScraper(BaseScraper):
    def __init__(self) -> None:
        super().__init__()

    def scrape(self, soup, length, color_name):
        color_data = {}
        variant = {
            "length": length,
            "color": {}
        }

        product_name = self.scrape_name(soup)
        product_code = self.scrape_code(soup)
        product_image = self.scrape_image(soup)
        product_specs = self.scrape_specifications(soup)
        product_price = self.scrape_price(soup)

        color_data["product_name"] = product_name
        color_data["product_code"] = product_code
        color_data["price"] = product_price
        color_data["image_name"] = product_image
        color_data["color_name"] = color_name
        color_data["specifications"] = product_specs
        variant["color"] = color_data

        return variant