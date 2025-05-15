from flask import Flask, jsonify, request

from core.booking_scraper import BookingScraper
from models.bookingQuery import BookingQuery

app = Flask(__name__)

@app.route('/scrape', methods=['POST'])
def scrape():
    try:
        data = request.get_json()
        query = BookingQuery(**data)
        scraper = BookingScraper(query=query)
        
        results = scraper.scrape()
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
