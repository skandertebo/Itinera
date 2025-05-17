from langgraph.prebuilt import create_react_agent
from ..schema.prompts import QA_AGENT_SYSTEM_PROMPT

# Analyst Agent
def create_qa_agent(llm):
  analyst_agent = create_react_agent(
      llm,
      tools=[],
      prompt=QA_AGENT_SYSTEM_PROMPT,
      name="Travel_Recommendations_Quality_Assessor"
  )
  
  return analyst_agent