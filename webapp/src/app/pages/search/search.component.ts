// search.component.ts
import {
  Component,
  OnInit,
  OnDestroy,
  ChangeDetectorRef,
  ViewChild,
  ElementRef,
  AfterViewInit,
  inject,
} from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import {
  GoogleMapsModule,
  MapInfoWindow,
  GoogleMap,
} from '@angular/google-maps';
import { Subscription } from 'rxjs';
import { AuthService } from '../../services/auth.service';
import {
  AgentService,
  RestaurantData,
  AgentResponse,
  SessionInfo,
} from '../../services/agent.service';
import { parse } from 'path';
import {
  Firestore,
  collection,
  addDoc,
  query,
  where,
  orderBy,
  limit,
  getDocs,
  onSnapshot,
  Unsubscribe,
} from '@angular/fire/firestore';
// Replace the current Firebase imports with these:
import { AngularFirestore } from '@angular/fire/compat/firestore';
import { AngularFireAuth } from '@angular/fire/compat/auth';
interface ChatMessage {
  sender: 'user' | 'agent' | 'system';
  text: string;
  timestamp?: Date;
  isTyping?: boolean;
}

const USER_LOCATION_KEY = 'forkcast_user_location';

@Component({
  selector: 'app-search',
  standalone: true,
  imports: [CommonModule, FormsModule, GoogleMapsModule],
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.scss'],
})
export class SearchComponent implements OnInit, OnDestroy, AfterViewInit {
  @ViewChild('map') map!: GoogleMap;
  @ViewChild('chatHistoryContainer') chatHistoryContainer!: ElementRef;

  // Chat state
  userMessage: string = '';
  chatHistory: ChatMessage[] = [];
  isProcessingMessage: boolean = false;
  conversationId: string = '';

  // Session management
  currentSession: SessionInfo | null = null;
  showSessionInfo: boolean = true;

  // Map and restaurant state
  restaurants: RestaurantData[] = [];
  selectedRestaurant: RestaurantData | null = null;
  showDirectionsButton: boolean = false;

  // Native Google Maps InfoWindow
  private infoWindow!: google.maps.InfoWindow;
  private markers: google.maps.marker.AdvancedMarkerElement[] = [];

  // SUser Location
  userLocation: { lat: number; lng: number } | undefined = undefined;
  isLoadingLocation: boolean = false;
  locationError: string | null = null;

  private userLocationMarker: google.maps.marker.AdvancedMarkerElement | null =
    null;

  // Subscriptions
  private agentLogsSubscription?: Subscription;
  private sessionSubscription?: Subscription;

  // Party Modes
  partyMode: 'solo' | 'host' | 'guest' = 'solo';
  partyCode?: string;

  // Firestore integration
  private firestoreUnsubscribe: Unsubscribe | null = null;
  private lastFirestoreTimestamp: Date | null = null;

  mapOptions: google.maps.MapOptions = {
    zoom: 13,
    mapId: '4504f8b37365c3d0', // Required for advanced markers
    mapTypeControl: true,
    streetViewControl: false,
    fullscreenControl: true,
    zoomControl: true,
    disableDefaultUI: false,
    gestureHandling: 'cooperative',
    clickableIcons: false, // Disable default POI clicks
    // colorScheme: 'FOLLOW_SYSTEM', // Follow system color scheme
  };

  constructor(
    private authService: AuthService,
    private router: Router,
    private cdr: ChangeDetectorRef,
    private agentService: AgentService
  ) {
    // Expose component instance globally for InfoWindow button callbacks
    (window as any).forkcastComponent = this;
    this.conversationId = this.generateConversationId();
  }

  async ngOnInit() {
    this.isLoadingLocation = true;
    await this.getUserLocation();

    // const mode = localStorage.getItem('partyMode');
    // Try to load user location from localStorage first
    // const storedLocation = localStorage.getItem(USER_LOCATION_KEY);
    // if (storedLocation) {
    //   try {
    //     const parsed = JSON.parse(storedLocation);
    //     if (
    //       parsed &&
    //       typeof parsed.lat === 'number' &&
    //       typeof parsed.lng === 'number'
    //     ) {
    //       this.userLocation = parsed;
    //       this.isLoadingLocation = false;
    //       this.locationError = null;

    //       setTimeout(() => {
    //         if (this.map?.googleMap && this.userLocation) {
    //           this.map.googleMap.setCenter(this.userLocation);
    //           this.createUserLocationMarker();
    //         }
    //       }, 0);
    //     } else {
    //       this.getUserLocation();
    //     }
    //   } catch {
    //     this.getUserLocation();
    //   }
    // } else {
    //   this.getUserLocation();
    // }

    const storedLocation = localStorage.getItem(USER_LOCATION_KEY);
    let initialCenter = { lat: 37.7749, lng: -122.4194 }; // fallback (SF)
    if (storedLocation) {
      try {
        const parsed = JSON.parse(storedLocation);
        if (
          parsed &&
          typeof parsed.lat === 'number' &&
          typeof parsed.lng === 'number'
        ) {
          initialCenter = { lat: parsed.lat, lng: parsed.lng };
        }
      } catch {}
    }

    if (storedLocation) {
      try {
        const parsed = JSON.parse(storedLocation);
        if (
          parsed &&
          typeof parsed.lat === 'number' &&
          typeof parsed.lng === 'number'
        ) {
          this.userLocation = parsed;
          this.isLoadingLocation = false;
          this.locationError = null;
          // Don't set center here, let the template binding handle it
          // Optionally, create marker after map is ready
          setTimeout(() => {
            if (this.map?.googleMap && this.userLocation) {
              this.createUserLocationMarker();
            }
          }, 0);
          // Now, always try to get the latest location in the background
          this.getUserLocation(true); // pass a flag to not update map immediately
        } else {
          this.getUserLocation();
        }
      } catch {
        this.getUserLocation();
      }
    } else {
      this.getUserLocation();
    }

    this.startConversation();
    this.subscribeToAgentLogs();
    this.subscribeToSession();
    this.loadPartyMode();
    this.startPartyRestaurantListener();
  }

  ngOnDestroy() {
    if (this.agentLogsSubscription) {
      this.agentLogsSubscription.unsubscribe();
    }
    if (this.sessionSubscription) {
      this.sessionSubscription.unsubscribe();
    }
    // Clean up Firestore listener
    this.stopPartyRestaurantListener();
  }

  ngAfterViewInit() {
    this.scrollToBottom();
    // Create user location marker after map is ready
    if (!localStorage.getItem(USER_LOCATION_KEY)) {
      this.getUserLocation();
    } else {
      // If we already have location, ensure marker is created after map is ready
      setTimeout(() => {
        this.createUserLocationMarker();
      }, 0);
    }
  }

  private loadPartyMode(): void {
    try {
      const partyData = localStorage.getItem('partyMode');
      if (partyData) {
        const parsed = JSON.parse(partyData);
        this.partyMode = parsed.mode || 'solo';
        this.partyCode = parsed.partyCode;
      }
    } catch (error) {
      console.error('Error loading party mode:', error);
      this.partyMode = 'solo';
    }
  }

  getPartyModeDisplay(): string {
    switch (this.partyMode) {
      case 'host':
        return `Host: ${this.partyCode}`;
      case 'guest':
        return `Guest: ${this.partyCode}`;
      default:
        return 'Solo';
    }
  }

  getPartyModeClass(): string {
    switch (this.partyMode) {
      case 'host':
        return 'party-mode-host';
      case 'guest':
        return 'party-mode-guest';
      default:
        return 'party-mode-solo';
    }
  }

  /**
   * Subscribe to agent logs and display them in chat
   */
  private subscribeToAgentLogs(): void {
    this.agentLogsSubscription = this.agentService.agentLogs$.subscribe(
      (logs) => {
        // Only show the latest log that hasn't been displayed yet
        const currentSystemMessages = this.chatHistory.filter(
          (msg) => msg.sender === 'system'
        ).length;
        if (logs.length > currentSystemMessages) {
          const newLog = logs[logs.length - 1];
          this.chatHistory.push({
            sender: 'system',
            text: newLog,
            timestamp: new Date(),
          });
          this.cdr.detectChanges();
          this.scrollToBottom();
        }
      }
    );
  }

  /**
   * Subscribe to session changes and update UI
   */
  private subscribeToSession(): void {
    this.sessionSubscription = this.agentService.currentSession$.subscribe(
      (session) => {
        this.currentSession = session;
        this.cdr.detectChanges();
      }
    );
  }

  /**
   * Get user's current location
   */
  private async getUserLocation(silentUpdate: boolean = false): Promise<void> {
    if (navigator.geolocation) {
      this.isLoadingLocation = true;

      return new Promise((resolve, reject) => {
        navigator.geolocation.getCurrentPosition(
          async (position) => {
            const newLocation = {
              lat: position.coords.latitude,
              lng: position.coords.longitude,
            };

            localStorage.setItem(
              USER_LOCATION_KEY,
              JSON.stringify(this.userLocation)
            );
            this.isLoadingLocation = false;
            this.locationError = null;

            if (!silentUpdate) {
              this.userLocation = newLocation;
              // The map will center via template binding
              if (this.map?.googleMap) {
                this.map.googleMap.setCenter(this.userLocation);
              }
              // Create user location marker
              await this.createUserLocationMarker();
              this.cdr.detectChanges();
            }
            resolve();
          },
          (error) => {
            this.isLoadingLocation = false;
            this.locationError =
              'Unable to get your location. Using default location.';
            console.error('Geolocation error:', error);
            this.userLocation = undefined;
            this.cdr.detectChanges();
            reject(error);
          },
          {
            enableHighAccuracy: true,
            timeout: 60000,
            maximumAge: 300000,
          }
        );
      });
    }
  }

  private async initializeGoogleMapsComponents() {
    try {
      // Load required libraries
      const { InfoWindow } = (await google.maps.importLibrary(
        'maps'
      )) as google.maps.MapsLibrary;

      // Now we can create the InfoWindow
      this.infoWindow = new InfoWindow({
        maxWidth: 520,
        disableAutoPan: false,
      });
    } catch (error) {
      console.error('Error loading Google Maps libraries:', error);
    }
  }

  private async createUserLocationMarker() {
    // Remove any existing marker
    if (this.userLocationMarker) {
      this.userLocationMarker.map = null;
      this.userLocationMarker = null;
    }

    // Wait for Google Maps libraries
    const { AdvancedMarkerElement } = (await google.maps.importLibrary(
      'marker'
    )) as google.maps.MarkerLibrary;

    if (this.userLocation && this.map?.googleMap) {
      // Create custom marker with logo and "You" badge
      const markerDiv = document.createElement('div');
      markerDiv.style.position = 'relative';
      markerDiv.style.cursor = 'pointer';
      markerDiv.style.transition = 'transform 0.2s ease';

      // Logo image
      const logoImg = document.createElement('img');
      logoImg.src = 'assets/user_icon.png';
      logoImg.width = 60;
      logoImg.height = 60;
      logoImg.alt = 'Your Location';
      // Fallback for logo loading error
      logoImg.onerror = () => {
        logoImg.src =
          'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHZpZXdCb3g9IjAgMCA0MCA0MCIgZmlsbD0ibm9uZSIgeG1zbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iMjAiIGN5PSIyMCIgcj0iMjAiIGZpbGw9IiNlYTQzMzUiLz4KPHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1zbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4PSI4IiB5PSI4Ij4KPHBhdGggZD0iTTExIDl2MmgtMXY3aDJ2LTdoLTF6IiBmaWxsPSJ3aGl0ZSIvPgo8L3N2Zz4KPC9zdmc+';
      };

      // "You" badge
      const youBadge = document.createElement('div');
      youBadge.textContent = 'You';
      youBadge.style.position = 'absolute';
      youBadge.style.bottom = '-15px';
      youBadge.style.right = '10px';
      youBadge.style.background = 'linear-gradient(135deg, #4285f4, #34a853)';
      youBadge.style.color = 'white';
      youBadge.style.borderRadius = '12px';
      youBadge.style.padding = '2px 8px';
      youBadge.style.fontSize = '11px';
      youBadge.style.fontWeight = 'bold';
      youBadge.style.border = '2px solid white';
      youBadge.style.boxShadow = '0 2px 6px rgba(0, 0, 0, 0.3)';
      youBadge.style.display = 'flex';
      youBadge.style.alignItems = 'center';
      youBadge.style.justifyContent = 'center';

      markerDiv.appendChild(logoImg);
      markerDiv.appendChild(youBadge);

      // Add hover effect
      markerDiv.addEventListener('mouseenter', () => {
        markerDiv.style.transform = 'scale(1.1)';
      });
      markerDiv.addEventListener('mouseleave', () => {
        markerDiv.style.transform = 'scale(1)';
      });

      this.userLocationMarker = new AdvancedMarkerElement({
        map: this.map.googleMap,
        position: this.userLocation,
        title: 'Your Location',
        content: markerDiv,
        zIndex: 1000,
        gmpClickable: false,
      });
    }
  }

  startConversation() {
    const environmentInfo = this.agentService.isLocalTesting()
      ? ' (Running in local testing mode)'
      : '';

    this.chatHistory.push({
      sender: 'agent',
      text: `Hello! I'm Forkcast. I'll create a session when you send your first message. What are you in the mood for today?${environmentInfo}`,
      timestamp: new Date(),
    });
  }

  /**
   * Toggle session info display
   */
  toggleSessionInfo(): void {
    this.showSessionInfo = !this.showSessionInfo;
  }

  /**
   * Create a new session manually (for testing)
   */
  createNewSession(): void {
    this.chatHistory.push({
      sender: 'system',
      text: 'Creating new session...',
      timestamp: new Date(),
    });

    this.agentService.createNewSession().subscribe({
      next: (session) => {
        this.chatHistory.push({
          sender: 'system',
          text: `New session created: ${session.sessionId}`,
          timestamp: new Date(),
        });
        this.cdr.detectChanges();
        this.scrollToBottom();
      },
      error: (error) => {
        this.chatHistory.push({
          sender: 'system',
          text: 'Failed to create new session. Please try again.',
          timestamp: new Date(),
        });
        console.error('Session creation error:', error);
        this.cdr.detectChanges();
        this.scrollToBottom();
      },
    });
  }
  private firestore = inject(Firestore);

  private async saveRestaurantsToFirestore(
    restaurants: RestaurantData[]
  ): Promise<void> {
    try {
      const partyModeData = localStorage.getItem('partyMode');
      let partyCode: string | undefined = undefined;

      if (partyModeData) {
        try {
          const partyMode = JSON.parse(partyModeData);
          partyCode = partyMode.partyCode;
        } catch (e) {
          console.warn('Could not parse partyMode from localStorage:', e);
        }
      }

      if (partyCode) {
        const restaurantsCollection = collection(
          this.firestore,
          'party_restaurants'
        );
        await addDoc(restaurantsCollection, {
          partyCode: partyCode,
          restaurants: restaurants,
          timestamp: new Date(),
          createdBy: this.agentService.getUserId(),
        });
        console.log('✅ Restaurants saved to Firestore for party:', partyCode);
      }
    } catch (error) {
      console.error('❌ Error saving restaurants to Firestore:', error);
    }
  }

  /**
   * Retrieve latest restaurants from Firestore for party
   */
  private async getRestaurantsFromFirestore(): Promise<RestaurantData[]> {
    try {
      const partyModeData = localStorage.getItem('partyMode');
      let partyCode: string | undefined = undefined;

      if (partyModeData) {
        try {
          const partyMode = JSON.parse(partyModeData);
          partyCode = partyMode.partyCode;
        } catch (e) {
          console.warn('Could not parse partyMode from localStorage:', e);
        }
      }

      if (partyCode) {
        const restaurantsCollection = collection(
          this.firestore,
          'party_restaurants'
        );

        const q = query(
          restaurantsCollection,
          where('partyCode', '==', partyCode),
          orderBy('timestamp', 'desc'),
          limit(1)
        );
        // const q = query(
        //   restaurantsCollection,
        //   where('partyCode', '==', partyCode)
        // );

        const querySnapshot = await getDocs(q);
        if (!querySnapshot.empty) {
          const doc = querySnapshot.docs[0];
          const data = doc.data();
          console.log(
            '✅ Retrieved restaurants from Firestore for party:',
            partyCode
          );
          return data['restaurants'] || [];
        }
      }

      return [];
    } catch (error) {
      console.error('❌ Error retrieving restaurants from Firestore:', error);
      return [];
    }
  }

  /**
   * Start listening for real-time restaurant updates for party members
   */
  private startPartyRestaurantListener(): void {
    const partyModeData = localStorage.getItem('partyMode');
    let partyCode: string | undefined = undefined;

    if (partyModeData) {
      try {
        const partyMode = JSON.parse(partyModeData);
        partyCode = partyMode.partyCode;
      } catch (e) {
        console.warn('Could not parse partyMode from localStorage:', e);
      }
    }

    // Only start listener if we're in a party (host or guest)
    if (partyCode && this.partyMode !== 'solo') {
      const restaurantsCollection = collection(
        this.firestore,
        'party_restaurants'
      );
      const q = query(
        restaurantsCollection,
        where('partyCode', '==', partyCode),
        orderBy('timestamp', 'desc'),
        limit(1)
      );

      this.firestoreUnsubscribe = onSnapshot(
        q,
        (querySnapshot) => {
          if (!querySnapshot.empty) {
            const doc = querySnapshot.docs[0];
            const data = doc.data();
            const timestamp = data['timestamp']?.toDate();

            // Only update if this is newer than what we've already processed
            if (
              !this.lastFirestoreTimestamp ||
              timestamp > this.lastFirestoreTimestamp
            ) {
              this.lastFirestoreTimestamp = timestamp;
              const firestoreRestaurants = data['restaurants'] || [];
              const createdBy = data['createdBy'];

              if (firestoreRestaurants.length > 0) {
                // Don't update if this user created the results (avoid duplicate updates)
                if (createdBy !== this.agentService.getUserId()) {
                  this.updateRestaurantsFromParty(
                    firestoreRestaurants,
                    createdBy
                  );
                }
              }
            }
          }
        },
        (error) => {
          console.error('❌ Error listening to party restaurants:', error);
        }
      );

      console.log(
        '👥 Started listening for party restaurant updates:',
        partyCode
      );
    }
  }

  /**
   * Update restaurants display when party member finds new results
   */
  private updateRestaurantsFromParty(
    restaurants: RestaurantData[],
    createdBy: string
  ): void {
    this.restaurants = restaurants;

    // Add system message to chat
    this.chatHistory.push({
      sender: 'system',
      text: `🎉 Party member found ${restaurants.length} restaurants! Check them out on the map.`,
      timestamp: new Date(),
    });

    // Update map markers
    setTimeout(() => {
      this.createNativeMarkersWithListeners();
      this.cdr.detectChanges();
    }, 500);

    this.cdr.detectChanges();
    this.scrollToBottom();

    console.log('👥 Updated restaurants from party member:', createdBy);
  }

  /**
   * Stop listening for party updates
   */
  private stopPartyRestaurantListener(): void {
    if (this.firestoreUnsubscribe) {
      this.firestoreUnsubscribe();
      this.firestoreUnsubscribe = null;
      console.log('👥 Stopped listening for party restaurant updates');
    }
  }
  /**
   * Handle user message and send to agent service
   */
  handleUserMessage() {
    if (!this.userMessage.trim() || this.isProcessingMessage) return;

    // Add user message to chat
    this.chatHistory.push({
      sender: 'user',
      text: this.userMessage,
      timestamp: new Date(),
    });

    const userQuery = this.userMessage;
    this.userMessage = '';
    this.isProcessingMessage = true;

    this.cdr.detectChanges();
    this.scrollToBottom();

    // Add typing indicator
    const typingMessage: ChatMessage = {
      sender: 'system',
      text: 'Forkcast is thinking...',
      isTyping: true,
      timestamp: new Date(),
    };
    this.chatHistory.push(typingMessage);
    this.cdr.detectChanges();
    this.scrollToBottom();

    // Send to agent service
    this.agentService
      .sendMessage(userQuery, this.userLocation, this.conversationId)
      .subscribe({
        next: (response: AgentResponse) => {
          this.handleAgentResponse(response);
        },
        error: (error) => {
          this.handleAgentError(error);
        },
        complete: () => {
          this.isProcessingMessage = false;
        },
      });
  }

  /**
   * Handle agent error
   */
  private handleAgentError(error: any, isRetry: boolean = false): void {
    // Remove typing indicator
    const typingIndex = this.chatHistory.findIndex((msg) => msg.isTyping);
    if (typingIndex !== -1) {
      this.chatHistory.splice(typingIndex, 1);
    }

    // Detect server error (500) and extract details if available
    let errorCode = '';
    let errorStatus = '';
    let errorMessage =
      error.content ||
      'Sorry, I encountered an error while searching for restaurants. Please try again.';

    // Try to extract error code and status from error object
    if (error && error.error) {
      if (error.error.code) errorCode = error.error.code;
      if (error.error.status) errorStatus = error.error.status;
      if (error.error.message) errorMessage = error.error.message;
    } else if (typeof error === 'object' && error.status) {
      errorCode = error.status;
      errorStatus = error.statusText || '';
    }

    // If it's a 500 error, show a detailed message and retry with "Continue"
    if (
      (errorCode === '500' ||
        errorStatus === 'INTERNAL' ||
        errorMessage.includes('500')) &&
      !isRetry
    ) {
      this.chatHistory.push({
        sender: 'agent',
        text: `❌ Forkcast: Error ${errorCode || 500} (${
          errorStatus || 'Internal Server Error'
        }): ${errorMessage}\n\nThe service is temporarily unavailable. Retrying...`,
        timestamp: new Date(),
      });
      this.cdr.detectChanges();
      this.scrollToBottom();

      // Retry with "Continue" after a short delay (e.g., 1.5 seconds)
      setTimeout(() => {
        this.chatHistory.push({
          sender: 'user',
          text: 'Continue',
          timestamp: new Date(),
        });
        this.cdr.detectChanges();
        this.scrollToBottom();

        this.isProcessingMessage = true;
        this.agentService
          .sendMessage('Continue', this.userLocation, this.conversationId)
          .subscribe({
            next: (response: AgentResponse) => {
              this.handleAgentResponse(response);
            },
            error: (err) => {
              // If retry also fails, show a final error message (no further retry)
              this.handleAgentError(err, true);
            },
            complete: () => {
              this.isProcessingMessage = false;
            },
          });
      }, 1500);
      return;
    }

    // For other errors or if already retried, show a generic error message
    this.chatHistory.push({
      sender: 'agent',
      text: errorMessage,
      timestamp: new Date(),
    });

    console.error('Agent error:', error);
    this.cdr.detectChanges();
    this.scrollToBottom();
  }

  // --- Robust agent response handler (replaces old handleAgentResponse) ---
  private async handleAgentResponse(response: AgentResponse): Promise<void> {
    // Remove typing indicator
    const typingIndex = this.chatHistory.findIndex((msg) => msg.isTyping);
    if (typingIndex !== -1) {
      this.chatHistory.splice(typingIndex, 1);
    }
    console.log('🔍 Processing response:', response);
    if (!response?.content) {
      this.addErrorMessage('Empty response received');
      return;
    }
    // Accept direct object (like your JSON above) or string
    let content: any = response.content;
    let extractedData: any = null;
    try {
      if (
        typeof content === 'object' &&
        content.final_results?.recommendations
      ) {
        extractedData = content;
      } else if (typeof content === 'string') {
        extractedData = this.robustJsonExtraction(content);
      }
      // fallback: try direct parse if not found
      if (!extractedData && typeof content === 'string') {
        try {
          extractedData = JSON.parse(content);
        } catch {}
      }
    } catch (err) {
      console.error('❌ Error extracting data:', err);
    }
    if (extractedData && this.isValidRestaurantData(extractedData)) {
      await this.processRestaurantsRobustly(extractedData);
    } else {
      this.processTextMessage(
        typeof content === 'string' ? content : JSON.stringify(content)
      );
    }
    this.cdr.detectChanges();
    this.scrollToBottom();
  }

  /**
   * Try multiple strategies to extract JSON from agent response.
   */
  private robustJsonExtraction(content: string): any {
    const strategies = [
      () => this.parseFullContentAsJson(content),
      () => this.extractJsonFromMixedContent(content),
      () => this.extractFinalResultsJson(content),
      () => this.extractAnyValidJson(content),
      () => this.parseCleanedJson(content),
    ];
    for (const strategy of strategies) {
      try {
        const result = strategy();
        if (result && this.isValidRestaurantData(result)) {
          return result;
        }
      } catch {
        continue;
      }
    }
    return null;
  }
  private parseFullContentAsJson(content: string): any {
    if (content.trim().startsWith('{') && content.trim().endsWith('}')) {
      return JSON.parse(content);
    }
    return null;
  }
  private extractJsonFromMixedContent(content: string): any {
    const match = content.match(/\{[\s\S]*\}/);
    if (match) return JSON.parse(match[0]);
    return null;
  }
  private extractFinalResultsJson(content: string): any {
    const match = content.match(/"final_results"\s*:\s*\{[\s\S]*?\}\s*[,}]/);
    if (match) {
      const jsonStr = `{${match[0]}}`;
      return JSON.parse(jsonStr);
    }
    return null;
  }
  private extractAnyValidJson(content: string): any {
    try {
      const start = content.indexOf('{');
      const end = content.lastIndexOf('}');
      if (start !== -1 && end > start) {
        return JSON.parse(content.substring(start, end + 1));
      }
    } catch {}
    return null;
  }
  private parseCleanedJson(content: string): any {
    try {
      const cleaned = this.enhancedJsonCleaning(content);
      return JSON.parse(cleaned);
    } catch {
      return null;
    }
  }
  private isValidRestaurantData(data: any): boolean {
    if (!data) return false;
    if (
      data.final_results?.recommendations &&
      Array.isArray(data.final_results.recommendations)
    ) {
      return data.final_results.recommendations.some(
        (r: any) => r.name || r.place_id
      );
    }
    if (Array.isArray(data.restaurants)) {
      return data.restaurants.some((r: any) => r.name || r.place_id);
    }
    if (Array.isArray(data)) {
      return data.some((r: any) => r.name || r.place_id);
    }
    return false;
  }
  private async processRestaurantsRobustly(extractedData: any): Promise<void> {
    try {
      let restaurants: any[] = [];
      let summary = '';
      if (extractedData.final_results?.recommendations) {
        restaurants = extractedData.final_results.recommendations;
        summary = this.extractSummaryFromFinalResults(extractedData);
      } else if (extractedData.restaurants) {
        restaurants = extractedData.restaurants;
        summary = extractedData.summary || '';
      } else if (Array.isArray(extractedData)) {
        restaurants = extractedData;
      } else {
        throw new Error('Unknown restaurant data structure');
      }
      const normalizedRestaurants = await this.normalizeRestaurantsWithLogging(
        restaurants
      );
      if (normalizedRestaurants.length === 0) {
        throw new Error('No valid restaurants after normalization');
      }
      if (summary) {
        this.chatHistory.push({
          sender: 'agent',
          text: summary,
          timestamp: new Date(),
        });
      }
      await this.saveAndSyncRestaurants(normalizedRestaurants);
      this.chatHistory.push({
        sender: 'agent',
        text: `🗺️ I found ${normalizedRestaurants.length} restaurants! Check them out on the map.`,
        timestamp: new Date(),
      });
      setTimeout(() => {
        this.createNativeMarkersWithListeners();
        this.cdr.detectChanges();
      }, 500);
    } catch (error) {
      console.error('❌ Error processing restaurants:', error);
      this.addErrorMessage(
        'Found restaurants but had trouble displaying them. The data might be incomplete.'
      );
    }
  }
  private async normalizeRestaurantsWithLogging(
    restaurants: any[]
  ): Promise<RestaurantData[]> {
    const normalized: RestaurantData[] = [];
    for (const r of restaurants) {
      try {
        const norm = this.agentService.normalizeRestaurantData
          ? this.agentService.normalizeRestaurantData(r)
          : this.enhancedRestaurantNormalization(r);
        if (this.basicRestaurantValidation(norm)) {
          normalized.push(norm);
        }
      } catch (error) {
        console.warn('Failed to normalize restaurant:', error, r);
        continue;
      }
    }
    return normalized;
  }
  private basicRestaurantValidation(restaurant: RestaurantData): boolean {
    return !!(
      restaurant?.name &&
      restaurant?.coordinates &&
      typeof restaurant.coordinates.latitude === 'number' &&
      typeof restaurant.coordinates.longitude === 'number' &&
      !isNaN(restaurant.coordinates.latitude) &&
      !isNaN(restaurant.coordinates.longitude) &&
      restaurant.coordinates.latitude >= -90 &&
      restaurant.coordinates.latitude <= 90 &&
      restaurant.coordinates.longitude >= -180 &&
      restaurant.coordinates.longitude <= 180
    );
  }
  private extractSummaryFromFinalResults(data: any): string {
    const summaryPaths = [
      data.summary?.search_quality_notes,
      data.summary?.alternative_suggestions,
      data.final_results?.summary?.search_quality_notes,
      data.final_results?.summary?.alternative_suggestions,
      data.summary,
    ];
    for (const s of summaryPaths) {
      if (s && typeof s === 'string' && s.trim()) return s.trim();
    }
    const count = data.final_results?.recommendations?.length || 0;
    return `I found ${count} great restaurants that match your preferences!`;
  }
  private enhancedJsonCleaning(jsonString: string): string {
    return jsonString
      .replace(/^\uFEFF/, '')
      .replace(/[\u0000-\u001F\u007F-\u009F]/g, '')
      .replace(/^.*?(\{.*\}).*$/s, '$1')
      .replace(/```json\s*/gi, '')
      .replace(/```\s*$/gi, '')
      .replace(/:\s*"([^"]*)\n([^"]*)"([^,}\]]*)/g, ': "$1 $2"$3')
      .replace(/:\s*'([^']*)'/g, ': "$1"')
      .replace(/,(\s*[}\]])/g, '$1')
      .replace(/([}\]])(\s*)([\{\[])/g, '$1,$2$3')
      .replace(/:\s*undefined/g, ': null')
      .replace(/:\s*None/g, ': null')
      .replace(/:\s*True/g, ': true')
      .replace(/:\s*False/g, ': false')
      .replace(/\[\s*,/g, '[')
      .replace(/,\s*\]/g, ']')
      .trim();
  }
  private enhancedRestaurantNormalization(r: any): RestaurantData {
    return {
      place_id: r.place_id || `fallback_${Date.now()}_${Math.random()}`,
      name: r.name || 'Unknown',
      rank: r.rank || 1,
      formatted_address: r.formatted_address || 'Address not available',
      coordinates: r.coordinates || { latitude: 0, longitude: 0 },
      position: r.position || {
        lat: r.coordinates?.latitude || 0,
        lng: r.coordinates?.longitude || 0,
      },
      contact: r.contact || { phone: null, website: null },
      ratings: r.ratings || {
        google_rating: 0,
        google_review_count: 0,
        yelp_rating: r.ratings?.yelp_rating || null, // Explicitly handle null
        yelp_review_count: r.ratings?.yelp_review_count || null, // Explicitly handle null
      },
      pricing: r.pricing || {
        price_level: 2,
        price_symbol: '$$',
        fits_budget: true,
      },
      cuisine_and_features: r.cuisine_and_features || {
        primary_cuisine: 'Restaurant',
        secondary_cuisines: [],
        dietary_options: [],
        key_amenities: [],
        service_options: ['Dine-in'],
      },
      timing: r.timing || {
        currently_open: true,
        hours_today: 'Hours not available',
        best_times_to_visit: [],
        current_busyness: null,
        peak_days: [],
      },
      highlights: r.highlights || {
        why_recommended: 'Found in search results',
        special_items: [],
        standout_features: [],
        review_sentiment: 'Positive',
        review_summary: '',
      },
      media: r.media || {
        primary_image: null,
        image_alt_text: `Image of ${r.name || 'Unknown'}`,
      },
      match_score: r.match_score || 75,
      preference_alignment: r.preference_alignment || {
        cuisine_match: 'Good',
        price_match: 'Good',
        location_convenience: 'Good',
        amenity_satisfaction: 'Good',
      },
      potential_concerns: r.potential_concerns || [],
    };
  }
  // --- Helper for robust handler compatibility ---
  private addErrorMessage(message: string): void {
    this.chatHistory.push({
      sender: 'agent',
      text: `❌ ${message}`,
      timestamp: new Date(),
    });
    this.cdr.detectChanges();
    this.scrollToBottom();
  }
  private processTextMessage(content: string): void {
    this.chatHistory.push({
      sender: 'agent',
      text: content,
      timestamp: new Date(),
    });
    this.cdr.detectChanges();
    this.scrollToBottom();
  }
  private async saveAndSyncRestaurants(
    restaurants: RestaurantData[]
  ): Promise<void> {
    try {
      await this.saveRestaurantsToFirestore(restaurants);
      const firestoreRestaurants = await this.getRestaurantsFromFirestore();
      if (firestoreRestaurants.length > 0) {
        this.restaurants = firestoreRestaurants;
      } else {
        this.restaurants = restaurants;
      }
    } catch {
      this.restaurants = restaurants;
    }
  }

  async onMarkerClick(restaurant: RestaurantData) {
    // Initialize InfoWindow if not already done
    if (!this.infoWindow) {
      await this.initializeGoogleMapsComponents();
    }

    this.selectedRestaurant = restaurant;
    this.showDirectionsButton = false;

    // Close any existing info window
    this.infoWindow.close();

    // Set HTML content and open info window
    this.infoWindow.setContent(this.getInfoWindowContent(restaurant));

    // Add system message
    this.chatHistory.push({
      sender: 'system',
      text: `Showing details for ${restaurant.name}...`,
      timestamp: new Date(),
    });
    this.scrollToBottom();
  }

  private getInfoWindowContent(restaurant: RestaurantData): string {
    const stars = this.getGoogleStarIcons(restaurant.ratings.google_rating);
    const statusClass = restaurant.timing.currently_open ? 'open' : 'closed';
    const statusText = restaurant.timing.currently_open ? 'Open Now' : 'Closed';

    // Build cuisine display exactly as shown in the design
    const cuisineDisplay = `${restaurant.cuisine_and_features.primary_cuisine}${
      restaurant.cuisine_and_features.secondary_cuisines.length > 0
        ? ' ' + restaurant.cuisine_and_features.secondary_cuisines.join(' ')
        : ''
    }`;

    // Build contact info
    const phoneRow = restaurant.contact.phone
      ? `<li><span class="icon">📞</span><a href="tel:${restaurant.contact.phone}">${restaurant.contact.phone}</a></li>`
      : '';

    const websiteRow = restaurant.contact.website
      ? `<li><span class="icon">🌐</span><a href="${restaurant.contact.website}" target="_blank">Visit Website</a></li>`
      : '';

    // Build timing info
    const bestTimes =
      restaurant.timing.best_times_to_visit.length > 0
        ? restaurant.timing.best_times_to_visit.join(', ')
        : 'Anytime';

    const peakDays =
      restaurant.timing.peak_days.length > 0
        ? restaurant.timing.peak_days
            .map((day) => day.charAt(0).toUpperCase() + day.slice(1))
            .join(', ')
        : 'None';

    // Build service options - capitalize properly
    const serviceOptions =
      restaurant.cuisine_and_features.service_options.length > 0
        ? restaurant.cuisine_and_features.service_options
            .map((option) => {
              return option
                .replace(/_/g, '-')
                .split('-')
                .map(
                  (word) =>
                    word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()
                )
                .join('-');
            })
            .join(', ')
        : 'Standard service';

    // Build dietary options - capitalize properly
    const dietaryOptions =
      restaurant.cuisine_and_features.dietary_options.length > 0
        ? restaurant.cuisine_and_features.dietary_options
            .map(
              (option) =>
                option.charAt(0).toUpperCase() + option.slice(1).toLowerCase()
            )
            .join(', ')
        : 'None specified';

    // Build concerns note
    const concernsNote =
      restaurant.potential_concerns.length > 0
        ? `<p class="note"><strong>Things to Note:</strong> ${restaurant.potential_concerns.join(
            ', '
          )}</p>`
        : '';

    // Show directions button if already selected
    const directionsButton = this.showDirectionsButton
      ? `<button class="btn btn-secondary" onclick="window.forkcastComponent.getDirections()">🗺️ Here We Go!!</button>`
      : '';

    const yelpRatingHtml = restaurant.ratings.yelp_rating
      ? `<span class="yelp-info">
          • Yelp: ${restaurant.ratings.yelp_rating}
          <img src="${this.getYelpStarImage(restaurant.ratings.yelp_rating)}" 
               alt="${restaurant.ratings.yelp_rating} stars" 
               class="yelp-stars" 
               style="height:16px;vertical-align:middle;margin-left:2px;">
          (${restaurant.ratings.yelp_review_count} reviews)
        </span>`
      : '';

    return `
      <div class="info-card">
        <div class="card-header">
          <div class="header-top">
            <h1 class="restaurant-name">${restaurant.name}</h1>
            <span class="status-badge ${statusClass}">${statusText}</span>
          </div>
          <p class="cuisine-type">${cuisineDisplay}</p>
          <div class="rating">
            <span class="stars">${stars}</span>
            <span class="review-count">${restaurant.ratings.google_rating} (${
      restaurant.ratings.google_review_count
    } reviews)${yelpRatingHtml}</span>
          </div>
        </div>
        <div class="card-body">
          <div class="info-section">
            <h2 class="section-title">Contact & Location</h2>
            <ul class="contact-list">
              <li><span class="icon">📍</span>${
                restaurant.formatted_address
              }</li>
              ${phoneRow}
              ${websiteRow}
            </ul>
          </div>
          <div class="details-grid">
            <div class="info-section">
              <h2 class="section-title">Hours</h2>
              <p><strong>Best:</strong> ${bestTimes}</p>
              <p><strong>Peak Day:</strong> ${peakDays}</p>
              ${
                restaurant.timing.current_busyness
                  ? `<p><strong>Current Busyness:</strong> ${restaurant.timing.current_busyness}</p>`
                  : ''
              }
            </div>
            <div class="info-section">
              <h2 class="section-title">Details</h2>
              <p><strong>Price:</strong> ${restaurant.pricing.price_symbol}</p>
              <p><strong>Service:</strong> ${serviceOptions}</p>
              <p><strong>Dietary:</strong> ${dietaryOptions}</p>
            </div>
          </div>
          <div class="info-section recommendation">
            <h2 class="section-title">Why We Recommend</h2>
            <p>${restaurant.highlights.why_recommended}</p>
            ${concernsNote}
          </div>
        </div>
        <div class="card-footer">
          <button class="btn btn-primary" onclick="window.forkcastComponent.selectRestaurant()">✨ Select This Restaurant</button>
          ${directionsButton}
        </div>
      </div>
    `;
  }

  async focusOnRestaurant(restaurant: RestaurantData) {
    // Initialize InfoWindow if not already done
    if (!this.infoWindow) {
      await this.initializeGoogleMapsComponents();
    }

    this.selectedRestaurant = restaurant;

    // Center map on restaurant
    if (this.map && restaurant.position) {
      this.map.googleMap?.setCenter(restaurant.position);
      this.map.googleMap?.setZoom(15);
    }

    // Open info window
    this.infoWindow.close();
    this.infoWindow.setContent(this.getInfoWindowContent(restaurant));

    // Find the corresponding marker and open info window
    const marker = this.markers.find((m) => m.title?.includes(restaurant.name));
    if (marker && this.map.googleMap) {
      this.infoWindow.open(this.map.googleMap, marker);
    }
  }

  async selectRestaurant() {
    if (this.selectedRestaurant) {
      this.chatHistory.push({
        sender: 'agent',
        text: `Great choice! ${this.selectedRestaurant.name} looks perfect for you. Ready to get directions?`,
        timestamp: new Date(),
      });
      this.showDirectionsButton = true;

      // Update info window content to show directions button if InfoWindow exists
      if (this.infoWindow) {
        this.infoWindow.setContent(
          this.getInfoWindowContent(this.selectedRestaurant)
        );
      }

      this.cdr.detectChanges();
      this.scrollToBottom();
    }
  }

  private async createNativeMarkersWithListeners() {
    // Initialize InfoWindow if not already done
    if (!this.infoWindow) {
      await this.initializeGoogleMapsComponents();
    }

    // Wait for Google Maps libraries
    const { AdvancedMarkerElement } = (await google.maps.importLibrary(
      'marker'
    )) as google.maps.MarkerLibrary;

    // Clear existing native markers
    this.markers.forEach((marker) => (marker.map = null));
    this.markers = [];

    // Create native markers with click listeners
    this.restaurants.forEach((restaurant, index) => {
      // Create custom marker with logo and rank
      const markerDiv = document.createElement('div');
      markerDiv.style.position = 'relative';
      markerDiv.style.cursor = 'pointer';
      markerDiv.style.transition = 'transform 0.2s ease';

      // Restaurant logo
      const logoImg = document.createElement('img');
      logoImg.src = 'assets/logo_transparent.png';
      logoImg.width = 60;
      logoImg.height = 60;
      logoImg.alt = restaurant.name;

      // Fallback for logo loading error
      logoImg.onerror = () => {
        logoImg.src =
          'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHZpZXdCb3g9IjAgMCA0MCA0MCIgZmlsbD0ibm9uZSIgeG1zbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iMjAiIGN5PSIyMCIgcj0iMjAiIGZpbGw9IiNlYTQzMzUiLz4KPHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1zbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4PSI4IiB5PSI4Ij4KPHBhdGggZD0iTTExIDl2MmgtMXY3aDJ2LTdoLTF6IiBmaWxsPSJ3aGl0ZSIvPgo8L3N2Zz4KPC9zdmc+';
      };

      // Rank badge
      const rankBadge = document.createElement('div');
      rankBadge.textContent = restaurant.rank.toString();
      rankBadge.style.position = 'absolute';
      rankBadge.style.top = '-3px';
      rankBadge.style.right = '-3px';
      rankBadge.style.background = 'linear-gradient(135deg, #ea4335, #ff6b6b)';
      rankBadge.style.color = 'white';
      rankBadge.style.borderRadius = '50%';
      rankBadge.style.width = '20px';
      rankBadge.style.height = '20px';
      rankBadge.style.fontSize = '11px';
      rankBadge.style.fontWeight = 'bold';
      rankBadge.style.display = 'flex';
      rankBadge.style.alignItems = 'center';
      rankBadge.style.justifyContent = 'center';
      rankBadge.style.border = '2px solid white';
      rankBadge.style.boxShadow = '0 2px 6px rgba(0, 0, 0, 0.3)';

      markerDiv.appendChild(logoImg);
      markerDiv.appendChild(rankBadge);

      // Add hover effect
      markerDiv.addEventListener('mouseenter', () => {
        markerDiv.style.transform = 'scale(1.1)';
      });
      markerDiv.addEventListener('mouseleave', () => {
        markerDiv.style.transform = 'scale(1)';
      });

      const marker = new AdvancedMarkerElement({
        map: this.map.googleMap,
        position: restaurant.position,
        title: restaurant.name,
        content: markerDiv,
        gmpClickable: true,
      });

      // Add click listener - Use 'gmp-click' for Advanced Markers
      marker.addListener('gmp-click', async () => {
        await this.onMarkerClick(restaurant);
        this.infoWindow.open(this.map.googleMap!, marker);
      });

      this.markers.push(marker);
    });
  }

  getDirections() {
    if (this.selectedRestaurant && this.userLocation) {
      const destination = `${this.selectedRestaurant.coordinates.latitude},${this.selectedRestaurant.coordinates.longitude}`;
      const origin = `${this.userLocation.lat},${this.userLocation.lng}`;

      const googleMapsUrl = `https://www.google.com/maps/dir/?api=1&origin=${origin}&destination=${destination}&travelmode=driving`;

      this.chatHistory.push({
        sender: 'system',
        text: `Opening directions to ${this.selectedRestaurant.name}... 🗺️`,
        timestamp: new Date(),
      });

      window.open(googleMapsUrl, '_blank');

      setTimeout(() => {
        this.chatHistory.push({
          sender: 'agent',
          text: `Enjoy your meal at ${
            this.selectedRestaurant!.name
          }! Have a great time! 🍽️`,
          timestamp: new Date(),
        });
        this.scrollToBottom();
      }, 1000);
    }
  }

  closeInfoWindowSafe() {
    if (this.infoWindow) {
      this.infoWindow.close();
    }
  }

  getStarRating(rating: number): string {
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 >= 0.5;
    const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0);
    const stars = '★'.repeat(fullStars) + (hasHalfStar ? '☆' : '');
    const inactiveStars =
      emptyStars > 0
        ? `<span class="stars-inactive">${'☆'.repeat(emptyStars)}</span>`
        : '';
    return stars + inactiveStars;
  }

  private getYelpStarImage(rating: number): string {
    // Round to nearest 0.5
    const rounded = Math.round(rating * 2) / 2;
    // Map to asset file names (adjust path as needed)
    switch (rounded) {
      case 5:
        return 'assets/ReviewRibbon_v2/Desktop/small_16/Review_Ribbon_small_16_5@1x.png';
      case 4.5:
        return 'assets/ReviewRibbon_v2/Desktop/small_16/Review_Ribbon_small_16_4_half@1x.png';
      case 4:
        return 'assets/ReviewRibbon_v2/Desktop/small_16/Review_Ribbon_small_16_4@1x.png';
      case 3.5:
        return 'assets/ReviewRibbon_v2/Desktop/small_16/Review_Ribbon_small_16_3_half@1x.png';
      case 3:
        return 'assets/ReviewRibbon_v2/Desktop/small_16/Review_Ribbon_small_16_3@1x.png';
      case 2.5:
        return 'assets/ReviewRibbon_v2/Desktop/small_16/Review_Ribbon_small_16_2_half@1x.png';
      case 2:
        return 'assets/ReviewRibbon_v2/Desktop/small_16/Review_Ribbon_small_16_2@1x.png';
      case 1.5:
        return 'assets/ReviewRibbon_v2/Desktop/small_16/Review_Ribbon_small_16_1_half@1x.png';
      case 1:
        return 'assets/ReviewRibbon_v2/Desktop/small_16/Review_Ribbon_small_16_1@1x.png';
      case 0.5:
        return 'assets/ReviewRibbon_v2/Desktop/small_16/Review_Ribbon_small_16_0_half@1x.png';
      default:
        return 'assets/ReviewRibbon_v2/Desktop/small_16/Review_Ribbon_small_16_0@1x.png';
    }
  }

  getGoogleStarIcons(rating: number): string {
    // Adjust these paths to match your actual asset location
    const fullStar = 'assets/google-stars/full_star.png';
    const halfStar = 'assets/google-stars/half_star.png';
    const emptyStar = 'assets/google-stars/empty_star.png';

    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 >= 0.25 && rating % 1 < 0.75;
    const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0);

    let starsHtml = '';
    for (let i = 0; i < fullStars; i++) {
      starsHtml += `<img src="${fullStar}" alt="★" class="google-star" style="height:16px;width:16px;vertical-align:middle;" onerror="this.onerror=null;this.style.display='none';this.insertAdjacentHTML('afterend','★');">`;
    }
    if (hasHalfStar) {
      starsHtml += `<img src="${halfStar}" alt="☆" class="google-star" style="height:16px;width:16px;vertical-align:middle;" onerror="this.onerror=null;this.style.display='none';this.insertAdjacentHTML('afterend','☆');">`;
    }
    for (let i = 0; i < emptyStars; i++) {
      starsHtml += `<img src="${emptyStar}" alt="☆" class="google-star google-star-empty" style="height:16px;width:16px;vertical-align:middle;opacity:0.4;" onerror="this.onerror=null;this.style.display='none';this.insertAdjacentHTML('afterend','☆');">`;
    }
    return starsHtml;
  }

  // Tracking functions for ngFor performance
  trackByFn(index: number, item: ChatMessage): string {
    return `${item.sender}-${index}-${item.text}`;
  }

  trackRestaurant(index: number, restaurant: RestaurantData): string {
    return restaurant.place_id;
  }

  showInfoWindow(): boolean {
    return !!this.selectedRestaurant;
  }

  scrollToBottom() {
    setTimeout(() => {
      if (this.chatHistoryContainer) {
        const element = this.chatHistoryContainer.nativeElement;
        element.scrollTop = element.scrollHeight;
      }
    }, 100);
  }

  /**
   * Generate a unique conversation ID
   */
  private generateConversationId(): string {
    return `conv_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  /**
   * Clear conversation and start fresh
   */
  clearConversation(): void {
    this.chatHistory = [];
    this.restaurants = [];
    this.selectedRestaurant = null;
    this.showDirectionsButton = false;
    this.agentService.clearConversation();
    this.conversationId = this.generateConversationId();

    // Clear markers
    this.markers.forEach((marker) => (marker.map = null));
    this.markers = [];

    // Restart party listener to continue receiving updates
    this.stopPartyRestaurantListener();
    this.startPartyRestaurantListener();
    this.startConversation();
  }
}
