import { Injectable } from '@angular/core';
import { GoogleAuthProvider, signInWithPopup } from 'firebase/auth';
import { auth } from '../firebase/firebaseConfig';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  signInWithGoogle() {
    const provider = new GoogleAuthProvider();
    return signInWithPopup(auth, provider);
  }
} 