# 🏨 Booking.com Hotel Scraper API

A Python Flask API that scrapes hotel data from [Booking.com](https://www.booking.com) based on search parameters like location, dates, guests, and more. The scraper returns detailed hotel information including names, prices, ratings, facilities, and nearby landmarks.

---

## 🚀 Features

* 🔍 Search hotels using Booking.com’s interface
* 🧭 Navigate the “Load More” button to fetch all results
* 🧼 Scrape detailed hotel data using BeautifulSoup
* 🛏️ Get structured hotel information including:

  * Name
  * Pricing
  * Ratings
  * Facilities
  * Nearby points of interest

---

## 📦 Tech Stack

* Python 3.9+
* Flask
* Selenium (for dynamic content)
* BeautifulSoup (for parsing HTML)
* ChromeDriver

---

## 📥 Installation
1. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Make sure ChromeDriver is installed and in your PATH**

---

## 🧪 Usage

### Start the Flask server

```bash
python app.py
```

### Make a request

```bash
curl -X POST http://localhost:5000/scrape \
  -H "Content-Type: application/json" \
  -d '{
    "search_string": "London",
    "checkin_date": "2025-06-01",
    "checkout_date": "2025-06-05",
    "number_of_adults": 2,
    "number_of_children": 1,
    "number_of_rooms": 1,
    "language": "en-gb",
    "currency": "GBP",
    "user_country": "UK"
  }'
```

---

## 🔍 API Endpoint

### `POST /scrape`

**Request Body (JSON):**

| Field                | Type   | Description                   |
| -------------------- | ------ | ----------------------------- |
| `search_string`      | string | City or area to search        |
| `checkin_date`       | string | Format: YYYY-MM-DD            |
| `checkout_date`      | string | Format: YYYY-MM-DD            |
| `number_of_adults`   | int    | Number of adults              |
| `number_of_children` | int    | Number of children            |
| `number_of_rooms`    | int    | Number of rooms               |
| `language`           | string | Booking.com language code     |
| `currency`           | string | ISO currency code (e.g., GBP) |
| `user_country`       | string | Country code (e.g., UK)       |

**Response:**

Returns a JSON list of hotels, each with:

```json
{
  "name": "Hotel Example",
  "pricing": "£123",
  "rating": 8.7,
  "detailed_ratings": {
    "Cleanliness": 8.9,
    "Comfort": 8.6,
    "Facilities": 8.4,
    "Location": 9.1,
    "Staff": 8.8,
    "Value for money": 8.0
  },
  "facilities": ["Free WiFi", "Parking", "Family rooms"],
  "surroundings": ["Hyde Park", "Big Ben"]
}
```

---

## 🧱 Project Structure

```
booking-scraper-api/
├── .gitignore
├── readme.md
├── core
│   ├── hotel_details_scraper_thread.py
│   ├── hotel_details_scraper.py
│   ├── utils.py
│   ├── hotel_list_scraper.py
│   ├── booking_scraper.py
├── requirements.txt
├── models
│   ├── bookingQuery.py
├── app.py
```

---

## 🧠 How It Works

* `BookingScraper` is the main class coordinating the scraping process.

  * `HotelsListScraper`: Uses Selenium to open Booking.com, search, and extract hotel names and URLs.
  * `HotelDetailsScraper`: Uses requests + BeautifulSoup to fetch and parse each hotel’s data.

---

## 🛡️ Disclaimer

This project is for educational purposes only. Scraping Booking.com may violate their Terms of Service. Use responsibly and consider contacting the site for API access.

---

## 📃 License

MIT License
