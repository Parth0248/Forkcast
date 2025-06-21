from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

from conversational_agent.adk_agents.google_reviews_agent.prompt import GOOGLE_REVIEWS_AGENT_INSTRUCTIONS
from conversational_agent.config.settings import GOOGLE_MAPS_API_KEY as google_maps_api_key
from conversational_agent.config.settings import GEMINI_MODEL


# root_agent = LlmAgent(
google_reviews_agent = LlmAgent(
    model=GEMINI_MODEL,
    name='GoogleReviewsAgent',
    description=(
        "Helps extract reviews, ratings, popular items, menu and more for restaurants using the Google Maps MCP tools."
    ),
    instruction=GOOGLE_REVIEWS_AGENT_INSTRUCTIONS,
        tools=[
        MCPToolset(
            connection_params=StdioServerParameters(
                command="npx",
                args=[
                    "-y",
                    "@modelcontextprotocol/server-google-maps",
                ],
                env={
                    "GOOGLE_MAPS_API_KEY": google_maps_api_key
                }
            ),
        )
    ],
    output_key='google_reviews_data',  # The output will be a JSON string of the search results
)
