import pickle
import threading
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.support import expected_conditions as EC


class HotelDetailsThreadScraper(threading.Thread):
    """ Represents the "unit of work" for the scraping operation
    processes a single hotel page in an individual thread
    """
    hotels_result = []
    def __init__(self, url, name, user_country, language: str):
        threading.Thread.__init__(self)
        self.url = url
        self.name = name
        self.user_country = user_country,
        self.language = language
    
    def scrape_page(self):
        print(f"⌛️ Started Processing {self.name}");
        iso_lang_code = self.language.split('-')[-1];
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': f'{self.language},{iso_lang_code};q=0.9,ar;q=0.8,fr;q=0.7',
            'cache-control': 'no-cache',
            'priority': 'u=0, i',
            'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
        }
        # load cookies
        selenium_cookies = pickle.load(open("temp/cookies.pkl", "rb"))
        cookies = {cookie['name']: cookie['value'] for cookie in selenium_cookies}
        response = requests.get(self.url, headers=headers, cookies=cookies)
        html_content = response.text

        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract overall rating
        rating_element = soup.find(id="js--hp-gallery-scorecard")
        overall_rating = rating_element['data-review-score'] if rating_element else "Rating not found"

        # Extract hotel description
        description_element = soup.find(attrs={"data-testid": "property-description"})
        description = description_element.text if description_element else "Description not found"

        # Extract most popular facilities
        facilities_wrapper = soup.find(attrs={"data-testid": "property-most-popular-facilities-wrapper"})
        facilities_list = facilities_wrapper.find("ul") if facilities_wrapper else None
        facilities = [item.find(class_="f6b6d2a959").text for item in facilities_list.find_all("li")] if facilities_list else []

        # Extract surroundings
        surroundings_section = soup.find(attrs={"data-testid": "property-section--content"})
        poi_blocks = surroundings_section.find_all(attrs={"data-testid": "poi-block"}) if surroundings_section else []
        surroundings = {}
        for poi_block in poi_blocks:
            category_name = poi_block.find("h3").text
            ul = poi_block.find("ul")
            li_items = ul.find_all("li") if ul else []
            category_items = []
            for li in li_items:
                name = li.find(class_="aa225776f2 ca9d921c46 d1bc97eb82").text
                distance = li.find(class_="b99b6ef58f fb14de7f14 a0a56631d6").text
                category_items.append({"name": name, "distance": distance})
            surroundings[category_name] = category_items

        # Extract detailed ratings
        def has_first_child_testid(tag):
            # get a list of children, skip over strings/newlines
            children = [c for c in tag.contents if getattr(c, 'attrs', None) is not None]
            if not children:
                return False
            first = children[0]
            return first.attrs.get("data-testid") == "ReviewSubscoresDesktop"

        # find the parent tags (e.g. div) for which the first element-child matches
        parents = soup.find_all(has_first_child_testid)
        review_group = parents[0]
        subscore_divs = review_group.find_all(attrs={"data-testid": "review-subscore"}) if review_group else []
        detailed_ratings = {}
        for subscore in subscore_divs:
            category = subscore.find(class_="d96a4619c0").text.strip()
            score = subscore.find(class_="a9918d47bf f87e152973").text
            detailed_ratings[category] = score

        # Placeholder for pricing (assumes a table with id="hprt-table")
        pricing = []
        table = soup.find(id="hprt-table")
        if table:
            rows = table.find("tbody").find_all("tr")
            for row in rows:
                # Extract room type
                room_type_th = row.find("th", class_="hprt-table-cell-roomtype")
                if room_type_th:
                    room_type_span = room_type_th.find("span", class_="hprt-roomtype-icon-link")
                    room_type = room_type_span.text.strip() if room_type_span else "Room type not found"
                else:
                    room_type = "Room type not found"
                
                # Extract price
                price_td = row.find("td", class_="hprt-table-cell-price")
                if price_td:
                    price_div = price_td.find("div", class_="bui-price-display__value")
                    price = price_div.text.strip() if price_div else "Price not found"
                else:
                    price = "Price not found"
                
                pricing.append({"room_type": room_type, "price": price})
        else:
            pricing = []
        
        print(f"✅ Done Processing {self.name}");
        return {
        "name": self.name,
        "url": self.url,
        "rating": overall_rating,
        "description": description,
        "facilities": facilities,
        "surroundings": surroundings,
        "detailed_ratings": detailed_ratings,
        "pricing": pricing
        }

    def run(self):
        result = self.scrape_page();
        self.hotels_result.append(result);