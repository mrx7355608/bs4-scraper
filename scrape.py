import json
import requests
from bs4 import BeautifulSoup as bs4

from data_extractor import DataExtractor
from fetch_urls import FetchUrls
from file_handler import FileHandler


extractor = DataExtractor()
fetcher = FetchUrls()
handle_files = FileHandler()

urls = handle_files.read_from_csv("urls.csv")
data = []

# with open("try.html") as file:
#     soup = bs4(file, "html.parser")
#     extractor.extract_colors_with_links(soup)
#     print(len(extractor.colors))
#     print(len(extractor.colors_links))


def main():
    counter = 0
    while counter < len(urls):
        url = urls[counter]

        try:
            print(f"\nScraping link {counter + 1}")

            response = fetcher.get(url)
            soup = bs4(response.content, "html.parser")

            # extract lengths and their links
            print("Extracting lengths...")
            extractor.extract_lengths_with_links(soup)

            if len(extractor.lengths_links) == 0:
                print("No lengths were found...")
                content2 = {
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
                extractor.extract_product_details(soup, content2)
                data.append(content2)
                counter += 1
                continue

            # extract data for individual length
            for idx, length_link in enumerate(extractor.lengths_links):
                print(f"\nExtracting colors for length: {extractor.lengths[idx]}...")
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
                if len(extractor.colors_links) == 0:
                    print("No colors were found...")
                    data.append(content)
                    continue

                for index, color_link in enumerate(extractor.colors_links):
                    print("Scraping variant...")
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

        except requests.exceptions.ConnectionError as e:
            print(f"ERROR: {e}")
            # save already scraped data
            if len(data) < 1:
                print("No data was scraped")
                break
            else:
                print("Saving already scraped data...")
                handle_files.write_to_json("scrape_fail_data.json", data)
                print(f"{counter+1} links were scraped")
                break

        except Exception as e:
            print(f"ERROR: {e}")
            # save already scraped data
            if len(data) < 1:
                print("No data was scraped")
                break
            else:
                print("Saving already scraped data...")
                handle_files.write_to_json("scrape_fail_data.json", data)
                print(f"{counter+1} links were scraped")
                break

    # save data in a data.json file
    handle_files.write_to_json("content.json", data)

    return


main()
