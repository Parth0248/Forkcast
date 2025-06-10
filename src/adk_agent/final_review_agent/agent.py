from google.adk.agents import LlmAgent
from config.settings import NEW_GEMINI_MODEL # Make sure GEMINI_MODEL is correctly imported from your settings
from final_review_agent.prompt import FINAL_REVIEW_AGENT_INSTRUCTIONS


final_review_agent = LlmAgent(
    model=NEW_GEMINI_MODEL,
    name='FinalReviewAgent',
    instruction=FINAL_REVIEW_AGENT_INSTRUCTIONS,
    description=(
        "This agent reviews the search and various place enrichment results to ensure they are aligned with the user's preferences."
        "It compiles these results in a final_results object in a uniform format."
        "It transfers back the control to the ConversationalAgent if user has wants to update preferences or needs further assistance."
    ),
    output_key='final_results',  # The output will be a JSON string of the updated final_results object
)