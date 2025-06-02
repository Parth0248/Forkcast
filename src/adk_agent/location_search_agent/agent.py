# ./adk_agent_samples/mcp_agent/agent.py
import os
import platform

from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from location_search_agent.prompt import LOCATION_SEARCH_AGENT_INSTRUCTIONS
from config.settings import GOOGLE_MAPS_API_KEY as google_maps_api_key
from config.settings import GEMINI_MODEL
# Load the Google Maps API key from environment variable

# Ensure you have the Google Maps API key set in your environment variables.
if not google_maps_api_key:
    print("Google Maps API key not found in environment variables. Please set GOOGLE_MAPS_API_KEY.")    
else:
    print("Google Maps API key found. Proceeding with agent initialization.", google_maps_api_key)
        
        
# # Windows-specific configuration
# def get_mcp_command_params():
#     if platform.system() == 'Windows':
#         # Method 1: Try PowerShell
#         # return {
#         #     'command': 'powershell.exe',
#         #     'args': [
#         #         '-Command',
#         #         'npx -y @modelcontextprotocol/server-google-maps'
#         #     ]
#         # }
        
#         # Method 2: Try cmd.exe
#         return {
#             'command': 'cmd.exe',
#             'args': [
#                 '/c',
#                 'npx -y @modelcontextprotocol/server-google-maps'
#             ]
#         }
        
#         # Method 3: Try direct npx path (uncomment if above methods fail)
#         # npx_paths = [
#         #     r'C:\Program Files\nodejs\npx.cmd',
#         #     r'C:\Program Files (x86)\nodejs\npx.cmd',
#         #     'npx.cmd',
#         #     'npx'
#         # ]
#         # 
#         # for npx_path in npx_paths:
#         #     if os.path.exists(npx_path) or npx_path in ['npx.cmd', 'npx']:
#         #         return {
#         #             'command': npx_path,
#         #             'args': [
#         #                 '-y',
#         #                 '@modelcontextprotocol/server-google-maps'
#         #             ]
#         #         }
#         # 
#         # # Fallback
#         # return {
#         #     'command': 'npx',
#         #     'args': [
#         #         '-y',
#         #         '@modelcontextprotocol/server-google-maps'
#         #     ]
#         # }
#     else:
#         # Unix/Linux/Mac
#         return {
#             'command': 'npx',
#             'args': [
#                 '-y',
#                 '@modelcontextprotocol/server-google-maps'
#             ]
#         }

# command_params = get_mcp_command_params()        
        
root_agent = LlmAgent(
# location_search_agent = LlmAgent(
    model=GEMINI_MODEL,
    name='LocationSearchAgent',
    description=(
        "Helps users find a restaurant that meets their requirements using the Google Maps MCP tools. "
        "It can search for places, get place details, and provide directions."
    ),
    instruction=LOCATION_SEARCH_AGENT_INSTRUCTIONS,
    # instruction="help the user find a restaurant that meets their requirements using the Google Maps MCP tools",
    tools=[
        MCPToolset(
            connection_params=StdioServerParameters(
                # command=command_params['command'],
                # args=command_params['args'],
                command="npx",
                args=[
                    "-y",
                    "@modelcontextprotocol/server-google-maps",
                ],
                env={
                    "GOOGLE_MAPS_API_KEY": google_maps_api_key
                }
            ),
            # You can filter for specific Maps tools if needed:
            # tool_filter=['get_directions', 'find_place_by_id']
        )
    ],
    # output_key='search_results',  # The output will be a JSON string of the search results
)
