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
        try:
            # fetch product from url
            logger.log(f"Scraping url: {urls[counter]}")
            product_soup = fetcher.get_soup(urls[counter])

            # ********************************
            #     Scrape product lengths
            # ********************************
            logger.log("Extracting lengths...")
            lengths, lengths_links = lengthsColorsScraper.extract_lengths_with_links(
                product_soup
            )
            if len(lengths) < 1:
                logger.log("No lengths were found, skipping to next url")
                counter += 1
                continue

            # *****************************
            #    Scrape current product
            # *****************************
            product = productScraper.scrape(product_soup)

            # Remove length of currently scraped product from the list
            current_length = lengthsColorsScraper.extract_selected_length(product_soup)
            lengths.remove(current_length)

            # ********************************
            #     Scrape product colors
            # ********************************
            logger.log("Extracting colors...")
            colors, colors_links = lengthsColorsScraper.extract_colors_with_links(
                product_soup
            )

            # ******************************************
            #   Scrape all variants of current product
            # ******************************************
            if len(colors) > 0:
                all_variants = variantScraper.scrape_all_variants(
                    current_length, colors_links, colors
                )
                product["variants"] = all_variants
            else:
                # add scraped product in data list
                data.append(product)

            # *****************************************
            #     Scrape all variants on each length
            # *****************************************
            for index, link in enumerate(lengths_links):
                current_len = lengths[index]
                logger.log(f"Scraping length: {current_len}")
                length_soup = fetcher.get_soup(link)
                length_product = productScraper.scrape(length_soup)
                colors2, colors_links2 = lengthsColorsScraper.extract_colors_with_links(
                    length_soup
                )
                all_variants = variantScraper.scrape_all_variants(
                    current_len, colors_links2, colors2
                )
                length_product["variants"] = all_variants
                data.append(length_product)

            counter += 1

        except requests.exceptions.ConnectionError as e:
            break

        except requests.exceptions.RequestException as e:
            counter += 1
            continue


# main()
