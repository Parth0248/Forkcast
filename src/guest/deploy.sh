#!/bin/bash

# ADK Multi-Agent System Deployment Script
# Make sure you have gcloud CLI installed and authenticated

set -e  # Exit on any error

# Configuration variables
SERVICE_NAME="guest-agent-service"
REGION="${GOOGLE_CLOUD_LOCATION:-us-central1}"
PROJECT="${GOOGLE_CLOUD_PROJECT}"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Starting ADK Multi-Agent System Deployment${NC}"

# Check if required environment variables are set
if [ -z "$GOOGLE_CLOUD_PROJECT" ]; then
    echo -e "${RED}❌ Error: GOOGLE_CLOUD_PROJECT environment variable is not set${NC}"
    echo "Please set it with: export GOOGLE_CLOUD_PROJECT=your-project-id"
    exit 1
fi

echo -e "${YELLOW}📋 Deployment Configuration:${NC}"
echo "  Service Name: $SERVICE_NAME"
echo "  Project: $PROJECT"
echo "  Region: $REGION"
echo "  Directory: $(pwd)"

# Verify gcloud is authenticated
echo -e "${YELLOW}🔍 Checking gcloud authentication...${NC}"
if ! gcloud auth list --filter="status:ACTIVE" --format="value(account)" | grep -q "."; then
    echo -e "${RED}❌ Error: No active gcloud authentication found${NC}"
    echo "Please run: gcloud auth login"
    exit 1
fi

# Set the project
echo -e "${YELLOW}⚙️ Setting gcloud project...${NC}"
gcloud config set project $PROJECT

# Enable required APIs
echo -e "${YELLOW}🔧 Enabling required APIs...${NC}"
gcloud services enable \
    cloudbuild.googleapis.com \
    run.googleapis.com \
    artifactregistry.googleapis.com \
    aiplatform.googleapis.com

# Deploy to Cloud Run
echo -e "${YELLOW}🏗️ Deploying to Cloud Run...${NC}"
gcloud run deploy $SERVICE_NAME \
    --source . \
    --region $REGION \
    --project $PROJECT \
    --allow-unauthenticated \
    --set-env-vars="GOOGLE_CLOUD_PROJECT=$PROJECT,GOOGLE_CLOUD_LOCATION=$REGION,GOOGLE_GENAI_USE_VERTEXAI=true"

# Check deployment status
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Deployment successful!${NC}"
    
    # Get the service URL
    SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format="value(status.url)")
    
    echo -e "${GREEN}🌐 Service URL: $SERVICE_URL${NC}"
    echo -e "${GREEN}🔍 Health Check: $SERVICE_URL/health${NC}"
    echo -e "${GREEN}📊 Service Info: $SERVICE_URL/info${NC}"
    
    # Test the health endpoint
    echo -e "${YELLOW}🏥 Testing health endpoint...${NC}"
    sleep 10  # Give the service time to start
    
    if curl -f "$SERVICE_URL/health" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Health check passed!${NC}"
    else
        echo -e "${YELLOW}⚠️ Health check failed, but service might still be starting...${NC}"
    fi
    
else
    echo -e "${RED}❌ Deployment failed!${NC}"
    exit 1
fi

echo -e "${GREEN}🎉 Deployment complete!${NC}"