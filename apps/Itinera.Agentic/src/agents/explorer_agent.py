
from typing import Dict, List
from langgraph.prebuilt import create_react_agent
from langchain.tools import tool
from schema.prompts import EXPLORER_AGENT_SYSTEM_PROMPT
from schema.classes import BookingResult, Pricing, TravelRequirements
import requests

def to_filtering_model(tr: TravelRequirements) -> dict:
    return {
        "destination": {
            "city": tr.destination.city,
            "country": tr.destination.country
        },
        "checkIn": tr.check_in.isoformat(),
        "checkOut": tr.check_out.isoformat(),
        "travelers": {
            "adults": tr.travelers.adults,
            "children": tr.travelers.children
        },
        "accommodation": {
            "rooms": tr.accommodation.rooms,
            "roomTypes": tr.accommodation.room_types
        },
        "budget": {
            "min": tr.budget.min,
            "max": tr.budget.max
        },
        "userCurrency": tr.user_currency,
        "userCountry": tr.user_country,
        "userLanguage": tr.user_language
    }

# Mock Tools for Explorer Agent
@tool
def search_accommodations(requirements: TravelRequirements) -> List[Dict]:
    """
    Search for accommodations based on travel requirements by calling the backend server.
    """

    filtered_payload = to_filtering_model(requirements)
    print(filtered_payload)

    url = "http://localhost:5015/api/ItineraSeeker"
    headers = {
        "accept": "text/plain",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=filtered_payload, headers=headers)
        response.raise_for_status()
        print(response.json())
        return response.json()  
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return []

# Analyst Agent
def create_explorer_agent(llm):
  analyst_agent = create_react_agent(
      llm,
      tools=[search_accommodations],
      prompt=EXPLORER_AGENT_SYSTEM_PROMPT,
      name="Accomodation_Research_Expert"
  )
  
  return analyst_agent