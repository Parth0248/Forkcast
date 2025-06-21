import { Routes } from '@angular/router';
import { AuthGuard } from './services/auth.guard';

export const routes: Routes = [
  { path: '', redirectTo: '/signin', pathMatch: 'full' },
  { path: 'search', loadComponent: () => import('./pages/search/search.component').then(m => m.SearchComponent), canActivate: [AuthGuard] },
  { path: 'party-selection', loadComponent: () => import('./pages/party-selection/party-selection.component').then(m => m.PartySelectionComponent), canActivate: [AuthGuard] },
  { path: 'signin', loadComponent: () => import('./pages/signin/signin.component').then(m => m.SigninComponent) }
];