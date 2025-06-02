import json
from google.adk.agents import LlmAgent
from config.settings import GEMINI_MODEL # Make sure GEMINI_MODEL is correctly imported from your settings
from user_preference_agent.prompt import USER_PREFERENCE_AGENT_INSTRUCTIONS


user_preference_agent = LlmAgent(
    model=GEMINI_MODEL,
    name='UserPreferenceAgent', # This name is used when it's an AgentTool
    instruction=USER_PREFERENCE_AGENT_INSTRUCTIONS,
    description=(
        "Validates and processes user dining preferences from a query_details JSON, "
        "identifies missing information, updates query status, and returns the updated query_details JSON. "
        "Input must be a valid JSON string of query_details."
    ),
    output_key='query_details',  # The output will be a JSON string of the updated query_details
    # No tools needed for UPA itself, its logic is in the instructions
)