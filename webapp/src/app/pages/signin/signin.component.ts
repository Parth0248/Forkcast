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
    this.authService.signInWithGoogle()
      .then((result: any) => {
        // Handle successful sign-in
        console.log('Google Sign-in successful', result);
        // Redirect to the search page
        this.router.navigate(['/search']);
      })
      .catch((error: any) => {
        // Handle errors
        alert('Sign in failed: ' + error.message);
      });
  }
} 