import json, requests
from bs4 import BeautifulSoup as bs4

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

        try:
            response = fetcher.get(url)
            soup = bs4(response.content, "html.parser")

            # extract lengths and their links
            extractor.extract_lengths_with_links(soup)

            # extract data for individual length
            for idx, length_link in enumerate(extractor.lengths_links):
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
                extractor.extract_colors_with_links(soup2)
                extractor.extract_product_details(soup2, content)

                # extract all colors and their links for every length
                for index, color_link in enumerate(extractor.colors_links):
                    resp3 = fetcher.get(color_link)
                    soup3 = bs4(resp3.content, "html.parser")
                    # extract data
                    extractor.extract_color_data(
                        soup3, content, extractor.colors[index], extractor.lengths[idx]
                    )
                extractor.empty_colors_list()
                extractor.empty_colors_links_list()
                data.append(content)

            extractor.empty_lengths_list()
            extractor.empty_colors_links_list()
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
