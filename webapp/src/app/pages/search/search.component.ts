import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { GoogleMap, MapMarker, GoogleMapsModule } from '@angular/google-maps';
import { UserAvatarComponent } from '../../components/user-avatar/user-avatar.component';
import { StarRatingComponent } from '../../components/star-rating/star-rating.component';
import { YelpRibbonComponent } from '../../components/yelp-ribbon/yelp-ribbon.component';
import { environment } from '../../../environments/environment';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { User } from 'firebase/auth';

interface Place {
  name: string;
  formatted_address: string;
  rating: number;
  yelp_rating: number;
  opening_hours: { open_now: boolean };
  review_summary: string;
  latitude: number;
  longitude: number;
  photo?: string; // Optional photo URL
  selected?: boolean; // New property for selection
  place_id: string; // Google Place ID
  expanded?: boolean; // New property for card expansion
  user_ratings_total?: number; // New property for user ratings total
}

@Component({
  selector: 'app-search',
  standalone: true,
  imports: [
    CommonModule,
    GoogleMapsModule,
    UserAvatarComponent,
    StarRatingComponent,
    YelpRibbonComponent,
    FormsModule
  ],
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.css']
})
export class SearchComponent implements OnInit {
  user = {
    photoUrl: '', // To be filled from Google Auth
    initials: '',
    name: ''
  };

  chatMessages: string[] = []; // Array to hold chat messages and logs
  isSearching: boolean = false; // New property for ripple animation
  currentChatMessage: string = ''; // For the text input field

  mapOptions: google.maps.MapOptions = {
    center: { lat: 34.052235, lng: -118.243683 }, // Default to Los Angeles, will update to current location
    zoom: 12,
    disableDefaultUI: true, // Disable default map UI
  };
  markerIcon: google.maps.Icon = {
    url: 'assets/logo_transparent.png', // Custom logo path
    scaledSize: new google.maps.Size(40, 40) // Initial size
  };

  private baseMarkerSize: number = 40; // Base size of the marker icon
  private markerSizeScaleFactor: number = 2; // How much the size changes per zoom level
  private minMarkerSize: number = 20; // Minimum size of the marker
  private maxMarkerSize: number = 80; // Maximum size of the marker

  places: Place[] = []; // Initialize places array as empty

  constructor(private router: Router, private authService: AuthService) { }

  ngOnInit(): void {
    this.authService.user$.subscribe((user: User | null) => {
      if (user) {
        this.user.photoUrl = user.photoURL || '';
        this.user.name = user.displayName || '';
        this.user.initials = user.displayName ? this.getInitials(user.displayName) : '';
      }
    });

    // Simulate initial chat messages/logs
    this.chatMessages.push('Welcome to Forkcast! How can I help you find a place to eat?');
    this.chatMessages.push('Calling location search agent...');

    this.getCurrentLocation(); // Call to get current location on init

    // Simulate fetching initial place data (this will be replaced by model results)
    this.places = [
      {
        name: 'The Great American Pizza Company',
        formatted_address: '123 Main St, Anytown CA',
        rating: 4.5,
        yelp_rating: 4,
        opening_hours: { open_now: true },
        review_summary: 'Great pizza, friendly staff.',
        latitude: 34.052235 + 0.01, // Slightly offset from center for demonstration
        longitude: -118.243683 + 0.01,
        photo: 'https://via.placeholder.com/150', // Placeholder image
        place_id: 'ChIJD4K4y1_OqokRV_Y1f3w0X4Q',
        user_ratings_total: 120 // Example value
      },
      {
        name: 'Burger Joint Deluxe',
        formatted_address: '456 Oak Ave, Anytown CA',
        rating: 3.8,
        yelp_rating: 3.5,
        opening_hours: { open_now: false },
        review_summary: 'Good burgers, a bit pricey.',
        latitude: 34.052235 - 0.01,
        longitude: -118.243683 - 0.01,
        photo: 'https://via.placeholder.com/150', // Placeholder image
        place_id: 'ChIJ0-n7sU_OqokRg_J3f3w0X4Q',
        user_ratings_total: 85 // Example value
      }
    ];
  }

  private getInitials(name: string): string {
    return name.split(' ').map(n => n[0]).join('').toUpperCase();
  }

  anyPlaceSelected(): boolean {
    return this.places.some(place => place.selected);
  }

  anyPlaceExpanded(): boolean {
    return this.places.some(place => place.expanded);
  }

  collapseAllPlaces(): void {
    this.places.forEach(place => place.expanded = false);
  }

  // Method to get current location and center the map
  private getCurrentLocation(): void {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          this.mapOptions.center = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
          };
          this.chatMessages.push('Map centered on your current location.');
          this.scrollToBottom();
        },
        (error) => {
          console.error('Error getting location', error);
          this.chatMessages.push('Could not retrieve your current location. Map defaulted to Los Angeles.');
          this.scrollToBottom();
        }
      );
    } else {
      this.chatMessages.push('Geolocation is not supported by your browser. Map defaulted to Los Angeles.');
      this.scrollToBottom();
    }
  }

  onZoomChanged(zoom: number): void {
    const newSize = Math.min(this.maxMarkerSize, Math.max(this.minMarkerSize, this.baseMarkerSize + (zoom - 12) * this.markerSizeScaleFactor));
    this.markerIcon = {
      ...this.markerIcon,
      scaledSize: new google.maps.Size(newSize, newSize)
    };
  }

  startSearchAnimation(): void {
    this.isSearching = true;
    // Simulate search process and stop animation after a delay
    setTimeout(() => {
      this.isSearching = false;
      // TODO: Call Forkcast model for search and update places/chatMessages
      this.chatMessages.push('Calling parallel enrichment agent...');
      this.chatMessages.push('  - Sub-agent: Cuisine preference analysis');
      this.chatMessages.push('  - Sub-agent: Budget estimation');
      this.chatMessages.push('  - Sub-agent: Amenity matching');
      this.chatMessages.push('Search complete! Here are some recommendations.');
      this.scrollToBottom(); // Scroll to bottom after new messages
    }, 3000); // 3 seconds for demonstration
  }

  onSendMessage(): void {
    if (this.currentChatMessage.trim()) {
      this.chatMessages.push(`User: ${this.currentChatMessage}`);
      this.currentChatMessage = ''; // Clear input
      this.scrollToBottom(); // Scroll to bottom after new message
      // TODO: Send message to Forkcast model and get response
    }
  }

  onMicClick(): void {
    this.chatMessages.push('Mic input activated (Voice recognition not yet implemented)');
    this.scrollToBottom(); // Scroll to bottom after new message
    // TODO: Implement voice recognition
  }

  private scrollToBottom(): void {
    try {
      const chatContent = document.querySelector('.chat-content');
      if (chatContent) {
        chatContent.scrollTop = chatContent.scrollHeight;
      }
    } catch (err) {
      console.error('Could not scroll to bottom:', err);
    }
  }

  togglePlaceExpansion(place: Place): void {
    place.expanded = !place.expanded;
  }

  createRoute(): void {
    const selectedPlaces = this.places.filter(place => place.selected);
    if (selectedPlaces.length > 0) {
      const origin = `${this.mapOptions.center?.lat},${this.mapOptions.center?.lng}`;
      const destination = `${selectedPlaces[0].latitude},${selectedPlaces[0].longitude}`;
      let waypoints = '';

      if (selectedPlaces.length > 1) {
        waypoints = selectedPlaces.slice(1).map(place => `${place.latitude},${place.longitude}`).join('|');
      }

      let googleMapsUrl = `https://www.google.com/maps/dir/?api=1&origin=${origin}&destination=${destination}`;
      if (waypoints) {
        googleMapsUrl += `&waypoints=${waypoints}`;
      }
      googleMapsUrl += `&travelmode=driving`; // Assuming driving mode

      window.open(googleMapsUrl, '_blank');
    }
  }
} 