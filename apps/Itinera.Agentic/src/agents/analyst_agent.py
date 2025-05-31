
from langgraph.prebuilt import create_react_agent
from schema.prompts import ANALYST_AGENT_SYSTEM_PROMPT

# Analyst Agent
def create_analyst_agent(llm):
  analyst_agent = create_react_agent(
      llm,
      tools=[],
      prompt=ANALYST_AGENT_SYSTEM_PROMPT,
      name="Travel_Requirements_Analyst"
  )
  
  return analyst_agent