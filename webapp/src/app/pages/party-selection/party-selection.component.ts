// party-selection.component.ts
import { Component, inject } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import {
  Firestore,
  doc,
  setDoc,
  getDoc,
  serverTimestamp,
} from '@angular/fire/firestore';
import { Auth } from '@angular/fire/auth';

interface PartyMode {
  mode: 'solo' | 'host' | 'guest';
  partyCode?: string;
  isHost?: boolean;
}

@Component({
  selector: 'app-party-selection',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './party-selection.component.html',
  styleUrls: ['./party-selection.component.scss'],
})
export class PartySelectionComponent {
  currentState: 'initial' | 'hosting' | 'joining' = 'initial';
  generatedPartyCode: string = '';
  enteredPartyCode: string = '';
  isCodeCopied: boolean = false;
  isValidatingCode: boolean = false;
  isCreatingParty: boolean = false;

  private firestore = inject(Firestore);
  private auth = inject(Auth);

  constructor(private router: Router) {}

  /**
   * Generate a unique 6-character alphanumeric party code
   */
  private generatePartyCode(): string {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    let result = '';
    for (let i = 0; i < 6; i++) {
      result += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return result;
  }

  generateRandomUserName(): string {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    let result = 'user_';
    for (let i = 0; i < 10; i++) {
      result += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return result;
  }

  /**
   * Create a new party in Firestore
   */
  private async createPartyInFirestore(
    partyCode: string,
    hostName: string
  ): Promise<boolean> {
    try {
      const user = this.auth.currentUser;
      if (!user) {
        console.error('No authenticated user');
        return false;
      }

      const partyRef = doc(this.firestore, 'parties', partyCode);

      // Create party document
      await setDoc(partyRef, {
        created_at: serverTimestamp(),
        expires_at: new Date(Date.now() + 24 * 60 * 60 * 1000), // 24 hours from now
        host_id: user.uid,
        host_name: hostName,
        last_updated: serverTimestamp(),
        member_count: 1,
        status: 'waiting',
        metadata: {
          created_by: 'forkcast_host_agent',
          version: '1.0',
        },
      });

      console.log(`✅ Party ${partyCode} created successfully`);
      return true;
    } catch (error) {
      console.error('❌ Failed to create party:', error);
      return false;
    }
  }

  /**
   * Verify if a party exists in Firestore
   */
  private async verifyPartyExists(partyCode: string): Promise<boolean> {
    try {
      const partyRef = doc(this.firestore, 'parties', partyCode);
      const partyDoc = await getDoc(partyRef);

      if (!partyDoc.exists()) {
        console.log(`❌ Party ${partyCode} not found`);
        return false;
      }

      const partyData = partyDoc.data();
      const partyStatus = partyData?.['status'];

      // Check if party is still accepting guests
      if (
        partyStatus !== 'waiting' &&
        partyStatus !== 'collecting_preferences'
      ) {
        console.log(
          `❌ Party ${partyCode} is no longer accepting guests (status: ${partyStatus})`
        );
        return false;
      }

      console.log(`✅ Party ${partyCode} found and accepting guests`);
      return true;
    } catch (error) {
      console.error('❌ Failed to verify party:', error);
      return false;
    }
  }

  /**
   * Handle Host a Party button click
   */
  async onHostParty(): Promise<void> {
    this.currentState = 'hosting';
    this.generatedPartyCode = this.generatePartyCode();
    this.isCreatingParty = true;

    const userName =
      localStorage.getItem('userName') || this.generateRandomUserName();

    // Create party in Firestore
    const partyCreated = await this.createPartyInFirestore(
      this.generatedPartyCode,
      userName
    );

    this.isCreatingParty = false;

    if (partyCreated) {
      // Store host mode in localStorage
      const partyData: PartyMode & { userName: string } = {
        mode: 'host',
        partyCode: this.generatedPartyCode,
        isHost: true,
        userName,
      };
      localStorage.setItem('partyMode', JSON.stringify(partyData));
    } else {
      // If party creation failed, generate a new code and try again
      alert('Failed to create party. Please try again.');
      this.onGoBack();
    }
  }

  /**
   * Handle Join a Party button click
   */
  onJoinParty(): void {
    this.currentState = 'joining';
  }

  /**
   * Handle Search Solo button click
   */
  async onSearchSolo(): Promise<void> {
    // Remove any previous party mode
    localStorage.removeItem('partyMode');

    // Store solo mode in localStorage
    const userName =
      localStorage.getItem('userName') || this.generateRandomUserName();

    // Store solo mode in localStorage
    const partyData: PartyMode & { userName: string } = {
      mode: 'solo',
      userName,
    };
    localStorage.setItem('partyMode', JSON.stringify(partyData));

    // Navigate to search page
    this.router.navigate(['/search']);
  }

  /**
   * Copy party code to clipboard
   */
  async copyPartyCode(): Promise<void> {
    try {
      await navigator.clipboard.writeText(this.generatedPartyCode);
      this.isCodeCopied = true;

      // Reset copy feedback after 2 seconds
      setTimeout(() => {
        this.isCodeCopied = false;
      }, 2000);
    } catch (err) {
      console.error('Failed to copy: ', err);
      // Fallback for older browsers
      this.fallbackCopyTextToClipboard(this.generatedPartyCode);
    }
  }

  /**
   * Fallback copy method for older browsers
   */
  private fallbackCopyTextToClipboard(text: string): void {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.top = '0';
    textArea.style.left = '0';
    textArea.style.position = 'fixed';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();

    try {
      document.execCommand('copy');
      this.isCodeCopied = true;
      setTimeout(() => {
        this.isCodeCopied = false;
      }, 2000);
    } catch (err) {
      console.error('Fallback: Could not copy text: ', err);
    }

    document.body.removeChild(textArea);
  }

  /**
   * Validate and join party with entered code
   */
  async onJoinWithCode(): Promise<void> {
    if (!this.enteredPartyCode.trim()) {
      return;
    }

    this.isValidatingCode = true;

    // Verify party exists in Firestore
    const partyExists = await this.verifyPartyExists(
      this.enteredPartyCode.toUpperCase()
    );

    this.isValidatingCode = false;

    if (partyExists) {
      const userName =
        localStorage.getItem('userName') || this.generateRandomUserName();

      // Store guest mode in localStorage
      const partyData: PartyMode & { userName: string } = {
        mode: 'guest',
        partyCode: this.enteredPartyCode.toUpperCase(),
        isHost: false,
        userName,
      };
      localStorage.setItem('partyMode', JSON.stringify(partyData));

      // Navigate to search page
      this.router.navigate(['/search']);
    } else {
      alert(
        'Party not found or no longer accepting guests. Please check the party code and try again.'
      );
    }
  }

  /**
   * Navigate to search page (for host after code generation)
   */
  onProceedToSearch(): void {
    this.router.navigate(['/search']);
  }

  /**
   * Go back to initial state
   */
  onGoBack(): void {
    this.currentState = 'initial';
    this.generatedPartyCode = '';
    this.enteredPartyCode = '';
    this.isCodeCopied = false;
  }

  /**
   * Format party code with spaces for better readability
   */
  getFormattedPartyCode(): string {
    return this.generatedPartyCode.replace(/(.{3})/g, '$1 ').trim();
  }
}
