import json
import pickle
import re
import threading
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, parse_qs


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
        
        session = requests.Session()
        response = session.get(self.url, headers=headers, cookies=cookies)
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
        "pricing": pricing,
        "reviews": self.get_reviews(soup=soup, hotel_page_url=self.url, cookies=cookies, session=session)
        }

    from urllib.parse import urlparse, parse_qs

    def get_reviews(self, soup, hotel_page_url, cookies, session):
        # Extract country code from URL path (e.g., '/hotel/dz/' -> 'dz')
        path_parts = urlparse(hotel_page_url).path.split('/')
        country_code = path_parts[2] if len(path_parts) > 2 else 'unknown'
        hotel_id = None
        ufi = None
        csrf_token = None
        
        # Extract all scripts
        scripts = soup.find_all('script', type='text/javascript')
        for script in scripts:
            if script.string and 'window.utag_data' in script.string:
                script_text = script.string
                break
        else:
            raise ValueError("Could not find script with window.utag_data")
        
        # Extract hotel_id and ufi using regex
        hotel_id_match = re.search(r"hotel_id\s*:\s*['\"]?(\d+)['\"]?", script_text)
        ufi_match = re.search(r"dest_ufi\s*:\s*['\"]?(-?\d+)['\"]?", script_text)
        cc_match = re.search(r"dest_cc\s*:\s*['\"]([a-zA-Z]{2})['\"]", script_text)
        
        if not hotel_id_match or not ufi_match or not cc_match:
            raise ValueError("Could not extract hotel_id, ufi, or country_code from script")
        
        hotel_id = int(hotel_id_match.group(1))  # e.g., 5415065
        ufi = int(ufi_match.group(1))            # e.g., -3715584
        country_code = cc_match.group(1)    
        # Extract CSRF token from meta tag (assumed name, adjust if different)
        csrf_meta = soup.find('meta', {'name': 'csrf-token'})
        csrf_token = csrf_meta['content'] if csrf_meta else None
        
        
        if not csrf_token:
            # CSRF token might be critical; proceed and adjust if request fails
            csrf_token = ''
        
        # Construct GraphQL variables
        variables = {
            "shouldShowReviewListPhotoAltText": True,
            "input": {
                "hotelId": hotel_id,
                "ufi": ufi,
                "hotelCountryCode": country_code,
                "sorter": "MOST_RELEVANT",
                "filters": {"text": ""},
                "skip": 0,
                "limit": 10,
                "hotelScore": 0,  # Optional, set to 0 if unknown
                "upsortReviewUrl": "",
                "searchFeatures": {
                    "destId": ufi,
                    "destType": "CITY"
                }
            }
        }
        
        # GraphQL query from the curl request
        query = """
        query ReviewList($input: ReviewListFrontendInput!, $shouldShowReviewListPhotoAltText: Boolean = false) {
        reviewListFrontend(input: $input) {
            ... on ReviewListFrontendResult {
            ratingScores {
                name
                translation
                value
                ufiScoresAverage {
                ufiScoreLowerBound
                ufiScoreHigherBound
                __typename
                }
                __typename
            }
            topicFilters {
                id
                name
                isSelected
                translation {
                id
                name
                __typename
                }
                __typename
            }
            reviewScoreFilter {
                name
                value
                count
                __typename
            }
            languageFilter {
                name
                value
                count
                countryFlag
                __typename
            }
            timeOfYearFilter {
                name
                value
                count
                __typename
            }
            customerTypeFilter {
                count
                name
                value
                __typename
            }
            reviewCard {
                reviewUrl
                guestDetails {
                username
                avatarUrl
                countryCode
                countryName
                avatarColor
                showCountryFlag
                anonymous
                guestTypeTranslation
                __typename
                }
                bookingDetails {
                customerType
                roomId
                roomType {
                    id
                    name
                    __typename
                }
                checkoutDate
                checkinDate
                numNights
                stayStatus
                __typename
                }
                reviewedDate
                isTranslatable
                helpfulVotesCount
                reviewScore
                textDetails {
                title
                positiveText
                negativeText
                textTrivialFlag
                lang
                __typename
                }
                isApproved
                partnerReply {
                reply
                __typename
                }
                positiveHighlights {
                start
                end
                __typename
                }
                negativeHighlights {
                start
                end
                __typename
                }
                editUrl
                photos {
                id
                urls {
                    size
                    url
                    __typename
                }
                kind
                mlTagHighestProbability @include(if: $shouldShowReviewListPhotoAltText)
                __typename
                }
                __typename
            }
            reviewsCount
            sorters {
                name
                value
                __typename
            }
            __typename
            }
            ... on ReviewsFrontendError {
            statusCode
            message
            __typename
            }
            __typename
        }
        }
        """
        
        # Headers from the curl request
        headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9,ar;q=0.8,fr;q=0.7",
            "apollographql-client-name": "b-property-web-property-page_rust",
            "apollographql-client-version": "YBTbEQJL",
            "content-type": "application/json",
            "origin": "https://www.booking.com",
            "referer": hotel_page_url,
            "sec-ch-ua": '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
            "x-apollo-operation-name": "ReviewList",
            "x-booking-context-action": "hotel",
            "x-booking-context-action-name": "hotel",
            "x-booking-csrf-token": csrf_token,
            "x-booking-dml-cluster": "rust",
            "x-booking-site-type-id": "1",
            "x-booking-timeout-ms": "4000",
            "x-booking-topic": "capla_browser_b-property-web-property-page",
            "x-envoy-upstream-rq-timeout-ms": "4000",
        }
        
        # Extract aid from URL for consistency
        query_params = parse_qs(urlparse(hotel_page_url).query)
        aid = query_params.get('aid', ['304142'])[0]  # Default from example URL
        
        # GraphQL endpoint with minimal query parameters
        graphql_url = f"https://www.booking.com/dml/graphql?aid={aid}&lang=en-gb"
        
        # Payload
        payload = {
            "operationName": "ReviewList",
            "variables": variables,
            "extensions": {},
            "query": query
        }
        
        # Make POST request
        response = session.post(graphql_url, headers=headers, cookies=cookies, json=payload)
        response.raise_for_status()
        
        return self.extract_reviews(response.json())

    def extract_reviews(self, response):
        """
        Extracts negative and positive text from each review in the JSON response.

        Args:
            response (dict): The JSON response containing review data.

        Returns:
            list: A list of dictionaries, each containing 'negativeText' and 'positiveText' from a review.
        """
        # Access the reviewCard array
        review_cards = response["data"]["reviewListFrontend"]["reviewCard"]
        
        # Initialize result list
        result = []
        
        # Iterate through each review
        for review in review_cards:
            # Safely get textDetails, default to empty dict if missing
            text_details = review.get("textDetails", {})
            
            # Extract negativeText and positiveText, default to None if not present
            negative_text = text_details.get("negativeText")
            positive_text = text_details.get("positiveText")
            title = text_details.get("title")
            
            # Append dictionary to result
            result.append({
                "title": title,
                "negativeText": negative_text,
                "positiveText": positive_text
            })
        
        return result
    def run(self):
        result = self.scrape_page();
        self.hotels_result.append(result);