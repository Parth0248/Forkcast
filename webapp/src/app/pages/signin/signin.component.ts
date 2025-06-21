import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-signin',
  templateUrl: './signin.component.html',
  styleUrls: ['./signin.component.css']
})
export class SigninComponent {
  constructor(private authService: AuthService, private router: Router) {}

  signInWithGoogle() {
    this.authService.googleSignIn()
      .then((result: any) => {
        // Handle successful sign-in
        console.log('Google Sign-in successful', result);

        const userName = result?.user?.displayName || '';
        localStorage.setItem('userName', userName);

        // Redirect to the party-selection page
        // this.router.navigate(['/party-selection']);
      })
      .catch((error: any) => {
        // Handle errors
        alert('Sign in failed: ' + error.message);
      });
  }
} 