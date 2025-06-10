import json
from google.adk.agents import LlmAgent
from google.adk.tools.openapi_tool.openapi_spec_parser.openapi_toolset import OpenAPIToolset
from config.settings import GEMINI_MODEL, YELP_API_KEY

from yelp_review_agent.prompt import YELP_REVIEW_AGENT_INSTRUCTIONS

from fastapi.openapi.models import HTTPBearer
from google.adk.auth.auth_credential import AuthCredential, AuthCredentialTypes, HttpAuth, HttpCredentials

# OpenAPI specification for Yelp Fusion API
from yelp_review_agent.yelp_fusion_openapi_spec import YELP_OPENAPI_SPEC

# 1. Define the AuthScheme object by instantiating HTTPBearer
# The 'type' will be 'http' and 'scheme' will be 'bearer' by default for HTTPBearer.
yelp_auth_scheme_definition = HTTPBearer(
    description="Yelp API Key provided as a Bearer token.",
    bearerFormat="JWT" # Or "APIKey", or omit if not adding specific value
)
yelp_auth_credential = AuthCredential(
    auth_type=AuthCredentialTypes.HTTP, # This is correct (AuthCredentialTypes.HTTP)
    http=HttpAuth(
        scheme="bearer", # Should match the scheme defined
        credentials=HttpCredentials(token=YELP_API_KEY)
    )
)

try:
    yelp_toolset = OpenAPIToolset(
        spec_dict=YELP_OPENAPI_SPEC,
        auth_scheme=yelp_auth_scheme_definition, # Pass the HTTPBearer instance
        auth_credential=yelp_auth_credential
    )
    print("OpenAPIToolset for Yelp initialized successfully.")

except Exception as e:
    print(f"Error initializing OpenAPIToolset for Yelp: {e}")

    
# root_agent = LlmAgent(
yelp_review_agent = LlmAgent(
    model=GEMINI_MODEL,
    name='YelpReviewAgent',
    instruction=YELP_REVIEW_AGENT_INSTRUCTIONS,
    description=(
        "Fetches restaurant review data from Yelp Fusion API for up to 10 restaurants. "
        "Takes restaurant names and addresses, searches Yelp for matches, and returns "
        "filtered data including title, image_url, review_count, rating, and price. "
        "Handles no-match scenarios by setting fields to null. "
        "Input must be a valid JSON string with restaurant data."
    ),
    tools=[yelp_toolset],
    output_key='yelp_reviews_data'
)

