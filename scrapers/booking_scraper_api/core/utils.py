import os
from pathlib import Path
from urllib.parse import urlencode, urlunparse

from flask import json

def generate_booking_url(
    ss: str,
    checkin: str,
    checkout: str,
    group_adults: int = 1,
    group_children: int = 0,
    no_rooms: int = 1,
    lang: str = "en-gb",
    currency: str = "GBP"
) -> str:
    """
    Generate a Booking.com search URL with dynamic query parameters.

    :param ss: Search string (e.g. "Oran")
    :param checkin: Check-in date in YYYY-MM-DD format
    :param checkout: Check-out date in YYYY-MM-DD format
    :param group_adults: Number of adults
    :param group_children: Number of children
    :param no_rooms: Number of rooms
    :param lang: Language code (default "en-gb")
    :param currency: Currency code (default "GBP")
    :return: Fully assembled Booking.com URL as a string
    """
    base = "https://www.booking.com/searchresults.html"

    # Core query parameters
    params = {
        "ss": ss,
        "checkin": checkin,
        "checkout": checkout,
        "group_adults": group_adults,
        "group_children": group_children,
        "no_rooms": no_rooms,
        "lang": lang,
        "selected_currency": currency,
    }

    # Build and return full URL
    return urlunparse(("https", "www.booking.com", "/searchresults.html", "", urlencode(params), ""))


def save_file(data, file_path):
  # Ensure the directory exists
  os.makedirs(os.path.dirname(file_path), exist_ok=True)

  # Save JSON to file
  with open(file_path, 'w') as json_file:
      json.dump(data, json_file, indent=4)
  print(f"✅ Saved data to {file_path}")

def read_file(file_path):
  # Read JSON from file
  with open(file_path, 'r') as json_file:
      data = json.load(json_file)
  print(f"✅ Read data from {file_path}")
  
  return data

# Example usage:
if __name__ == "__main__":
    url = generate_booking_url(
        ss="Oran",
        dest_id="-480007",
        dest_type="city",
        checkin="2025-08-10",
        checkout="2025-09-30",
        group_adults=1,
        group_children=0,
        no_rooms=1,
        lang="en-gb",
        currency="GBP",
        extra_params={
            "aid": 304142,
            "label": "gen173nr-1FCAQoggJCFHNlYXJjaF9vcmFuLCBhbGdlcmlhSAlYBGjiAYgBAZgBCbgBGcgBDNgBAegBAfgBA4gCAagCA7gCoOeBwQbAAgHSAiRkOTllMjYwNy04NGFiLTQzYWItODkyMi05NDExMTAyNjExYWHYAgXgAgE"
        }
    )
    print(url)
