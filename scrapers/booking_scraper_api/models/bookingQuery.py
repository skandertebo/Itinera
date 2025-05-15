from dataclasses import dataclass

@dataclass
class BookingQuery:
    search_string: str
    checkin_date: str
    checkout_date: str
    number_of_adults: int = 1
    number_of_children: int = 0
    number_of_rooms: int = 1
    language: str = "en-gb"
    currency: str = "GBP"
    user_country: str = "UK"
