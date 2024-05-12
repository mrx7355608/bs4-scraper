import json
import requests
from bs4 import BeautifulSoup as bs4

from page_scraper import PageScraper
from fetch_urls import FetchUrls


urls = [
    "https://www.cablestogo.com/networking/data-center/0-5ft-0-15m-cat6-snagless-unshielded-utp-ethernet-network-patch-cable-green/p/cg-00954"
]
data = []

page_scraper = PageScraper()
fetcher = FetchUrls()


def main():
    counter = 0
    while counter < len(urls):
        url = urls[counter]

        try:
            response = fetcher.get(url)
            soup = bs4(response.content, "html.parser")

            # extract lengths and their links
            page_scraper.extract_lengths_with_links(soup)

            # extract data for individual length
            for idx, length_link in enumerate(page_scraper.lengths_links):
                if idx == 2:
                    break
                content = {
                    "product_name": "",
                    "product_code": "",
                    "product_description": "",
                    "category_1": "",
                    "category_2": "",
                    "product_features": [],
                    "image_name": "",
                    "variants": [],
                    "specifications": [],
                }
                resp2 = fetcher.get(length_link)
                soup2 = bs4(resp2.content, "html.parser")
                page_scraper.extract_colors_with_links(soup2)
                page_scraper.extract_product_details(soup2, content)

                # extract all colors and their links for every length
                for index, color_link in enumerate(page_scraper.colors_links):
                    resp3 = fetcher.get(color_link)
                    soup3 = bs4(resp3.content, "html.parser")
                    # extract data
                    page_scraper.extract_color_data(
                        soup3,
                        content,
                        page_scraper.colors[index],
                        page_scraper.lengths[idx],
                    )
                page_scraper.empty_colors_list()
                page_scraper.empty_colors_links_list()
                data.append(content)

            page_scraper.empty_lengths_list()
            page_scraper.empty_colors_links_list()
            counter += 1

        except requests.exceptions.RequestException as e:
            # print error message
            print(f"ERROR: {str(e)}")
            print("Trying next url")
            continue

        except requests.exceptions.ConnectionError:
            print("ERROR: Lost internet connection")
            # save already scraped data
            if len(data) < 1:
                print("No data was scraped")
            else:
                print("Saving already scraped data...")
                with open("scrape_fail_data.json", "a+") as file:
                    json.dump(data, file, indent=4)

        # save data in a data.json file
        with open("content.json", "a+") as file:
            json.dump(data, file, indent=4)

    return


main()
