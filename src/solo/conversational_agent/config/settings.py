# config/settings.py - Based on Google's Codelabs tutorial pattern
import os

# Load environment variables - using the same pattern as Google's tutorial
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Environment variables loaded from .env")
except ImportError:
    print("ℹ️ Running in deployed environment")

# Core Google Cloud Configuration - exactly matching Codelabs tutorial names
GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "forkcast-460406")
GOOGLE_CLOUD_LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
GOOGLE_CLOUD_REGION = os.getenv("GOOGLE_CLOUD_REGION", "us-central1")
PROJECT_ID = os.getenv("PROJECT_ID", GOOGLE_CLOUD_PROJECT)  # Some ADK code expects PROJECT_ID
GCP_REGION = GOOGLE_CLOUD_REGION  # Alias for backward compatibility

# Vertex AI Gemini Model Configuration
GEMINI_MODEL = "gemini-2.0-flash-001"
NEW_GEMINI_MODEL = "gemini-2.5-flash"
REASON_GEMINI_MODEL = "gemini-2.5-pro"
LITE_GEMINI_MODEL = "gemini-2.5-flash-lite-preview-06-17"

# API Keys for external services
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "") # For Google Maps and Places APIs
FOURSQUARE_API_KEY = os.getenv("FOURSQUARE_API_KEY", "") # For Foursquare API
YELP_API_KEY = os.getenv("YELP_API_KEY", "") # For Yelp Fusion API
BESTTIME_API_KEY = os.getenv("BESTTIME_API_KEY", "") # For BestTime API


if not GOOGLE_MAPS_API_KEY:
   print("Warning: GOOGLE_MAPS_API_KEY is not set. Maps and Places features might fail.")
if not FOURSQUARE_API_KEY:
   print("Warning: FOURSQUARE_API_KEY is not set. Foursquare features might fail.")
if not YELP_API_KEY:
   print("Warning: YELP_API_KEY is not set. Yelp features might fail.")
if not BESTTIME_API_KEY:
   print("Warning: BESTTIME_API_KEY is not set. BestTime features might fail.")