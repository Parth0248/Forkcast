from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

from conversational_agent.adk_agents.location_search_agent.prompt import LOCATION_SEARCH_AGENT_INSTRUCTIONS
from conversational_agent.config.settings import GOOGLE_MAPS_API_KEY as google_maps_api_key
from conversational_agent.config.settings import GEMINI_MODEL


# root_agent = LlmAgent(
location_search_agent = LlmAgent(
    model=GEMINI_MODEL,
    name='LocationSearchAgent',
    description=(
        "Helps agent shortlist restaurants that meets the requirements set in query_details using the Google Maps MCP tools. "
        "It can search for places, get place details, and stores results in a structured format. "
    ),
    instruction=LOCATION_SEARCH_AGENT_INSTRUCTIONS,
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
    output_key='search_results',  # The output will be a JSON string of the search results
)
