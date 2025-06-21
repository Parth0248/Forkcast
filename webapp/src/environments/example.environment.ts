export const environment = {
  production: false,
  firebase: {
    apiKey: 'your-firebase-api-key',
    authDomain: 'your-firebase-auth-domain',
    projectId: 'your-firebase-project-id',
    storageBucket: 'your-firebase-storage-bucket',
    messagingSenderId: 'your-firebase-messaging-sender-id',
    appId: 'your-firebase-app-id',
    measurementId: 'your-firebase-measurement-id'
  },
  googleMapsApiKey: 'your-google-maps-api-key',
  // Set for local testing
  // localAdkUrl: 'http://localhost:8000/',
  // Set for deployed agents
  agentUrl: 'https://your-region-aiplatform.googleapis.com',
  projectId: 'your-gcp-project-id',
  region: 'your-gcp-region',
  guestAgentApi: 'https://your-guest-agent-url',
  hostAgentApi: 'https://your-host-agent-url',
  soloAgentApi: 'https://your-solo-agent-url',
};
