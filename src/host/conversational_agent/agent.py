import json
from typing import Optional

from google.adk.agents import LlmAgent, SequentialAgent, ParallelAgent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.exit_loop_tool import exit_loop

from conversational_agent.config.settings import NEW_GEMINI_MODEL

from conversational_agent.adk_agents.user_preference_agent.agent import user_preference_agent
from conversational_agent.adk_agents.location_search_agent.agent import location_search_agent
from conversational_agent.adk_agents.yelp_review_agent.agent import yelp_review_agent
from conversational_agent.adk_agents.fsq_enrichment_agent.agent import fsq_enrichment_agent
from conversational_agent.adk_agents.google_reviews_agent.agent import google_reviews_agent
from conversational_agent.adk_agents.busyness_forecast_agent.agent import busyness_forecast_agent
from conversational_agent.adk_agents.final_review_agent.agent import final_review_agent

from conversational_agent.prompt import CONVERSATIONAL_AGENT_INSTRUCTIONS
# from conversational_agent.callback import validate_restaurant_relevance


# Define the parallel agent that enriches location data with reviews, forecasts and more
parallel_enrichment_agent = ParallelAgent(
    name="ParallelEnrichmentAgent",
    sub_agents=[
        yelp_review_agent,
        fsq_enrichment_agent,
        google_reviews_agent,
        busyness_forecast_agent,
    ],
    description="Enriches location data with reviews and forecasts in parallel.",
)

# Define the sequential agent that first searches for locations and then enriches data
sequential_search_agent = SequentialAgent(
    name="SequentialSearchAgent",
    sub_agents=[
        location_search_agent,  # Use the location_search_agent tool
        parallel_enrichment_agent,  # Enrich data with reviews and forecasts
    ],
    description="Sequentially searches for locations based on user preferences and then parallelly enriches data with reviews and forecasts.",
)

# Instantiate user_preference_agent, sequential_search_agent and final_review_agent as a tool for the ConversationalAgent
user_preference_agent_instance = AgentTool(agent=user_preference_agent)
sequential_search_agent_instance = AgentTool(agent=sequential_search_agent)
final_review_agent_instance = AgentTool(agent=final_review_agent)

# conversational_agent = LlmAgent(
    
root_agent = LlmAgent(
    name="ConversationalAgent",
    model= NEW_GEMINI_MODEL,
    instruction=CONVERSATIONAL_AGENT_INSTRUCTIONS,
    # instruction=TEST_PROMPT,
    description="Manages Greeting and initial conversation on it's own. Extracts preferences from substantial user message, sends it to the user_preference_agent to update and validate its preferences, and identify critical missing information."
                "It then uses the sequential_search_agent to search for restaurants based on the validated preferences and enriches the results with reviews and forecasts."
                "Finally, it uses the final_review_agent to summarize and finalize the results.",
    tools=[
        user_preference_agent_instance,  # Use the user_preference_agent tool
        sequential_search_agent_instance,  # Use the restaurant_search_agent tool
        final_review_agent_instance,  # Final review agent to summarize and finalize the results
    ],
    # before_agent_callback=validate_restaurant_relevance,
)