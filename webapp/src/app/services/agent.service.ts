import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, BehaviorSubject, throwError, of, timer } from 'rxjs';
import {
  catchError,
  map,
  tap,
  switchMap,
  delay,
  take,
  retry,
  mergeMap,
} from 'rxjs/operators';
import { environment } from '../../environments/environment';
import { v4 as uuidv4 } from 'uuid';
import e from 'express';

export interface AgentMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp?: Date;
}

export interface AgentResponse {
  content: string;
  restaurants?: RestaurantData[];
  agentLogs?: string[];
  status: 'success' | 'error' | 'processing';
  error?: string;
  sessionId?: string;
}

export interface SessionInfo {
  sessionId: string;
  createdAt: Date;
  isActive: boolean;
}

export interface RestaurantData {
  rank: number;
  place_id: string;
  name: string;
  formatted_address: string;
  coordinates: {
    latitude: number;
    longitude: number;
  };
  contact: {
    phone: string | null;
    website: string | null;
  };
  ratings: {
    google_rating: number;
    google_review_count: number;
    yelp_rating: number;
    yelp_review_count: number;
  };
  pricing: {
    price_level: number;
    price_symbol: string;
    fits_budget: boolean;
  };
  cuisine_and_features: {
    primary_cuisine: string;
    secondary_cuisines: string[];
    dietary_options: string[];
    key_amenities: string[];
    service_options: string[];
  };
  timing: {
    currently_open: boolean;
    hours_today: string;
    best_times_to_visit: string[];
    current_busyness: string | null;
    peak_days: string[];
  };
  highlights: {
    why_recommended: string;
    special_items: string[];
    standout_features: string[];
    review_sentiment: string;
    review_summary: string;
  };
  media: {
    primary_image: string | null;
    image_alt_text: string;
  };
  match_score: number;
  preference_alignment: {
    cuisine_match: string;
    price_match: string;
    location_convenience: string;
    amenity_satisfaction: string;
  };
  potential_concerns: string[];
  position?: { lat: number; lng: number };
}

export interface AgentConfig {
  isLocalTesting: boolean;
  localUrl?: string;
  deployedUrl?: string;
  apiKey?: string;
  projectId?: string;
  region?: string;
  agentId?: string;
}

@Injectable({
  providedIn: 'root',
})
export class AgentService {
  private conversationHistory: AgentMessage[] = [];
  private agentLogsSubject = new BehaviorSubject<string[]>([]);
  public agentLogs$ = this.agentLogsSubject.asObservable();

  // Session management
  private currentSessionSubject = new BehaviorSubject<SessionInfo | null>(null);
  public currentSession$ = this.currentSessionSubject.asObservable();
  private currentSessionId: string | null = null;

  // ADK specific properties
  private userId: string = `u_${uuidv4()}`; // Generate unique user ID per browser session
  private agentName: string = 'conversational_agent'; // Your agent folder name

  private config: AgentConfig = {
    isLocalTesting: false, // Set to false when deploying to production
    localUrl: '', // Using proxy, so no need for full URL
    deployedUrl: environment.agentUrl || '', // Set in environment
    projectId: environment.projectId || '',
    region: environment.region || 'us-central1',
  };

  constructor(private http: HttpClient) {
    // Debug configuration on startup
    console.log('🔧 Forkcast Agent Service Configuration:');
    console.log('- Local Testing:', this.config.isLocalTesting);
    console.log('- Agent Name:', this.agentName);
    console.log('- User ID:', this.userId);
    console.log(
      '- Environment:',
      environment.production ? 'Production' : 'Development'
    );
  }

  /**
   * Send a message to the ADK agent system (creates session if needed)
   */
  sendMessage(
    userMessage: string,
    userLocation?: { lat: number; lng: number },
    conversationId?: string
  ): Observable<AgentResponse> {
    const message: AgentMessage = {
      role: 'user',
      content: userMessage,
      timestamp: new Date(),
    };

    this.conversationHistory.push(message);

    // Check if we have an active session, create one if not
    if (!this.currentSessionId) {
      this.addAgentLog('🔄 Forkcast: Creating new session...');
      return this.createSession().pipe(
        switchMap((sessionInfo) => {
          return this.sendQueryToSession(
            message,
            userLocation,
            sessionInfo.sessionId
          );
        }),
        catchError((error) => {
          this.addAgentLog('❌ Forkcast: Failed to create session');
          return this.handleError(error);
        })
      );
    } else {
      // Use existing session
      return this.sendQueryToSession(
        message,
        userLocation,
        this.currentSessionId
      );
    }
  }
  private getProductionUrl(partyMode: string): string {
    switch (partyMode) {
      case 'solo':
        return environment.soloAgentApi;
      case 'guest':
        return environment.guestAgentApi;
      case 'host':
        return environment.hostAgentApi;
      default:
        return environment.soloAgentApi;
    }
  }

  /**
   * Get party mode from localStorage
   */
  private getPartyMode(): 'solo' | 'host' | 'guest' {
    try {
      const partyModeData = localStorage.getItem('partyMode');
      if (partyModeData) {
        const partyMode = JSON.parse(partyModeData);
        return partyMode.mode || 'solo';
      }
    } catch (error) {
      console.warn('Could not parse partyMode from localStorage:', error);
    }
    return 'solo'; // Default fallback
  }

  /**
   * Build the full URL for API calls - FIXED VERSION
   */
  private buildApiUrl(endpoint: string): string {
    const partyMode = this.getPartyMode();
    if (this.config.isLocalTesting) {
      // Handle different endpoint patterns
      if (endpoint.startsWith('apps/')) {
        // For session creation: apps/conversational_agent/users/u_123/sessions/s_123
        // Result: /apps/solo/conversational_agent/users/u_123/sessions/s_123
        return `/apps/${partyMode}/${endpoint.substring(5)}`;
      } else if (endpoint === 'run') {
        // For queries: run
        // Result: /run/solo
        return `/run/${partyMode}`;
      } else if (endpoint === 'run_sse') {
        // For SSE queries: run_sse
        // Result: /run_sse/solo
        return `/run_sse/${partyMode}`;
      } else {
        // Fallback for other patterns
        return `/${endpoint}/${partyMode}`;
      }
    } else {
      const baseUrl = this.getProductionUrl(partyMode);
      // For production, just append the endpoint to the base URL
      return `${baseUrl}/${endpoint}`;
    }
  }

  private createSession(): Observable<SessionInfo> {
    const sessionId = `s_${uuidv4()}`;
    const url = this.buildApiUrl(
      `apps/${this.agentName}/users/${this.userId}/sessions/${sessionId}`
    );
    const headers = this.buildHeaders();

    const requestBody = {};

    console.log('📤 Session ID:', sessionId);
    console.log('📤 User ID:', this.userId);
    console.log('📤 Request body JSON:', JSON.stringify(requestBody, null, 2));

    return this.http.post<any>(url, requestBody, { headers }).pipe(
      map(
        (response) => {
          console.log('📥 Session created:', response);

          const sessionInfo: SessionInfo = {
            sessionId: sessionId,
            createdAt: new Date(),
            isActive: true,
          };

          this.currentSessionId = sessionId;
          this.currentSessionSubject.next(sessionInfo);

          return sessionInfo;
        },
        catchError((error) => {
          console.error('❌ Session creation failed:', error);
          console.error('❌ Error details:', error.error);
          throw error;
        })
      )
    );
  }

  /**
   * Send query to existing session using SSE endpoint
   */
  private sendQueryToSession(
    message: AgentMessage,
    userLocation?: { lat: number; lng: number },
    sessionId?: string
  ): Observable<AgentResponse> {
    const sessionIdToUse = sessionId || this.currentSessionId;

    if (!sessionIdToUse) {
      return throwError(() => new Error('No active session available'));
    }

    // Log the request details on once
    if (this.conversationHistory.length === 1) {
      this.addAgentLog(`🆕 Starting new conversation...`);
      this.addAgentLog(
        `📍 Location: ${
          userLocation
            ? `${userLocation.lat.toFixed(4)}, ${userLocation.lng.toFixed(4)}`
            : 'Not provided'
        }`
      );
      this.addAgentLog(`🆔 Using Session: ${sessionIdToUse}`);
    }

    // append the party_code and user_id to the message
    const partyModeData = localStorage.getItem('partyMode');
    let userName: string | undefined = undefined;
    let partyCode: string | undefined = undefined;

    if (partyModeData) {
      try {
        const partyMode = JSON.parse(partyModeData);
        userName = partyMode.userName;
        partyCode = partyMode.partyCode;
      } catch (e) {
        console.warn('Could not parse partyMode from localStorage:', e);
      }
    }

    const extraInfo = ` USE party_code = ${partyCode} , user_id = ${userName}`;
    message.content += extraInfo;

    // Use HTTP for both local and production for now
    return this.sendQueryWithHttp(message, userLocation, sessionIdToUse);
  }

  /**
   * Send query using regular HTTP (updated version)
   */
  private sendQueryWithHttp(
    message: AgentMessage,
    userLocation: { lat: number; lng: number } | undefined,
    sessionId: string
  ): Observable<AgentResponse> {
    const requestBody = {
      appName: this.agentName,
      userId: this.userId,
      sessionId: sessionId,
      newMessage: {
        role: 'user',
        parts: [
          {
            text: message.content,
          },
        ],
      },
    };

    const headers = this.buildHeaders();
    const url = this.buildApiUrl('run');

    return this.http.post<any[]>(url, requestBody, { headers }).pipe(
      tap((response) => {
        console.log('📥 Received query response:', response);
        this.addAgentLog('🤖 Forkcast: Processing complete');
      }),
      map((events) => {
        // Process array of events
        let content = '';
        let restaurants: RestaurantData[] = [];

        events.forEach((event) => {
          if (event.content?.parts) {
            event.content.parts.forEach((part: any) => {
              if (part.text) {
                content += part.text;
              }
              if (part.functionCall) {
                this.addAgentLog(`🔧 Called: ${part.functionCall.name}`);
              }
              if (
                part.functionResponse &&
                part.functionResponse.response?.restaurants
              ) {
                restaurants = part.functionResponse.response.restaurants.map(
                  (r: any) => this.normalizeRestaurantData(r)
                );
              }
            });
          }
        });

        // If content is empty, throw to trigger retry
        if (!content || content.trim() === '') {
          throw new Error('RETRY_EMPTY_CONTENT');
        }

        return {
          content: content,
          restaurants: restaurants,
          status: 'success' as const,
          sessionId: sessionId,
        };
      }),
      retry({
        count: 3,
        delay: (error, retryCount) => {
          // Only retry on our custom empty content error or network errors

          console.error(
            `❌ Query request failed (attempt ${retryCount}), retrying in 5 seconds:`,
            error
          );
          this.addAgentLog(
            `Apologies, this is taking longer than usual. 
            Thank you for your patience... ⏳`
          );
          return timer(5000); // 5 second delay
        },
      }),
      catchError((error) => {
        console.error('❌ Query request failed:', error);
        this.addAgentLog(
          '❌ Forkcast: Error occurred while processing request'
        );
        return this.handleError(error);
      })
    );
  }

  /**
   * Build HTTP headers for the request
   */
  private buildHeaders(): HttpHeaders {
    let headers = new HttpHeaders({
      'Content-Type': 'application/json',
    });

    return headers;
  }

  normalizeRestaurantData(restaurant: any): RestaurantData {
    console.log('🔄 Normalizing restaurant:', restaurant.name);
    console.log('📍 Raw restaurant data:', restaurant);

    try {
      const normalized: RestaurantData = {
        place_id: restaurant.place_id || `temp_${Date.now()}_${Math.random()}`,
        name: restaurant.name || 'Unknown Restaurant',
        rank: restaurant.rank || 1,
        formatted_address:
          restaurant.formatted_address || 'Address not available',

        // Handle coordinates/position
        coordinates: {
          latitude: restaurant.coordinates?.latitude || 0,
          longitude: restaurant.coordinates?.longitude || 0,
        },
        position: {
          lat: restaurant.coordinates?.latitude || 0,
          lng: restaurant.coordinates?.longitude || 0,
        },

        // Contact information
        contact: {
          phone: restaurant.contact?.phone || null,
          website: restaurant.contact?.website || null,
        },

        // Ratings
        ratings: {
          google_rating: restaurant.ratings?.google_rating || 0,
          google_review_count: restaurant.ratings?.google_review_count || 0,
          yelp_rating: restaurant.ratings?.yelp_rating || null,
          yelp_review_count: restaurant.ratings?.yelp_review_count || 0,
        },

        // Pricing
        pricing: {
          price_level: restaurant.pricing?.price_level || 1,
          price_symbol: restaurant.pricing?.price_symbol || '$',
          fits_budget: restaurant.pricing?.fits_budget ?? true,
        },

        // Cuisine and features
        cuisine_and_features: {
          primary_cuisine:
            restaurant.cuisine_and_features?.primary_cuisine || 'Restaurant',
          secondary_cuisines:
            restaurant.cuisine_and_features?.secondary_cuisines || [],
          dietary_options:
            restaurant.cuisine_and_features?.dietary_options || [],
          key_amenities: restaurant.cuisine_and_features?.key_amenities || [],
          service_options: restaurant.cuisine_and_features?.service_options || [
            'Dine-in',
          ],
        },

        // Timing
        timing: {
          currently_open: restaurant.timing?.currently_open ?? true,
          hours_today: restaurant.timing?.hours_today || 'Hours not available',
          best_times_to_visit: restaurant.timing?.best_times_to_visit || [],
          current_busyness: restaurant.timing?.current_busyness || null,
          peak_days: restaurant.timing?.peak_days || [],
        },

        // Highlights
        highlights: {
          why_recommended:
            restaurant.highlights?.why_recommended || 'Recommended for you',
          special_items: restaurant.highlights?.special_items || [],
          standout_features: restaurant.highlights?.standout_features || [],
          review_sentiment:
            restaurant.highlights?.review_sentiment || 'Positive',
          review_summary: restaurant.highlights?.review_summary || null,
        },

        // Media
        media: {
          primary_image: restaurant.media?.primary_image || null,
          image_alt_text:
            restaurant.media?.image_alt_text || `Image of ${restaurant.name}`,
        },

        // Match score and alignment
        match_score: restaurant.match_score || 80,
        preference_alignment: restaurant.preference_alignment || {
          cuisine_match: 'Good',
          price_match: 'Good',
          location_convenience: 'Good',
          amenity_satisfaction: 'Good',
        },

        // Potential concerns
        potential_concerns: restaurant.potential_concerns || [],
      };

      console.log('✅ Successfully normalized:', normalized.name);
      console.log('📍 Final position:', normalized.position);

      return normalized;
    } catch (error) {
      console.error('❌ Error normalizing restaurant:', error);
      console.error('📍 Problem restaurant data:', restaurant);
      throw error;
    }
  }
  /**
   * Handle HTTP errors
   */
  private handleError(error: any): Observable<AgentResponse> {
    console.error('Agent service error:', error);

    let errorMessage =
      'An error occurred while contacting the restaurant search service.';

    if (error.status === 0) {
      if (this.config.isLocalTesting) {
        errorMessage =
          'Unable to connect to the local ADK server. Please ensure:\n' +
          '1. Your ADK server is running on the correct port\n' +
          '2. You started Angular with: ng serve --proxy-config proxy.conf.json\n' +
          '3. The proxy.conf.json file is correctly configured\n' +
          '4. The backend server has CORS enabled';
      } else {
        errorMessage =
          'Unable to connect to the service. Please check your internet connection.';
      }
    } else if (error.status === 404) {
      errorMessage =
        'The ADK server endpoint was not found. Please check if your server is running and the endpoint URL is correct.';
    } else if (error.status >= 400 && error.status < 500) {
      errorMessage = 'There was an issue with your request. Please try again.';
    } else if (error.status >= 500) {
      errorMessage =
        'The service is temporarily unavailable. Please try again later.';
    }

    return throwError(() => ({
      content: errorMessage,
      status: 'error' as const,
      error: error.message || error.toString(),
    }));
  }

  /**
   * Add a log message to the agent logs stream
   */
  private addAgentLog(message: string): void {
    const currentLogs = this.agentLogsSubject.value;
    this.agentLogsSubject.next([...currentLogs, message]);
  }

  /**
   * Generate a unique conversation ID
   */
  private generateConversationId(): string {
    return `conv_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  /**
   * Clear conversation history and create new session
   */
  public clearConversation(): void {
    this.conversationHistory = [];
    this.agentLogsSubject.next([]);

    // Clear current session
    this.currentSessionId = null;
    this.currentSessionSubject.next(null);

    // Generate new user ID for fresh start
    this.userId = `u_${uuidv4()}`;

    this.addAgentLog('🔄 Starting new conversation...');
  }

  /**
   * Get current session information
   */
  public getCurrentSession(): SessionInfo | null {
    return this.currentSessionSubject.value;
  }

  /**
   * Get current session ID
   */
  public getCurrentSessionId(): string | null {
    return this.currentSessionId;
  }

  /**
   * Force create a new session (useful for testing)
   */
  public createNewSession(): Observable<SessionInfo> {
    this.currentSessionId = null;
    this.currentSessionSubject.next(null);
    return this.createSession();
  }

  /**
   * Get conversation history
   */
  public getConversationHistory(): AgentMessage[] {
    return [...this.conversationHistory];
  }

  /**
   * Update configuration (useful for switching between local and deployed)
   */
  public updateConfig(newConfig: Partial<AgentConfig>): void {
    this.config = { ...this.config, ...newConfig };
  }

  /**
   * Check if the service is configured for local testing
   */
  public isLocalTesting(): boolean {
    return this.config.isLocalTesting;
  }

  /**
   * Get current user ID
   */
  public getUserId(): string {
    return this.userId;
  }

  /**
   * Get agent name
   */
  public getAgentName(): string {
    return this.agentName;
  }
}
