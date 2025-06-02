"""
Sequential agent for Orchestrating the conversation and workflow of ForkCast
"""
import asyncio
from google.adk.agents import SequentialAgent, LoopAgent
# from google.adk.sessions import InMemorySessionService, Session
# from google.adk.runners import Runner
from google.genai.types import Content, Part
from conversational_agent.agent import conversational_agent
from google.genai import types
# from .user_preference_agent.agent import user_preference_agent
import warnings
# Ignore all warnings
warnings.filterwarnings("ignore")

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# preference_gathering_loop_agent = None
# try:
    
#         preference_gathering_loop_agent = LoopAgent(
#         name="PreferenceGatheringLoopAgent",
#         sub_agents=[conversational_agent],
#         description="A loop agent that continues to gather user preferences until the UserPreferenceAgent indicates readiness for search.",
#         max_iterations=1,  # Limit iterations to prevent infinite loops
#         )
#         print("--- PreferenceGatheringLoopAgent created successfully. ---")
        
# except Exception as e:
#     print(f"Error creating PreferenceGatheringLoopAgent: {e}")
    

# root_agent = SequentialAgent(
#     name="OrchestratorAgent",
#     sub_agents=[preference_gathering_loop_agent],
#     description="Orchestrates the multi-agent workflow for Forkcast: gathers preferences, searches locations, enriches data, finds offers, and reviews matches.",
# )

root_agent = conversational_agent  # For now, use the conversational agent directly
logger.info(f"Root agent set to: {root_agent.name}")