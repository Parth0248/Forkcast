import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-yelp-ribbon',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './yelp-ribbon.component.html',
  styleUrls: ['./yelp-ribbon.component.css']
})
export class YelpRibbonComponent {
  @Input() yelpRating: number = 0;

  get ribbonSrc(): string {
    // Use the medium_20 asset directory for Yelp stars
    return `assets/ReviewRibbon_v2/Desktop/medium_20/Review_Ribbon_medium_20_${this.yelpRating}@1x.png`;
  }
} 