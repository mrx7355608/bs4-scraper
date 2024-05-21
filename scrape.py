import json
import requests
from bs4 import BeautifulSoup as bs4

from fetch_urls import FetchUrls
from product_scraper import ProductScraper
from variant_scraper import VariantScraper
from lengths_colors_scraper import LengthsAndColorsScraper
from file_handler import FileHandler
from event_logger import Logger

fetcher = FetchUrls()
variantScraper = VariantScraper()
productScraper = ProductScraper()
lengthsColorsScraper = LengthsAndColorsScraper()
fileHandler = FileHandler()
logger = Logger()

urls = fileHandler.read_urls()
data = []


def main():
    counter = 0
    while counter < len(urls):
        # fetch product from url
        content = fetcher.get(urls[counter])
        logger.log(f"Scraping url: {urls[counter]}")

        # check if lengths are available on that product
        # if lengths are not available, then skip the product
        # otherwise proceed
        logger.log("Extracting lengths...")
        soup_product = bs4(content, "lxml")
        lengths, links = lengthsColorsScraper.extract_lengths_with_links(soup_product)
        if len(lengths) < 1:
            logger.log("No lengths were found, skipping to next url")
            counter += 1
            continue

        colors, links = lengthsColorsScraper.extract_colors_with_links(soup_product)

        counter += 1


# main()
