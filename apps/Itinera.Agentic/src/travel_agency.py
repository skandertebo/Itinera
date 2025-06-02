from agents.analyst_agent import create_analyst_agent
from agents.explorer_agent import create_explorer_agent
from agents.qa_agent import create_qa_agent
from langchain.callbacks import StdOutCallbackHandler
from langchain.schema import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph_supervisor import create_supervisor
from schema.prompts import DIRECTOR_AGENT_SYSTEM_PROMPT

model = ChatOpenAI(model="gpt-4o", callbacks=[StdOutCallbackHandler()])

def create_travel_agency():
  # Create the supervisor workflow to manage the Engineering Manager agents
  analyst_agent = create_analyst_agent(model)
  explorer_agent = create_explorer_agent(model)
  qa_agent = create_qa_agent(model)
  workflow = create_supervisor(
      agents=[
          analyst_agent,
          explorer_agent,
          qa_agent
      ],
      model=model,
      prompt=DIRECTOR_AGENT_SYSTEM_PROMPT
  )

  # Compile the workflow and run the query
  return workflow.compile()

def consult_travel_agency(customerRequestStr: str) -> str:
  travel_agency = create_travel_agency()
  result = travel_agency.invoke({
      "messages": [
          HumanMessage(content=(
              "Recommend me a travel plan based on these preferences"
              f"{customerRequestStr}"
          ))
      ]
  }, debug=True)
  
  final_agency_response: AIMessage = result["messages"][-1];
  return final_agency_response.content