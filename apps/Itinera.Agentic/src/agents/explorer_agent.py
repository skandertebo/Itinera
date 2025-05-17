
from typing import Dict, List
from langgraph.prebuilt import create_react_agent
from langchain.tools import tool
from ..schema.prompts import EXPLORER_AGENT_SYSTEM_PROMPT

# Mock Tools for Explorer Agent
@tool
def search_accommodations(requirements: Dict) -> List[Dict]:
    """
    Search for accommodations based on travel requirements.
    """
    # In a real implementation, this would call an external API
    # Mock data for demonstration
    print(f"Calling search accomodations with requirements: {requirements}")
    
    num_nights = 3;
    mock_results = [
        {
            "hotel_name": "3asba",
            "hotel_rating": 4.5,
            "price_per_night": 150.0,
            "total_price": 150.0 * num_nights,
            "location": f"Downtown Bali",
            "amenities": ["WiFi", "Pool", "Restaurant", "Fitness Center"],
            "available": True
        },
        {
            "hotel_name": "Zeby",
            "hotel_rating": 3.8,
            "price_per_night": 95.0,
            "total_price": 95.0 * num_nights,
            "location": f"North Bali",
            "amenities": ["WiFi", "Free Breakfast", "Parking"],
            "available": True
        },
        {
            "hotel_name": "L9a7ba",
            "hotel_rating": 4.9,
            "price_per_night": 275.0,
            "total_price": 275.0 * num_nights,
            "location": f"Beachfront, Bali",
            "amenities": ["WiFi", "Pool", "Spa", "Restaurant", "Room Service", "Ocean View"],
            "available": True
        }
    ]
    
    return mock_results

# Analyst Agent
def create_explorer_agent(llm):
  analyst_agent = create_react_agent(
      llm,
      tools=[search_accommodations],
      prompt=EXPLORER_AGENT_SYSTEM_PROMPT,
      name="Accomodation_Research_Expert"
  )
  
  return analyst_agent