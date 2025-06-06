import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-star-rating',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './star-rating.component.html',
  styleUrls: ['./star-rating.component.css']
})
export class StarRatingComponent {
  @Input() rating: number = 0;
  max: number = 5;

  get fullStars(): number[] {
    return Array(Math.floor(this.rating)).fill(0);
  }
  get halfStar(): boolean {
    return this.rating % 1 >= 0.29 && this.rating % 1 <= 0.71;
  }
  get emptyStars(): number[] {
    return Array(this.max - Math.ceil(this.rating)).fill(0);
  }
} 