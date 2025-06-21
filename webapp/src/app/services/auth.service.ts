import { Injectable, inject, PLATFORM_ID } from '@angular/core';
import { Auth, signInWithRedirect, GoogleAuthProvider, getRedirectResult, User } from '@angular/fire/auth';
import { Router } from '@angular/router';
import { isPlatformBrowser } from '@angular/common';
import { signInWithPopup } from '@angular/fire/auth';


@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private auth: Auth = inject(Auth);
  private router: Router = inject(Router);
  private platformId: Object = inject(PLATFORM_ID);
  private provider = new GoogleAuthProvider();

  constructor() {
    // if (isPlatformBrowser(this.platformId)) {
    //   this.handleRedirectResult();
    // }
  }

  googleSignIn() {
    if (!isPlatformBrowser(this.platformId)) {
      return Promise.reject(new Error('Authentication is only available in browser environment'));
    }
    return signInWithPopup(this.auth, this.provider)
      .then((result) => {
        return result.user.getIdToken().then(token => {
          localStorage.setItem('authToken', token);
          this.router.navigate(['/party-selection']);
        });
      });
  }

  isAuthenticated(): boolean {
    if (!isPlatformBrowser(this.platformId)) {
      return false;
    }
    return !!localStorage.getItem('authToken');
  }

  signOut() {
    if (!isPlatformBrowser(this.platformId)) {
      return;
    }
    localStorage.removeItem('authToken');
    this.auth.signOut();
    this.router.navigate(['/signin']);
  }
}