from google.adk.agents import LlmAgent
from google.adk.tools.openapi_tool.openapi_spec_parser.openapi_toolset import OpenAPIToolset
from fastapi.openapi.models import HTTPBearer
from google.adk.auth.auth_credential import AuthCredential, AuthCredentialTypes, HttpAuth, HttpCredentials


from conversational_agent.config.settings import NEW_GEMINI_MODEL, BESTTIME_API_KEY
from conversational_agent.adk_agents.busyness_forecast_agent.prompt import BUSYNESS_FORECAST_AGENT_INSTRUCTIONS
from conversational_agent.adk_agents.busyness_forecast_agent.besttime_openapi_spec import BESTTIME_OPENAPI_SPEC

# 1. Define the AuthScheme object by instantiating HTTPBearer
# The 'type' will be 'http' and 'scheme' will be 'bearer' by default for HTTPBearer.
besttime_auth_scheme_definition = HTTPBearer(
    description="BestTime API Key provided as a Bearer token.",
    bearerFormat="JWT" # Or "APIKey", or omit if not adding specific value
)
besttime_auth_credential = AuthCredential(
    auth_type=AuthCredentialTypes.HTTP, # This is correct (AuthCredentialTypes.HTTP)
    http=HttpAuth(
        scheme="bearer", # Should match the scheme defined
        credentials=HttpCredentials(token=BESTTIME_API_KEY,)
    )
)

try:
    besttime_toolset = OpenAPIToolset(
        spec_dict=BESTTIME_OPENAPI_SPEC,
        auth_scheme=besttime_auth_scheme_definition, # Pass the HTTPBearer instance
        auth_credential=besttime_auth_credential
    )
    print("OpenAPIToolset for Yelp initialized successfully.")

except Exception as e:
    print(f"Error initializing OpenAPIToolset for Yelp: {e}")

    
# root_agent = LlmAgent(
busyness_forecast_agent = LlmAgent(
    model=NEW_GEMINI_MODEL,
    name='BusynessForecastAgent',
    instruction=BUSYNESS_FORECAST_AGENT_INSTRUCTIONS,
    description=(
        "Advanced busyness intelligence agent that fetches real-time foot traffic forecasts "
        "and live crowd data for restaurants using BestTime API. Provides comprehensive "
        "analysis including peak hours, quiet times, weekly patterns, and current busyness "
        "levels with intelligent fallback strategies for maximum data coverage."
    ),
    tools=[besttime_toolset],
    output_key='busyness_data'
)

