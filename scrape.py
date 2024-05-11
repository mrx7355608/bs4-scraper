import requests
import time
import json
from bs4 import BeautifulSoup as bs4
from requests.exceptions import ConnectTimeout, ConnectionError
from urllib3.exceptions import ProtocolError

from data_extractor import DataExtractor
from fetch_urls import FetchUrls


extractor = DataExtractor()
fetcher = FetchUrls()

urls = [
    "https://www.cablestogo.com/networking/data-center/0-5ft-0-15m-cat6-snagless-unshielded-utp-ethernet-network-patch-cable-green/p/cg-00954"
]
data = []

# with open("./try.html") as file:
#     soup = bs4(file, "html.parser")
#     content = {
#         "product_name": "",
#         "product_code": "",
#         "product_description": "",
#         "product_features": [],
#         "image_name": "",
#         "variants": [],
#         "specifications": [],
#     }
#     extractor.extract_product_details(soup, content)
#     print(json.dumps(content, indent=4))


def main():
    counter = 0
    while counter < len(urls):
        url = urls[counter]
        response = fetcher.get(url)
        soup = bs4(response.content, "html.parser")
        extractor.extract_lengths_with_links(soup)

        # extract lengths and their links
        for idx, length_link in enumerate(extractor.lengths_links):
            if idx == 2:
                break
            content = {
                "product_name": "",
                "product_code": "",
                "product_description": "",
                "product_features": [],
                "image_name": "",
                "variants": [],
                "specifications": [],
            }
            resp2 = fetcher.get(length_link)
            soup2 = bs4(resp2.content, "html.parser")
            extractor.extract_colors_with_links(soup2)
            extractor.extract_product_details(soup2, content)

            # extract all colors and their links for every length
            for index, color_link in enumerate(extractor.colors_links):
                resp3 = fetcher.get(color_link)
                soup3 = bs4(resp3.content, "html.parser")
                # extract data
                extractor.extract_color_data(soup3, content, extractor.colors[index])
            extractor.empty_colors_list()
            extractor.empty_colors_links_list()
            data.append(content)

        extractor.empty_lengths_list()
        extractor.empty_colors_links_list()
        counter += 1

        # save data in a data.json file
        with open("content.json", "a+") as file:
            json.dump(data, file, indent=4)

    return


main()


# Main scraping process
# response = requests.get("")
# if response.ok:
#     soup = bs4(response.content, "html.parser")
#     extract_lengths(soup)
#
#     counter = 0
#     while counter != len(lengths_links):
#         content = {'length': "", 'colors': []}
#         content["length"] = lengths[counter]
#
#         resp = requests.get(lengths_links[counter], timeout=10)
#         if resp.ok:
#             soup = bs4(resp.content, "html.parser")
#             extract_colors(soup)
#
#             counter2 = 0
#             while counter2 != len(colors_links):
#                 retries = 3
#                 delay = 1
#                 while retries > 0:
#                     try:
#                         print(f"Extracting data for:\nLength: {lengths[counter]}\nColor: {colors[counter2]}")
#                         resp2 = requests.get(colors_links[counter2], timeout=10)
#                         if resp2.ok:
#                             soup2 = bs4(resp2.content, "html.parser")
#                             extract_color_data(soup2, content, counter2)
#                             break
#                         else:
#                             print(f"Failed to retrieve data for URL: {colors_links[counter2]}")
#                     except (ConnectTimeout, ConnectionError, ProtocolError) as e:
#                         print(f"Connection error occurred: {e}")
#                     retries -= 1
#                     time.sleep(delay)
#                     delay *= 2
#                 counter2 += 1
#
#             data.append(content)
#             colors_links = []
#             counter += 1
#         else:
#             print(f"Failed to retrieve data for URL: {lengths_links[counter]}")
#
# else:
#     print("Failed to retrieve initial page data.")
#
