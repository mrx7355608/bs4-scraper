from base_scraper import BaseScraper
from typing import List


class ProductScraper(BaseScraper):
    def __init__(self) -> None:
        super().__init__()

    def scrape(self, soup) -> dict:
        scraped_product_data = {
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
        product_name = self.scrape_name(soup)
        product_code = self.scrape_code(soup)
        product_image = self.scrape_image(soup)
        product_features = self.scrape_features(soup)
        product_categories = self.scrape_categories(soup)
        product_description = self.scrape_description(soup)
        product_specifications = self.scrape_specifications(soup)

        scraped_product_data["image_name"] = product_image
        scraped_product_data["product_code"] = product_code
        scraped_product_data["product_name"] = product_name
        scraped_product_data["category_1"] = product_categories[-2]
        scraped_product_data["category_2"] = product_categories[-1]
        scraped_product_data["product_features"] = product_features
        scraped_product_data["specifications"] = product_specifications
        scraped_product_data["product_description"] = product_description
        return scraped_product_data

    def scrape_categories(self, soup) -> List[str]:
        category_div = soup.find("div", {"class": "breadcrumb-section"})

        categories = []
        for li in category_div.ol:
            category = li.text.strip()
            if category:
                categories.append(category)
            else:
                categories.append("N/A")

        return categories

    def scrape_description(self, soup) -> str:
        description = soup.find(
            "div", {"class": "description js-product-description"}
        ).text

        if not description:
            return "N/A"

        return description.strip()

    def scrape_features(self, soup) -> List[str]:
        features = []
        features_ul = soup.find("ul", {"class": "list-unstyled lr-features-list"})
        for li in features_ul:
            li_text = self.get_text(li)
            if li_text:
                features.append(li_text)

        return features
