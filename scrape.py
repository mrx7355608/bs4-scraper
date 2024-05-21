import requests
from bs4 import BeautifulSoup as bs4
import lxml


from data_extractor import DataExtractor
from fetch_urls import FetchUrls
from file_handler import FileHandler


extractor = DataExtractor()
fetcher = FetchUrls()
handle_files = FileHandler()

urls = handle_files.read_from_csv("urls.csv")
data = []
logs=[]

# with open("try.html") as file:
#     soup = bs4(file, "lxml")
#     extractor.extract_selected_length(soup)


def scrape_variants(content, length):
    for index, color_link in enumerate(extractor.colors_links):
        print("Scraping color...")
        logs.append("Scraping color...")

        resp3 = fetcher.get(color_link)
        soup3 = bs4(resp3.content, "lxml")
        # extract data
        extractor.extract_color_data(soup3, content, extractor.colors[index], length)
        
        print("Variant scraped...")
        logs.append("Variant scraped...")

    extractor.empty_colors_list()
    extractor.empty_colors_links_list()
    data.append(content)


def main():
    counter = 0
    while counter < len(urls):
        url = urls[counter]

        try:
            print(f"\nScraping url: {url}")
            logs.append(f"\nScraping url: {url}")

            response = fetcher.get(url)
            soup = bs4(response.content, "lxml")
            extractor.empty_lengths_list()
            extractor.empty_lengths_links_list()

            # extract lengths and their links
            print("Extracting lengths...")
            logs.append("Extracting lengths...")
            extractor.extract_lengths_with_links(soup)

            if len(extractor.lengths) < 1:
                print("No lengths were found, skipping to next url...")
                logs.append("No lengths were found, skipping to next url...")
                counter += 1
                continue

            # extract current product with its variants
            selected_length = extractor.extract_selected_length(soup)
            print(f"Extracting colors for length: {selected_length}")
            logs.append(f"Extracting colors for length: {selected_length}")
            extractor.extract_colors_with_links(soup)

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
            if len(extractor.colors_links) > 0:
                extractor.extract_product_details(soup, content2)
                scrape_variants(content2, selected_length)
                extractor.lengths.remove(selected_length)
            else:
                extractor.extract_product_details(soup, content2)
                extractor.lengths.remove(selected_length)
                data.append(content2)
                print("No colors were found")
                logs.append("No colors were found")

            # extract data for individual length
            for idx, length_link in enumerate(extractor.lengths_links):
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
                soup2 = bs4(resp2.content, "lxml")
                
                print(f"\nExtracting colors for length: {extractor.lengths[idx]}...")
                logs.append(f"\nExtracting colors for length: {extractor.lengths[idx]}...")

                extractor.extract_colors_with_links(soup2)
                extractor.extract_product_details(soup2, content)

                # extract all colors and their links for every length
                if len(extractor.colors_links) < 1:
                    print("No colors were found...")
                    logs.append("No colors were found...")
                    data.append(content)
                    continue
                else:
                    scrape_variants(content, extractor.lengths[idx])

            extractor.empty_lengths_list()
            extractor.empty_colors_links_list()
            counter += 1

        except requests.exceptions.RequestException as e:
            # print error message
            print(f"ERROR: {str(e)}")
            logs.append(f"ERROR: {str(e)}")
            print("Trying next url")
            logs.append("Trying next url")
            counter += 1
            continue

        except requests.exceptions.ConnectionError as e:
            print(f"ERROR: {str(e)}")
            logs.append(f"ERROR: {str(e)}")
            # save already scraped data
            if len(data) < 1:
                print("No data was scraped")
                logs.append("No data was scraped")
                break
            else:
                print("Saving already scraped data...")
                logs.append("Saving already scraped data...")
                handle_files.write_to_json(f"scrape_fail_data_{counter+1}.json", data)
                print(f"{counter+1} links were scraped")
                logs.append(f"{counter+1} links were scraped")
                break

        except Exception as e:
            print(f"ERROR: {str(e)}")
            logs.append(f"ERROR: {str(e)}")
            # save already scraped data
            if len(data) < 1:
                print("No data was scraped")
                logs.append("No data was scraped")
                break
            else:
                print("Saving already scraped data...")
                logs.append("Saving already scraped data...")
                handle_files.write_to_json(f"scrape_fail_data_{counter+1}.json", data)
                print(f"{counter+1} links were scraped")
                logs.append(f"{counter+1} links were scraped")
                break

        # save data in a data.json file
        handle_files.write_to_json("content.json", data)
        logs.append("Created content.json file")
        data = []

        handle_files.write_logs(logs)
        print("log file created")

    return


main()
