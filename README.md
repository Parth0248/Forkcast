# Forkcast

**A Multi-Agent AI System to End Group Dining Chaos Forever**

**Deployed Agent:** [https://forkcast-0248.web.app/](https://forkcast-0248.web.app/)

**Demo Video:** [https://www.youtube.com/watch?v=3vYvGvs0boU](https://www.youtube.com/watch?v=3vYvGvs0boU)

**Medium Blog:** [Read more about the project](https://medium.com/@parthmaradia2002/building-forkcast-how-i-created-a-multi-agent-ai-system-to-end-group-dining-chaos-forever-15d7fed85037)

**Technical Report:** [For technical details about the project](https://drive.google.com/file/d/1epGSUitmqgZpShUJ_M3ckl0-Uvw0Phot/view?usp=sharing)

Forkcast is a multi-agent AI system designed to simplify and streamline the process of choosing a restaurant for groups and individuals. It uses a conversational interface to gather preferences and provides personalized recommendations based on a variety of factors including cuisine, price, location, and even real-time busyness data.

## Features

  * **Solo Mode:** Get individual restaurant recommendations based on your preferences.
  * **Party Mode (Host & Guest):**
      * **Host:** Create a party and invite guests to join. The host can see aggregated preferences from all guests and get recommendations for the whole group.
      * **Guest:** Join a party and submit your dining preferences.
  * **Multi-API Integration:** Forkcast leverages Google Maps, Yelp, Foursquare, and BestTime APIs to provide comprehensive information about restaurants.
  * **Conversational AI:** A friendly and intuitive chat interface for a seamless user experience.

## Setup

### Prerequisites

  * Python 3.8+
  * Node.js and npm
  * Google Cloud SDK

### Environment Variables

Before running the application, you need to set up your environment variables. Create a `.env` file in the root of the `src/guest`, `src/host`, and `src/solo` directories and add the following:

```
GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
GOOGLE_CLOUD_LOCATION="your-gcp-region"
GOOGLE_GENAI_USE_VERTEXAI="true"
Maps_API_KEY="your-google-maps-api-key"
FOURSQUARE_API_KEY="your-foursquare-api-key"
YELP_API_KEY="your-yelp-api-key"
BESTTIME_API_KEY="your-besttime-api-key"
```

### Python Environment

It is recommended to use a virtual environment for each of the Python-based agents (guest, host, solo).

1.  **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

2.  **Install the required packages:**

    There are separate `requirements.txt` files for each mode. Install the dependencies for the mode you want to run. For example, for the "guest" mode:

    ```bash
    pip install -r src/guest/requirements.txt
    ```

    Repeat this for `src/host/requirements.txt` and `src/solo/requirements.txt` in their respective virtual environments.

### Webapp Setup

Navigate to the `webapp` directory and install the required npm packages:

```bash
cd webapp
npm install
```

## Running the Application

### Backend API Servers

Open three separate terminals and navigate to the respective agent directories to run the API servers for each mode.

  * **Guest Agent:**

    ```bash
    adk api_server --port 7000
    ```

  * **Solo Agent:**

    ```bash
    adk api_server --port 8000
    ```

  * **Host Agent:**

    ```bash
    adk api_server --port 9000
    ```

### Webapp

In the `webapp` directory, run the following command to start the Angular development server with the proxy configuration:

```bash
npm run proxy
```

This will start the web application, and the `proxy.conf.json` file will handle routing requests to the correct backend server. You can access the application at `http://localhost:4200`.

### Testing Individual Agents

You can test individual agents in a web interface using the `adk web` command. For example, to test the "guest" agent:

```bash
adk web src/guest/conversational_agent/agent.py
```

## Deployment

The project includes deployment scripts for Google Cloud Run in the `src/guest`, `src/host`, and `src/solo` directories (`deploy.sh`). These scripts can be used to deploy the agents to a serverless environment.
