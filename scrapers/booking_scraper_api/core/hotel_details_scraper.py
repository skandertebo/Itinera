from hotel_details_scraper_thread import HotelDetailsThreadScraper
from utils import read_file, save_file


class HotelDetailsScraper():
    """ Scrapes the individual hotel pages to extract useful data such as 
    - description
    - detailed_ratings: {
        Cleanliness
        Comfort
        Facilities
        Location
        Staff
        Value for money
    }
    - facilities
    - name
    - pricing
    - rating
    - surroundings
    """
    def __init__(self, user_country, language):
        """ Initiates this class

        Args:
            user_country (str): the user country, used to query bookings based on user location and currency
            language (str): the language to query bookings with
        """
        self.user_country = user_country
        self.language = language
        
    def scrape_hotels(self, hotels_list):
        threads = []
        for hotel in hotels_list:
            t = HotelDetailsThreadScraper(hotel["link"], hotel["name"], self.user_country, self.language)
            threads.append(t)
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        return HotelDetailsThreadScraper.hotels_result
    
if __name__ == "__main__":
    try:
        hotels_list = read_file('testData/hotels_list/test_data.json')
        scraper = HotelDetailsScraper(user_country="UK", language="en-US")
        result = scraper.scrape_hotels(hotels_list=hotels_list);
        save_file(result, 'testData/hotels_details/test_data.json')
    except Exception as e:
        print(f"❌ Failed: {e}")