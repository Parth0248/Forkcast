import json
from typing import Optional

from google.adk.agents import LlmAgent, SequentialAgent, ParallelAgent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.exit_loop_tool import exit_loop

from conversational_agent.config.settings import NEW_GEMINI_MODEL, REASON_GEMINI_MODEL

from conversational_agent.adk_agents.user_preference_agent.agent import user_preference_agent

from conversational_agent.tools.store_guest_pref import upload_preferences
from conversational_agent.prompt import CONVERSATIONAL_AGENT_INSTRUCTIONS
# from conversational_agent.callback import validate_restaurant_relevance

# Instantiate user_preference_agent as a tool for the ConversationalAgent
user_preference_agent_instance = AgentTool(agent=user_preference_agent)

root_agent = LlmAgent(
    name="ConversationalAgent",
    model= NEW_GEMINI_MODEL,
    instruction=CONVERSATIONAL_AGENT_INSTRUCTIONS,
    # instruction=TEST_PROMPT,
    description="Manages Greeting and initial conversation on it's own. Extracts preferences from substantial user message, sends it to the user_preference_agent to update and validate its preferences, and identify critical missing information."
                "Finally, it uses the upload_preferences tool to upload the preferences to the firestore database.",
    tools=[
        user_preference_agent_instance,  # Use the user_preference_agent tool
        upload_preferences,
    ],
    # before_agent_callback=validate_restaurant_relevance,
)