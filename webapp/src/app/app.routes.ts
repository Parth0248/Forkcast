import { Routes } from '@angular/router';
import { SigninComponent } from './pages/signin/signin.component';
import { ResultsComponent } from './pages/results/results.component';

export const routes: Routes = [
  { path: '', redirectTo: 'signin', pathMatch: 'full' },
  { path: 'signin', component: SigninComponent },
  { path: 'results', component: ResultsComponent },
];
