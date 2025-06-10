import { Component, OnInit, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { GoogleMap, GoogleMapsModule } from '@angular/google-maps';

@Component({
  selector: 'app-search',
  standalone: true,
  imports: [CommonModule, FormsModule, GoogleMapsModule],
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.scss']
})
export class SearchComponent implements OnInit {
  @ViewChild(GoogleMap) map!: GoogleMap;

  userMessage: string = '';
  chatHistory: Array<{sender: 'user' | 'agent' | 'system', text: string, type?: string}> = [];
  restaurants: any[] = [];
  selectedRestaurant: any = null;
  showModal: boolean = false;
  mapOptions: google.maps.MapOptions = {
    center: { lat: 37.7749, lng: -122.4194 },
    zoom: 12
  };

  constructor(private router: Router) {}

  ngOnInit() {
    const token = localStorage.getItem('authToken');
    if (!token) {
      this.router.navigate(['/signin']);
      return;
    }
    this.startConversation();
  }

  ngAfterViewInit() {
    // Initialize map after view is ready
    this.initMap();
  }

  async initMap() {
    try {
      const { Map } = await google.maps.importLibrary("maps") as google.maps.MapsLibrary;
      const { AdvancedMarkerElement } = await google.maps.importLibrary("marker") as google.maps.MarkerLibrary;
      
      // Update map options
      this.mapOptions = {
        ...this.mapOptions,
        mapId: 'forkcast-map'
      };
    } catch (error) {
      console.error('Error initializing map:', error);
    }
  }

  startConversation() {
    this.addMessageToChat('agent', 'Hello! I\'m Forkcast. What kind of food are you in the mood for today?');
  }

  addMessageToChat(sender: 'user' | 'agent' | 'system', text: string, type: string = 'agent') {
    this.chatHistory.push({ sender, text, type });
  }

  handleUserMessage() {
    if (this.userMessage.trim()) {
      this.addMessageToChat('user', this.userMessage);
      this.userMessage = '';
      
      setTimeout(() => {
        this.addMessageToChat('agent', 'Interesting! And what about the price range or general vibe?');
      }, 1000);
      
      setTimeout(() => {
        this.addMessageToChat('agent', 'Forkcast: Consulting Location Search Agent...', 'system');
      }, 2000);
      
      setTimeout(() => {
        this.addMessageToChat('agent', 'Forkcast: Analyzing preferences for cuisine, budget, and amenities...', 'system');
      }, 3500);
      
      setTimeout(() => {
        this.addMessageToChat('agent', 'Okay, I think I have enough to go on. Ready to search?');
      }, 5000);
    }
  }

  findRestaurants() {
    this.addMessageToChat('agent', 'Forkcast: Searching for locations via Google Maps...', 'system');
    this.addMessageToChat('agent', 'Forkcast: Enriching details with Yelp, Foursquare, and Busyness data...', 'system');
    
    this.restaurants = [
      {
        id: 1,
        name: "The Grand Eatery",
        rating: 4.8,
        photo: "https://source.unsplash.com/random/400x300/?restaurant,interior",
        price: "$$$",
        amenities: ["Wi-Fi", "Parking", "Outdoor Seating"],
        diet: ["Vegan Options"],
        busyness: "Moderately Busy",
        summary: "Matches your preference for 'lively ambiance' and 'great for groups'.",
        position: { lat: 37.7749, lng: -122.4194 }
      }
    ];
    
    setTimeout(() => {
      this.addMessageToChat('agent', 'I\'ve found a few places for you! They are now shown on the map.');
    }, 2000);
  }

  openRestaurantModal(restaurant: any) {
    this.selectedRestaurant = restaurant;
    this.showModal = true;
  }

  closeModal() {
    this.showModal = false;
    this.selectedRestaurant = null;
  }

  selectRestaurant() {
    if (this.selectedRestaurant) {
      this.closeModal();
    }
  }

  onZoomChanged() {
    if (this.map) {
      const zoomLevel = this.map.getZoom();
      console.log('Zoom level changed:', zoomLevel);
    }
  }
}