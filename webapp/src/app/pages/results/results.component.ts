import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { GoogleMap, MapMarker, GoogleMapsModule } from '@angular/google-maps';
import { UserAvatarComponent } from '../../components/user-avatar/user-avatar.component';
import { StarRatingComponent } from '../../components/star-rating/star-rating.component';
import { YelpRibbonComponent } from '../../components/yelp-ribbon/yelp-ribbon.component';
import { environment } from '../../../environments/environment';

@Component({
  selector: 'app-results',
  standalone: true,
  imports: [
    CommonModule,
    GoogleMapsModule,
    UserAvatarComponent,
    StarRatingComponent,
    YelpRibbonComponent
  ],
  templateUrl: './results.component.html',
  styleUrls: ['./results.component.css']
})
export class ResultsComponent implements OnInit {
  user = {
    photoUrl: '', // To be filled from Google Auth
    initials: 'PM', // Fallback initials
    name: 'Parth M', // Example name
  };

  googleMapsApiKey = environment.googleMapsApiKey;

  places = [
    // Sample data, replace with real agent response
    {
      place_id: 'ChIJP-J-0Jq0woARLzKqj_zVw0',
      name: 'Fu Man Dumpling House',
      formatted_address: '818 W 7th St, Los Angeles, CA 90017, United States',
      latitude: 34.0473642,
      longitude: -118.2586268,
      vicinity: '818 W 7th St, Los Angeles',
      business_status: 'OPERATIONAL',
      price_level: 2,
      rating: 4.3,
      yelp_rating: 4,
      user_ratings_total: 547,
      opening_hours: { open_now: false },
      types: ['restaurant', 'food', 'point_of_interest', 'establishment'],
      review_summary: 'A popular spot for dumplings.'
    },
    // Add more places as needed
  ];

  mapOptions = {
    center: { lat: 34.0473642, lng: -118.2586268 },
    zoom: 13,
    options: {
      mapTypeControl: false,
      streetViewControl: false,
      fullscreenControl: false
    }
  };

  markerIcon = {
    url: 'assets/logo_transparent.png',
    scaledSize: typeof google !== 'undefined' ? new google.maps.Size(40, 40) : undefined
  };

  ngOnInit() {
    // TODO: Load user info from Google Auth service
    // this.user = ...
  }
} 