from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.tools import tool
from langchain.memory import ConversationBufferMemory

from .travel_agency import consult_travel_agency

# Load environment variables
load_dotenv()

# Models for structured data
class TravelRequirements(BaseModel):
    destination: Optional[str] = Field(None, description="Destination city, country, or region")
    start_date: Optional[str] = Field(None, description="Start date of the trip (YYYY-MM-DD)")
    end_date: Optional[str] = Field(None, description="End date of the trip (YYYY-MM-DD)")
    budget: Optional[str] = Field(None, description="Budget for the trip")
    num_travelers: Optional[int] = Field(None, description="Number of travelers")
    accommodation_preferences: Optional[str] = Field(None, description="Preferences for accommodation")
    activity_preferences: Optional[str] = Field(None, description="Preferred activities during the trip")
    transportation_preferences: Optional[str] = Field(None, description="Preferred modes of transportation")

class BookingResult(BaseModel):
    hotel_name: str = Field(..., description="Name of the hotel")
    hotel_rating: float = Field(..., description="Rating of the hotel (1-5)")
    price_per_night: float = Field(..., description="Price per night in USD")
    total_price: float = Field(..., description="Total price for the stay in USD")
    location: str = Field(..., description="Location of the hotel")
    amenities: List[str] = Field(..., description="List of amenities")
    available: bool = Field(..., description="Whether the hotel is available for the requested dates")

# Initialize LLM
llm = ChatOpenAI(temperature=0.7, model="gpt-4o")

# Tools for Customer-Facing Agent
@tool
def extract_travel_requirements(conversation: str) -> Dict:
    """
    Extract travel requirements from the conversation.
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", """Extract travel requirements from the conversation. 
        Return a JSON object with keys: destination, start_date, end_date, budget, num_travelers, 
        accommodation_preferences, activity_preferences, transportation_preferences.
        If information is not provided, set the value to null.
        Important: Return only the raw JSON without any markdown formatting, code blocks, or additional text."""),
        ("user", f"Conversation: {conversation}")
    ])
    
    response = llm.invoke(prompt.format_messages(conversation=conversation))
    
    # Clean up response content - remove markdown code blocks if present
    content = response.content
    if "```json" in content:
        # Extract content between ```json and ```
        import re
        json_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", content)
        if json_match:
            content = json_match.group(1)
    
    # Parse as JSON
    import json
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        # Fallback to a default structure if parsing fails
        return {
            "destination": None,
            "start_date": None,
            "end_date": None,
            "budget": None,
            "num_travelers": None,
            "accommodation_preferences": None,
            "activity_preferences": None,
            "transportation_preferences": None
        }

@tool
def process_customer_request(customerRequestStr: str) -> str:
    """Processes a customer request by contacting a travel agency 
    and requesting travel info with the customer's preferences.

    Args:
        customerRequestStr (str): a json string representing the customer's travel requirements

    Returns:
        str: The response of the travel agency
    """
    
    travel_agency_result = consult_travel_agency(customerRequestStr)
    
    return travel_agency_result

# Customer-Facing Agent
def create_customer_facing_agent():
    tools = [extract_travel_requirements, process_customer_request]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a friendly travel assistant helping users plan their trips.
        Your goal is to gather all necessary information about their travel plans.
        Ask questions to learn about: destination, dates, budget, number of travelers,
        accommodation preferences, activity interests, and transportation preferences.
        Be conversational and helpful. Do not overwhelm the user with too many questions at once.
        Only use the provided tools when you have gathered sufficient information."""),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    agent = create_openai_tools_agent(llm, tools, prompt)
    
    return AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True,
        max_iterations=3
    )
# Main application
def travel_recommendation_app():
    print("🌴 Welcome to AI Travel Planner! 🌴")
    print("I'm your travel assistant. Let me help you plan your next trip.")
    print("Type 'exit' at any time to quit.\n")
    
    # Create agents
    customer_agent = create_customer_facing_agent()
    
    travel_requirements = {}
    booking_complete = False
    
    while not booking_complete:
        user_input = input("\nYou: ")
        
        if user_input.lower() == 'exit':
            print("\nThank you for using AI Travel Planner. Have a great day!")
            break
        
        # Step 1: Customer agent interacts with user
        try:
            customer_response = customer_agent.invoke({"input": user_input})
            print(f"\nTravel Assistant: {customer_response['output']}")
        except Exception as e:
            print(f"\nTravel Assistant: I'm sorry, I encountered an error: {str(e)}")
            print("Let's continue our conversation about your travel plans.")

if __name__ == "__main__":
    travel_recommendation_app()