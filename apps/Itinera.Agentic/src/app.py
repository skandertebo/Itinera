from typing import Dict
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.tools import tool
from langchain.memory import ConversationBufferMemory
from schema.classes import TravelRequirements, BookingResult, Destination, Travelers, Accommodation, Budget
from schema.prompts import CUSTOMER_FACING_AGENT_SYSTEM_PROMPT

from travel_agency import consult_travel_agency

# Load environment variables
load_dotenv()


# Initialize LLM
llm = ChatOpenAI(temperature=0.7, model="gpt-4o", api_key=OPENAI_API_KEY)

# Tools for Customer-Facing Agent
@tool

def extract_travel_requirements(conversation: str) -> TravelRequirements:
    """
    Extract travel requirements from the conversation.
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", """Extract travel requirements from the conversation.\nYou are a helpful assistant that extracts structured data from natural language.\nGiven a user’s travel request, extract all relevant details and return a valid JSON object that matches the following schema.\nEnsure that all required fields are included and valid. Optional fields should only be included if they are mentioned.\n\n**Schema Fields**:\n- **destination.city** (str, required): City of the travel destination\n- **destination.country** (str, required): Country of the travel destination\n- **check_in** (date, required): Check-in date (format: YYYY-MM-DD)\n- **check_out** (date, required): Check-out date (format: YYYY-MM-DD)\n- **travelers.adults** (int, required, >= 1): Number of adult travelers\n- **travelers.children** (int, required, >= 0): Number of child travelers\n- **travelers.companions** (str, optional): Who the client is traveling with\n- **accommodation.rooms** (int, required, >= 1): Number of rooms required\n- **accommodation.room_types** (List[str], required): Preferred room types\n- **budget.min** (float, required, >= 0): Minimum budget in USD\n- **budget.max** (float, required, >= 0): Maximum budget in USD\n- **travel_purpose** (str, optional): Purpose of the trip (e.g., leisure, business)\n- **preferred_activities** (List[str], optional): Activities or interests\n- **travel_history** (str, optional): Client’s travel background\n- **preferred_climate** (str, optional): Desired climate or season\n- **special_requirements** (List[str], optional): Any specific needs\n- **user_language** (str, required): User's preferred language\n- **user_currency** (str, required): User's preferred currency\n- **user_country** (str, required): User's country\n\n**Instructions**:\n- Extract the fields from the provided user input.\n- Return only the JSON output in the exact structure.\n- Do not include any explanations or extra text.\n- Dates must be in YYYY-MM-DD format.\n- Omit optional fields if not mentioned in the input.\n\n**User Input**:\n{conversation}\n\n**Expected Output**:\nA JSON object matching the schema above, strictly formatted and including only mentioned optional fields.""")
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
    
    # Parse as JSON and convert to TravelRequirements model
    import json
    try:
        data = json.loads(content)
        print(data)
        return TravelRequirements(**data)
    except (json.JSONDecodeError, ValueError):
        # Fallback to a default structure if parsing fails
        return TravelRequirements(
            destination=Destination(city=None, country=None),
            check_in=None,
            check_out=None,
            travelers=Travelers(adults=None, children=None, companions=None),
            accommodation=Accommodation(rooms=None, room_types=None),
            budget=Budget(min=None, max=None),
            travel_purpose=None,
            preferred_activities=None,
            travel_history=None,
            preferred_climate=None,
            special_requirements=None
        )


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
        ("system", CUSTOMER_FACING_AGENT_SYSTEM_PROMPT),
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