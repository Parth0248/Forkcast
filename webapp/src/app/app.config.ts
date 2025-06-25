import { ApplicationConfig, provideZoneChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient, withFetch } from '@angular/common/http';
import { provideAnimations } from '@angular/platform-browser/animations';
import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';

import { routes } from './app.routes';
import {firebaseConfig } from './firebase/firebaseConfig';
import { provideFirebaseApp, initializeApp as initializeApp_alias } from '@angular/fire/app';
import { provideAuth } from '@angular/fire/auth';
import { getFirestore, provideFirestore } from '@angular/fire/firestore';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideHttpClient(withFetch()),
    provideAnimations(),
    provideFirebaseApp(() => initializeApp(firebaseConfig)),
    provideAuth(() => getAuth()), provideFirebaseApp(() => initializeApp({
        projectId: '<YOUR_PROJECT_ID>',
        appId: '<YOUR_APP_ID>',
        storageBucket: '<YOUR_STORAGE_BUCKET>',
        apiKey: '<YOUR_API_KEY>',
        authDomain: '<YOUR_AUTH_DOMAIN>',
        messagingSenderId: '<YOUR_MESSAGING_SENDER_ID>',
        measurementId: '<YOUR_MEASUREMENT_ID>',
      })
    ), provideFirestore(() => getFirestore())
  ],
};
