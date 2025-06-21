import { Inject, Injectable, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class MapsLoaderService {

  private scriptLoaded = false;
  private loadingPromise?: Promise<void>;

  constructor(@Inject(PLATFORM_ID) private platformId: Object) { }

  load(): Promise<void> {
    // Only run this code in a browser environment
    if (!isPlatformBrowser(this.platformId)) {
      return Promise.resolve();
    }

    if (this.scriptLoaded) {
      return Promise.resolve();
    }

    if (this.loadingPromise) {
      return this.loadingPromise;
    }

    this.loadingPromise = new Promise((resolve, reject) => {
      const script = document.createElement('script');
      script.src = `https://maps.googleapis.com/maps/api/js?key=${environment.googleMapsApiKey}`;
      script.async = true;
      script.defer = true;

      script.onload = () => {
        this.scriptLoaded = true;
        this.loadingPromise = undefined;
        resolve();
      };

      script.onerror = (error) => {
        this.loadingPromise = undefined;
        reject(error);
      };

      document.head.appendChild(script);
    });

    return this.loadingPromise;
  }
}