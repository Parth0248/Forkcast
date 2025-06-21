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
    provideAuth(() => getAuth()), provideFirebaseApp(() => initializeApp({ projectId: "forkcast-0248", appId: "1:1061887948695:web:a17310fbdf4a5a9e6cb6d2", storageBucket: "forkcast-0248.firebasestorage.app", apiKey: "AIzaSyD0KAZxVBcaQ3kvlLamANL4FnRN8sPqfHU", authDomain: "forkcast-0248.firebaseapp.com", messagingSenderId: "1061887948695", measurementId: "G-90SD3N7JLG" })), provideFirestore(() => getFirestore())
  ]
};