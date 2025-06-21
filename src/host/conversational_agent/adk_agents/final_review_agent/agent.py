from google.adk.agents import LlmAgent

from conversational_agent.config.settings import NEW_GEMINI_MODEL # Make sure GEMINI_MODEL is correctly imported from your settings
from conversational_agent.adk_agents.final_review_agent.prompt import FINAL_REVIEW_AGENT_INSTRUCTIONS
from conversational_agent.adk_agents.final_review_agent.schema import FinalReviewOutput

final_review_agent = LlmAgent(
    model=NEW_GEMINI_MODEL,
    name='FinalReviewAgent',
    instruction=FINAL_REVIEW_AGENT_INSTRUCTIONS,
    description=(
        "This agent reviews the search and various place enrichment results to ensure they are aligned with the user's preferences."
        "It compiles these results in a final_results object in a uniform format."
    ),
    output_schema=FinalReviewOutput,
    output_key='final_results',  # The output will be a JSON string of the updated final_results object
)