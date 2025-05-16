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

        # Define the cookies from the curl command
        cookies = {
            'pcm_consent': f'analytical%3Dtrue%26countryCode%3D{self.user_country}%26consentId%3D6b4c3162-cd3b-4909-84b3-a364dfb02f74%26consentedAt%3D2025-03-10T23%3A17%3A37.278Z%26expiresAt%3D2025-09-06T23%3A17%3A37.278Z%26implicit%3Dtrue%26marketing%3Dtrue%26regionCode%3D11%26regulation%3Dnone%26legacyRegulation%3Dnone',
            'pcm_personalization_disabled': '0',
            'cors_js': '1',
            'bkng_sso_session': 'e30',
            'bkng_sso_ses': 'e30',
            '_gcl_au': '1.1.436207334.1741648661',
            'FPID': 'FPID2.2.PibCXG13Qbhzzq2%2B4e7szSg%2Bs8P3Z%2Fp2I9r2Nn3ggcU%3D.1741648660',
            'FPAU': '1.1.436207334.1741648661',
            '_yjsu_yjad': '1741648662.90f86f40-ddc4-494a-afbe-5ecb6e38055e',
            'bkng_sso_auth': 'CAIQ0+WGHxpm6ygrJxiTLDgmWemsWtURePhUFsGUNqan4PW61B0w6clv2dRZ2JNwB2oq0ccC+5i3HNL8p5nh0Qs3VdtkFU0ptfFWpSgzy8fKVvF8ogB7dptgh96ho6h/ZiPZuaFoTkA5aL3s2dFQ',
            'BJS': '-',
            '_gid': 'GA1.2.492057804.1746957152',
            'bkng_prue': '1',
            'FPLC': 'Fh2JaumonoS7FWSis2J93Yh%2FNJbza3frXLqX6kjSXbcx8UT7BddKxlHzcDZPxbbMj7za46yMfWw7k256IymQha1CKoHE89VNjjXI4XN2qfl8rk8SqfR36cUMYzUjSg%3D%3D',
            'b': '%7B%22countLang%22%3A1%7D',
            'OptanonConsent': 'implicitConsentCountry=nonGDPR&implicitConsentDate=1741648660222&isGpcEnabled=0&datestamp=Sun+May+11+2025+12%3A51%3A03+GMT%2B0100+(Central+European+Standard+Time)&version=202501.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=e5372b17-c965-4dd5-81da-a064c361aa86&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0004%3A1&AwaitingReconsent=false',
            '_gat': '1',
            '_ga': 'GA1.1.1716958605.1741648660',
            'cgumid': 'GcNC_19mWENrV25RWUprdWlnSFltSSUyRiUyRlVjUENBdzlBMFQwR3BiZHglMkJrTk9wSlRrJTNE',
            'cto_bundle': 'mtYYh18yYkNIakl3cjNraVVsYm9BUXFuWkkzT1RidGRQMzdvWEVCMGc1Mk16M2dpbEpyaVBCMmZYNERMdVJ3Z3lWMEdVVHpOZlN3WmFQbXhmc1pvclZLY2FRNXAlMkJlSDNvWXl1WFZlVkE2T3EzT0JtOXFGS1dXTWpZU09MUUVSQThnWXFaJTJGekM5RmVRciUyQjdzSFQyZkhXb1BvTVElM0QlM0Q',
            '_ga_A12345': 'GS2.1.s1746964267$o5$g1$t1746964275$j0$l0$h725978192',
            '_uetsid': 'aa001be02e4d11f0847a3fa404710016',
            '_uetvid': 'de1deb50fe0511ef91591f1238c20085',
            'bkng': '11UmFuZG9tSVYkc2RlIyh9Yaa29%2F3xUOLbwcLxQQ4VaCrizqDMgpeZKfH1fVcT7LWqQC0aFrc1kxjboEfQtNFLnTQP0N3U5UoGgDL5jC7jnt3sx0K8Epg8fjeUOFm5IdvbUL0pKpCazuF0Mxls%2F9SUrcCOUl11b2mMU27uo8vLvPIPBX5%2BLXu4Y9dQ5MbYWo0ylj242WpPEcE%3D',
            'aws-waf-token': '8075d2b4-b074-4bd2-8cdf-b2881dea74e4:DgoAnwZTApu7AAAA:UcWgmhtebrfcN64C0TyKzVW6lvmQXeN1M/ZdplDfPaLAH3nMxqTVuXGcyqRHV1jBjKMercOvXOhb1ccEnYeGKpUp2vKMTXEJ0RMqKbwYl/sG6FUpJREboThzhbYs+goPgCAD1tmIg++c7CmV0gcSxqmW1qHo7vHJUbU3Zi2fRel6ARzQBL6yeSRmzsMp279gZCSwSb+scwpNLOBZm7Xidgn7FQ0HZzXJg67Q2MpaWiQMedn7cJ3tuCHhLcuQY2c9adU=',
            'lastSeen': '0'
        }
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