import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { GoogleMap, MapMarker, GoogleMapsModule } from '@angular/google-maps';
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
  photo?: string;
  selected?: boolean;
  place_id: string;
  expanded?: boolean;
  user_ratings_total?: number;
  showHover?: boolean;
  hoverX?: number;
  hoverY?: number;
}

@Component({
  selector: 'app-search',
  standalone: true,
  imports: [
    CommonModule,
    GoogleMapsModule,
    StarRatingComponent,
    YelpRibbonComponent,
    FormsModule
  ],
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.css']
})
export class SearchComponent implements OnInit {
  user = {
    photoUrl: '',
    initials: '',
    name: ''
  };

  chatMessages: string[] = [];
  isSearching: boolean = false;
  currentChatMessage: string = '';

  mapOptions: google.maps.MapOptions = {
    center: { lat: 34.052235, lng: -118.243683 },
    zoom: 12,
    disableDefaultUI: true,
    styles: [
      {
        "elementType": "geometry",
        "stylers": [{"color": "#242f3e"}]
      },
      {
        "elementType": "labels.text.fill",
        "stylers": [{"color": "#746855"}]
      },
      {
        "elementType": "labels.text.stroke",
        "stylers": [{"color": "#242f3e"}]
      },
      {
        "featureType": "administrative.locality",
        "elementType": "labels.text.fill",
        "stylers": [{"color": "#d59563"}]
      },
      {
        "featureType": "poi",
        "elementType": "labels.text.fill",
        "stylers": [{"color": "#d59563"}]
      },
      {
        "featureType": "poi.park",
        "elementType": "geometry",
        "stylers": [{"color": "#263c3f"}]
      },
      {
        "featureType": "poi.park",
        "elementType": "labels.text.fill",
        "stylers": [{"color": "#6b9a76"}]
      },
      {
        "featureType": "road",
        "elementType": "geometry",
        "stylers": [{"color": "#38414e"}]
      },
      {
        "featureType": "road",
        "elementType": "geometry.stroke",
        "stylers": [{"color": "#212a37"}]
      },
      {
        "featureType": "road",
        "elementType": "labels.text.fill",
        "stylers": [{"color": "#9ca5b3"}]
      },
      {
        "featureType": "road.highway",
        "elementType": "geometry",
        "stylers": [{"color": "#746855"}]
      },
      {
        "featureType": "road.highway",
        "elementType": "geometry.stroke",
        "stylers": [{"color": "#1f2835"}]
      },
      {
        "featureType": "road.highway",
        "elementType": "labels.text.fill",
        "stylers": [{"color": "#f3d19c"}]
      },
      {
        "featureType": "transit",
        "elementType": "geometry",
        "stylers": [{"color": "#2f3948"}]
      },
      {
        "featureType": "transit.station",
        "elementType": "labels.text.fill",
        "stylers": [{"color": "#d59563"}]
      },
      {
        "featureType": "water",
        "elementType": "geometry",
        "stylers": [{"color": "#17263c"}]
      },
      {
        "featureType": "water",
        "elementType": "labels.text.fill",
        "stylers": [{"color": "#515c6d"}]
      },
      {
        "featureType": "water",
        "elementType": "labels.text.stroke",
        "stylers": [{"color": "#17263c"}]
      }
    ]
  };

  markerIcon: google.maps.Icon = {
    url: 'assets/logo_transparent.png',
    scaledSize: new google.maps.Size(40, 40)
  };

  private baseMarkerSize: number = 40;
  private markerSizeScaleFactor: number = 2;
  private minMarkerSize: number = 20;
  private maxMarkerSize: number = 80;

  places: Place[] = [];

  constructor(private router: Router, private authService: AuthService) { }

  ngOnInit(): void {
    this.authService.user$.subscribe((user: User | null) => {
      if (user) {
        this.user.photoUrl = user.photoURL || '';
        this.user.name = user.displayName || '';
        this.user.initials = user.displayName ? this.getInitials(user.displayName) : '';
      }
    });

    this.chatMessages.push('Welcome to Forkcast! How can I help you find a place to eat?');
    this.chatMessages.push('Calling location search agent...');

    this.getCurrentLocation();

    this.places = [
      {
        name: 'The Great American Pizza Company',
        formatted_address: '123 Main St, Anytown CA',
        rating: 4.5,
        yelp_rating: 4,
        opening_hours: { open_now: true },
        review_summary: 'Great pizza, friendly staff.',
        latitude: 34.052235 + 0.01,
        longitude: -118.243683 + 0.01,
        photo: 'https://via.placeholder.com/150',
        place_id: 'ChIJD4K4y1_OqokRV_Y1f3w0X4Q',
        user_ratings_total: 120
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
        photo: 'https://via.placeholder.com/150',
        place_id: 'ChIJ0-n7sU_OqokRg_J3f3w0X4Q',
        user_ratings_total: 85
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
    if (zoom) {
      const newSize = Math.min(
        this.maxMarkerSize,
        Math.max(this.minMarkerSize, this.baseMarkerSize + (zoom - 12) * this.markerSizeScaleFactor)
      );
      this.markerIcon = {
        ...this.markerIcon,
        scaledSize: new google.maps.Size(newSize, newSize)
      };
    }
  }

  showHoverCard(place: Place, event?: MouseEvent): void {
    if (event) {
      const rect = (event.target as HTMLElement).getBoundingClientRect();
      place.hoverX = rect.left + window.scrollX;
      place.hoverY = rect.top + window.scrollY - 100;
    }
    this.places.forEach(p => p.showHover = false);
    place.showHover = true;
  }

  hideHoverCard(place: Place): void {
    place.showHover = false;
  }

  startSearchAnimation(): void {
    this.isSearching = true;
    setTimeout(() => {
      this.isSearching = false;
      this.chatMessages.push('Calling parallel enrichment agent...');
      this.chatMessages.push('  - Sub-agent: Cuisine preference analysis');
      this.chatMessages.push('  - Sub-agent: Budget estimation');
      this.chatMessages.push('  - Sub-agent: Amenity matching');
      this.chatMessages.push('Search complete! Here are some recommendations.');
      this.scrollToBottom();
    }, 3000);
  }

  onSendMessage(): void {
    if (this.currentChatMessage.trim()) {
      this.chatMessages.push(`User: ${this.currentChatMessage}`);
      this.currentChatMessage = '';
      this.scrollToBottom();
    }
  }

  onMicClick(): void {
    this.chatMessages.push('Mic input activated (Voice recognition not yet implemented)');
    this.scrollToBottom();
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
    this.places.forEach(p => {
      if (p !== place) {
        p.expanded = false;
      }
    });
    place.expanded = !place.expanded;
  }

  createRoute(): void {
    const selectedPlaces = this.places.filter(place => place.selected);
    if (selectedPlaces.length > 0 && this.mapOptions.center) {
      const origin = `${this.mapOptions.center.lat},${this.mapOptions.center.lng}`;
      const destination = `${selectedPlaces[0].latitude},${selectedPlaces[0].longitude}`;
      let waypoints = '';

      if (selectedPlaces.length > 1) {
        waypoints = selectedPlaces.slice(1).map(place => `${place.latitude},${place.longitude}`).join('|');
      }

      let googleMapsUrl = `https://www.google.com/maps/dir/?api=1&origin=${origin}&destination=${destination}`;
      if (waypoints) {
        googleMapsUrl += `&waypoints=${waypoints}`;
      }
      googleMapsUrl += `&travelmode=driving`;

      window.open(googleMapsUrl, '_blank');
    }
  }
} 