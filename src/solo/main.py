import os
import uvicorn
from google.adk.cli.fast_api import get_fast_api_app

# Get the directory where main.py is located
AGENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Session DB URL - using SQLite for simplicity (you can switch to Firestore)
SESSION_DB_URL = os.environ.get("SESSION_DB_URL", "sqlite:///./sessions.db")

# CORS configuration for web interface
ALLOWED_ORIGINS = [
    "http://localhost",
    "http://localhost:8080", 
    "http://localhost:3000",  # Common for React dev
    "http://localhost:4200",  # Angular dev server
    "*"  # For development - restrict in production
]

# Set web=True if you intend to serve a web interface, False otherwise
SERVE_WEB_INTERFACE = True

# Environment variables for Google Cloud and APIs
required_env_vars = [
    "GOOGLE_CLOUD_PROJECT",
    "GOOGLE_CLOUD_LOCATION", 
    "GOOGLE_GENAI_USE_VERTEXAI"
]

# Validate environment variables
missing_vars = [var for var in required_env_vars if not os.environ.get(var)]
if missing_vars:
    print(f"Warning: Missing environment variables: {missing_vars}")

# Call the function to get the FastAPI app instance
# Ensure the agent directory name matches your agent folder structure
app = get_fast_api_app(
    agents_dir=AGENT_DIR,
    session_service_uri=SESSION_DB_URL,
    allow_origins=ALLOWED_ORIGINS,
    web=SERVE_WEB_INTERFACE,
)

# Add health check endpoint for Cloud Run
@app.get("/health")
async def health_check():
    """Health check endpoint for Cloud Run and load balancers."""
    return {
        "status": "healthy",
        "service": "adk-multi-agent-service",
        "version": "1.0.0"
    }

# Add environment info endpoint (useful for debugging)
@app.get("/info")
async def service_info():
    """Service information endpoint."""
    return {
        "service": "ADK Multi-Agent System",
        "features": [
            "OpenAPIToolset (Foursquare, BestTime, Yelp)",
            "MCPToolset (Google Maps)",
            "Authentication (HTTPBearer)",
            "Multiple External APIs"
        ],
        "project": os.environ.get("GOOGLE_CLOUD_PROJECT", "not-set"),
        "location": os.environ.get("GOOGLE_CLOUD_LOCATION", "not-set"),
        "vertex_ai": os.environ.get("GOOGLE_GENAI_USE_VERTEXAI", "not-set")
    }

if __name__ == "__main__":
    # Use the PORT environment variable provided by Cloud Run, defaulting to 8080
    port = int(os.environ.get("PORT", 8080))
    
    print(f"Starting ADK Multi-Agent Service on port {port}")
    print(f"Agent directory: {AGENT_DIR}")
    print(f"Session DB: {SESSION_DB_URL}")
    print(f"Web interface: {SERVE_WEB_INTERFACE}")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=port,
        log_level="info"
    )