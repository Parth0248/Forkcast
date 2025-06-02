import json
from typing import Optional

from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.exit_loop_tool import exit_loop

from config.settings import NEW_GEMINI_MODEL

from user_preference_agent.agent import user_preference_agent
from location_search_agent.agent import location_search_agent
from schemas.query_details_schema import QueryDetails
# from conversational_agent.tools import update_session_query_details

from conversational_agent.prompt import CONVERSATIONAL_AGENT_INSTRUCTIONS

target_schema = QueryDetails.get_default_instance()


# Instantiate user_preference_agent as a tool for the ConversationalAgent
user_preference_agent_instance = AgentTool(agent=user_preference_agent)
location_search_agent_instance = AgentTool(agent=location_search_agent)

conversational_agent = LlmAgent(
    name="ConversationalAgent",
    model=NEW_GEMINI_MODEL,
    instruction=CONVERSATIONAL_AGENT_INSTRUCTIONS,
    # instruction=TEST_PROMPT,
    description="Manages conversation, extracts preferences, sends it to the user_preference_agent to update and validate its preferences, and identify critical missing information.",
    tools=[
        user_preference_agent_instance,  # Use the user_preference_agent tool
        location_search_agent_instance,  # Use the location_search_agent tool
    ]
)
