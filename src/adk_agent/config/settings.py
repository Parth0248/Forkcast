# forkcast/config/settings.py
import os
from dotenv import load_dotenv

load_dotenv() # Loads variables from .env file into environment variables

# GCP Project Configuration
GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
GCP_REGION = os.getenv("GCP_REGION", "us-central1") # Or your preferred region

# Vertex AI Gemini Model Configuration
GEMINI_MODEL = "gemini-2.0-flash-001"
NEW_GEMINI_MODEL = "gemini-2.5-flash-preview-05-20"
REASON_GEMINI_MODEL = "gemini-2.5-pro-preview-05-06"
LITE_GEMINI_MODEL = "gemini-2.0-flash-lite-001"

# API Keys for external services
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY") # For Google Maps and Places APIs
FOURSQUARE_API_KEY = os.getenv("FOURSQUARE_API_KEY") # For Foursquare API
YELP_API_KEY = os.getenv("YELP_API_KEY") # For Yelp Fusion API
BESTTIME_API_KEY = os.getenv("BESTTIME_API_KEY") # For BestTime API

if not GOOGLE_CLOUD_PROJECT:
    raise ValueError("GCP_PROJECT_ID environment variable not set.")
if not GOOGLE_MAPS_API_KEY:
   print("Warning: GOOGLE_MAPS_API_KEY is not set. Maps and Places features might fail.")
if not FOURSQUARE_API_KEY:
   print("Warning: FOURSQUARE_API_KEY is not set. Foursquare features might fail.")
if not YELP_API_KEY:
   print("Warning: YELP_API_KEY is not set. Yelp features might fail.")
if not BESTTIME_API_KEY:
   print("Warning: BESTTIME_API_KEY is not set. BestTime features might fail.")