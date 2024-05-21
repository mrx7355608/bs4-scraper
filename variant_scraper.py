from base_scraper import BaseScraper
from fetch_urls import FetchUrls
from event_logger import Logger


class VariantScraper(BaseScraper):
    def __init__(self) -> None:
        super().__init__()
        self.fetcher = FetchUrls()
        self.logger = Logger()

    def scrape_all_variants(self, length, colors_links, colors):
        all_variants = []

        for index, link in colors_links:
            # get soup of the link's html
            self.logger.log(f"Scraping variant: {colors[index]}")
            soup = self.fetcher.get_soup(link)

            # scrape
            color_data = {}
            variant = {"length": length, "color": {}}

            product_name = self.scrape_name(soup)
            product_code = self.scrape_code(soup)
            product_image = self.scrape_image(soup)
            product_specs = self.scrape_specifications(soup)
            product_price = self.scrape_price(soup)
            color_name = colors[index]

            # create an object containing all details of the variant
            color_data["product_name"] = product_name
            color_data["product_code"] = product_code
            color_data["price"] = product_price
            color_data["image_name"] = product_image
            color_data["color_name"] = color_name
            color_data["specifications"] = product_specs

            # Save variant object in all_variants list
            variant["color"] = color_data
            all_variants.append(variant)
            self.logger.log(f"Completed")

        return all_variants
