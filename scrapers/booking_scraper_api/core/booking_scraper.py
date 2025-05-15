
from core.hotel_details_scraper import HotelDetailsScraper
from core.hotel_list_scraper import HotelsListScraper
from models.bookingQuery import BookingQuery


class BookingScraper:
    def __init__(self, query: BookingQuery):
      self.hotels_list_scraper = HotelsListScraper(ss=query.search_string,
                                                   checkin=query.checkin_date,
                                                   checkout=query.checkout_date, 
                                                   group_adults=query.number_of_adults,
                                                   group_children=query.number_of_children,
                                                   no_rooms=query.number_of_rooms,
                                                   lang=query.language,
                                                   currency=query.currency)
      self.hotel_details_scraper = HotelDetailsScraper(user_country=query.user_country, language=query.language)
      
    def scrape(self):
      hotels_list = self.hotels_list_scraper.get_hotel_info()
      result = self.hotel_details_scraper.scrape_hotels(hotels_list=hotels_list)
      
      return result