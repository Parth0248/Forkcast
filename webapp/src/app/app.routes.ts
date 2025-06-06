import { Routes } from '@angular/router';
import { SigninComponent } from './pages/signin/signin.component';
import { SearchComponent } from './pages/search/search.component';

export const routes: Routes = [
  { path: '', redirectTo: 'signin', pathMatch: 'full' },
  { path: 'signin', component: SigninComponent },
  { path: 'search', component: SearchComponent },
];
