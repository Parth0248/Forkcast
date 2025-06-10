from google.adk.agents import LlmAgent
from google.adk.tools.openapi_tool.openapi_spec_parser.openapi_toolset import OpenAPIToolset
from config.settings import GEMINI_MODEL, FOURSQUARE_API_KEY

from fsq_enrichment_agent.prompt import FOURSQUARE_ENRICHMENT_AGENT_INSTRUCTIONS

from fastapi.openapi.models import HTTPBearer
from google.adk.auth.auth_credential import AuthCredential, AuthCredentialTypes, HttpAuth, HttpCredentials

# OpenAPI specification for Yelp Fusion API
from fsq_enrichment_agent.foursquare_openapi_spec import FOURSQUARE_OPENAPI_SPEC

# 1. Define the AuthScheme object by instantiating HTTPBearer
# The 'type' will be 'http' and 'scheme' will be 'bearer' by default for HTTPBearer.
fsq_auth_scheme_definition = HTTPBearer(
    description="Foursquare API Key provided as a Bearer token.",
    bearerFormat="JWT" # Or "APIKey", or omit if not adding specific value
)
fsq_auth_credential = AuthCredential(
    auth_type=AuthCredentialTypes.HTTP, # This is correct (AuthCredentialTypes.HTTP)
    http=HttpAuth(
        scheme="bearer", # Should match the scheme defined
        credentials=HttpCredentials(token=FOURSQUARE_API_KEY)
    )
)

try:
    fsq_toolset = OpenAPIToolset(
        spec_dict=FOURSQUARE_OPENAPI_SPEC,
        auth_scheme=fsq_auth_scheme_definition, # Pass the HTTPBearer instance
        auth_credential=fsq_auth_credential
    )
    print("OpenAPIToolset for Yelp initialized successfully.")

except Exception as e:
    print(f"Error initializing OpenAPIToolset for Yelp: {e}")

    
# root_agent = LlmAgent(
fsq_enrichment_agent = LlmAgent(
    model=GEMINI_MODEL,
    name='FourSquareEnrichmentAgent',
    instruction=FOURSQUARE_ENRICHMENT_AGENT_INSTRUCTIONS,
    description=(
        "Fetches restaurant attributes, amenities, menu and dietary data from Foursquare API for up to 8 restaurants. "
        "Takes restaurant names and addresses, searches Foursquare for matches, and returns "
        "filtered data including title, attributes, amenities, menu and dietary data. "
        "Handles no-match scenarios by setting fields to null. "
        "Input must be a valid JSON string with restaurant data."
    ),
    tools=[fsq_toolset],
    output_key='fsq_data'
)

