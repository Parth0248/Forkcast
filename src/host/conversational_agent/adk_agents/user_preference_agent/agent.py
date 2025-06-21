from google.adk.agents import LlmAgent

from conversational_agent.config.settings import GEMINI_MODEL # Make sure GEMINI_MODEL is correctly imported from your settings
from conversational_agent.adk_agents.user_preference_agent.prompt import USER_PREFERENCE_AGENT_INSTRUCTIONS
from conversational_agent.tools.get_guest_pref import fetch_and_integrate_preferences

user_preference_agent = LlmAgent(
    model=GEMINI_MODEL,
    name='UserPreferenceAgent', # This name is used when it's an AgentTool
    instruction=USER_PREFERENCE_AGENT_INSTRUCTIONS,
    description=(
        "Aggregates guest preferences and integrates host preferences for restaurant search. "
        "ALWAYS calls fetch_and_integrate_preferences tool first with party_code from user message. "
        "Validates combined preferences and sets search readiness flags. "
        "Input: JSON string of query_details. Output: Updated query_details with aggregated preferences."
    ),
    tools=[fetch_and_integrate_preferences],  # Use the fetch_guest_preferences tool to get existing preferences
    output_key='query_details',  # The output will be a JSON string of the updated query_details
    # No tools needed for UPA itself, its logic is in the instructions
)