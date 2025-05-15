from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from core.utils import generate_booking_url, save_file


class HotelsListScraper:
    """Opens a browser and extracts the hotel list based on the search input
    The purpose of running this on a browser is to perform the endless scroll on javascript.
    """
    def __init__(self, ss: str,
    checkin: str,
    checkout: str,
    group_adults: int = 1,
    group_children: int = 0,
    no_rooms: int = 1,
    lang: str = "en-gb",
    currency: str = "GBP",
    ):
        self.driver = webdriver.Chrome()
        self.url = generate_booking_url(ss, checkin, checkout, group_adults, group_children, no_rooms, lang, currency)

    def scroll_to_bottom(self, pause_time=1):
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(pause_time)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                print("✅ Reached the bottom of the page.")
                break
            last_height = new_height

    def click_all_load_more(self, max_clicks=3):
        clicks = 0
        while clicks < max_clicks:
            self.scroll_to_bottom(pause_time=1)
            try:
                button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[contains(., "Load more results")]'))
                )
                button.click()
                clicks += 1
                print(f"🔁 Clicked 'Load more results' button ({clicks})")
                time.sleep(2)
            except:
                print("❌ No more 'Load more results' button found.")
                break
        print(f"🔢 Total 'Load more results' button clicks: {clicks}")

    def close(self):
        self.driver.quit()

    def get_hotel_info(self):
        self.driver.get(self.url)
        self.scroll_to_bottom()
        self.click_all_load_more()

        property_cards = self.driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="property-card"]')

        hotels_list = []

        for property in property_cards:
            try:
                name = property.find_element(By.CSS_SELECTOR, 'div[data-testid="title"]').text.strip()
                link = property.find_element(By.CSS_SELECTOR, 'a[data-testid="title-link"]').get_attribute('href')
                review_block = property.find_element(By.CSS_SELECTOR, 'div[data-testid="review-score"]').text.strip()

                lines = review_block.split('\n')
                num_reviews = int(lines[-1].split()[0])

                if num_reviews < 20: # don't take smaller than 20 reviews
                    continue

                hotels_list.append({"name": name, "link": link})

            except Exception:
                continue

        self.driver.quit()

        return hotels_list


if __name__ == "__main__":
    try:
        scraper = HotelsListScraper(ss="Oran, Algeria, Beach View",
          checkin="2025-08-10",
          checkout="2025-09-30",
          group_adults=1,
          group_children=0,
          no_rooms=1,
          lang="en-gb",
          currency="GBP");
        hotels_list = scraper.get_hotel_info()
        save_file(hotels_list, 'testData/hotels_list/test_data.json')
    except Exception as e:
        print(f"❌ Failed: {e}")



