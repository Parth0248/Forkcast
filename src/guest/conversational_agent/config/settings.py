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

# Vertex AI settings
GOOGLE_GENAI_USE_VERTEXAI = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "TRUE")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

# Storage
STORAGE_BUCKET = os.getenv("STORAGE_BUCKET", "forkcast-guest-agent")

# Vertex AI Gemini Models - hardcoded as these don't come from environment
GEMINI_MODEL = "gemini-2.0-flash-001"
NEW_GEMINI_MODEL = "gemini-2.5-flash"
REASON_GEMINI_MODEL = "gemini-2.5-pro"
LITE_GEMINI_MODEL = "gemini-2.5-flash-lite-preview-06-17"

# Optional API Keys - only if you actually use them

print(f"✅ Settings loaded - Project: {GOOGLE_CLOUD_PROJECT}, Location: {GOOGLE_CLOUD_LOCATION}")
print(f"✅ Using Vertex AI: {GOOGLE_GENAI_USE_VERTEXAI}")
print(f"✅ Storage Bucket: {STORAGE_BUCKET}")