import { initializeApp } from 'firebase/app';
import { getAuth, connectAuthEmulator } from 'firebase/auth';
import { isPlatformBrowser } from '@angular/common';
import { PLATFORM_ID, inject } from '@angular/core';
import { environment } from '../../environments/environment';

const firebaseConfig = {
  apiKey: environment.firebase.apiKey,
  authDomain: environment.firebase.authDomain,
  projectId: environment.firebase.projectId,
  storageBucket: environment.firebase.storageBucket,
  messagingSenderId: environment.firebase.messagingSenderId,
  appId: environment.firebase.appId,
  measurementId: environment.firebase.measurementId
};

// Create a factory function to initialize Firebase
export function initializeFirebase() {
  const platformId = inject(PLATFORM_ID);
  const app = isPlatformBrowser(platformId) ? initializeApp(firebaseConfig) : null;
  const auth = app ? getAuth(app) : null;
  return { app, auth };
}

export { firebaseConfig };