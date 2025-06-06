import { Injectable } from '@angular/core';
import { GoogleAuthProvider, signInWithPopup, User } from 'firebase/auth';
import { auth } from '../firebase/firebaseConfig';
import { Observable, from } from 'rxjs';
import { startWith } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  user$: Observable<User | null>;

  constructor() {
    this.user$ = new Observable<User | null>(observer => {
      auth.onAuthStateChanged(user => {
        observer.next(user);
      });
    }).pipe(startWith(auth.currentUser));
  }

  signInWithGoogle() {
    const provider = new GoogleAuthProvider();
    return signInWithPopup(auth, provider);
  }
} 