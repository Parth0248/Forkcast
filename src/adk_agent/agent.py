from conversational_agent.agent import root_agent as conversational_agent
import warnings
# Ignore all warnings
warnings.filterwarnings("ignore")

root_agent = conversational_agent  # For now, use the conversational agent directly

# import json
# from typing import Optional

# from google.adk.agents import LlmAgent, SequentialAgent, ParallelAgent
# from google.adk.tools.agent_tool import AgentTool
# from google.adk.tools.exit_loop_tool import exit_loop

# from config.settings import NEW_GEMINI_MODEL
# from schemas.query_details_schema import QueryDetails

# from user_preference_agent.agent import user_preference_agent
# from location_search_agent.agent import location_search_agent
# from yelp_review_agent.agent import yelp_review_agent
# from fsq_enrichment_agent.agent import fsq_enrichment_agent
# from google_reviews_agent.agent import google_reviews_agent
# from busyness_forecast_agent.agent import busyness_forecast_agent
# from final_review_agent.agent import final_review_agent

# from conversational_agent.prompt import CONVERSATIONAL_AGENT_INSTRUCTIONS

# target_schema = QueryDetails.get_default_instance()

# # Define the parallel agent that enriches location data with reviews, forecasts and more
# parallel_enrichment_agent = ParallelAgent(
#     name="ParallelEnrichmentAgent",
#     sub_agents=[
#         yelp_review_agent,
#         fsq_enrichment_agent,
#         google_reviews_agent,
#         busyness_forecast_agent,
#     ],
#     description="Enriches location data with reviews and forecasts in parallel.",
# )

# # Define the sequential agent that first searches for locations and then enriches data
# sequential_search_agent = SequentialAgent(
#     name="SequentialSearchAgent",
#     sub_agents=[
#         location_search_agent,  # Use the location_search_agent tool
#         parallel_enrichment_agent,  # Enrich data with reviews and forecasts
#         final_review_agent,  # Final review agent to summarize and finalize the results
#     ],
#     description="Sequentially searches for locations based on user preferences and then parallelly enriches data with reviews and forecasts.",
# )

# # Instantiate user_preference_agent as a tool for the ConversationalAgent
# user_preference_agent_instance = AgentTool(agent=user_preference_agent)
# sequential_search_agent_instance = AgentTool(agent=sequential_search_agent)

# # conversational_agent = LlmAgent(
# root_agent = LlmAgent(
#     name="ConversationalAgent",
#     model=NEW_GEMINI_MODEL,
#     instruction=CONVERSATIONAL_AGENT_INSTRUCTIONS,
#     # instruction=TEST_PROMPT,
#     description="Manages conversation, extracts preferences, sends it to the user_preference_agent to update and validate its preferences, and identify critical missing information.",
#     tools=[
#         user_preference_agent_instance,  # Use the user_preference_agent tool
#         sequential_search_agent_instance,  # Use the restaurant_search_agent tool
#     ],
#     output_key='query_details',  # The output will be a JSON string of the updated query_details
    
# )
