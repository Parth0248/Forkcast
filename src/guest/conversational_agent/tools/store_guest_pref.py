# tools/store_guest_pref.py
import json
import logging
import os
from datetime import datetime
from typing import Dict, Any, Optional
import firebase_admin
from firebase_admin import credentials, firestore as admin_firestore

logger = logging.getLogger(__name__)

# Initialize Firebase Admin (do this only once)
try:
    # Check if already initialized
    firebase_admin.get_app()
    print("✅ Firebase Admin already initialized")
except ValueError:
    # Try multiple approaches for Firebase credentials
    cred = None
    
    # Approach 1: Try service account file paths
    possible_paths = [
        "conversational_agent/config/forkcast-0248-firebase-adminsdk-fbsvc-c8f0336fb6.json",
        "../config/forkcast-0248-firebase-adminsdk-fbsvc-c8f0336fb6.json",
        "./forkcast-0248-firebase-adminsdk-fbsvc-c8f0336fb6.json",
        os.path.join(os.path.dirname(__file__), "..", "config", "forkcast-0248-firebase-adminsdk-fbsvc-c8f0336fb6.json"),
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            print(f"✅ Found Firebase service account at: {path}")
            try:
                cred = credentials.Certificate(path)
                break
            except Exception as e:
                print(f"⚠️ Failed to load credentials from {path}: {e}")
                continue
    
    # Approach 2: Try Application Default Credentials if no file found
    if cred is None:
        try:
            print("ℹ️ No service account file found, using Application Default Credentials")
            cred = credentials.ApplicationDefault()
        except Exception as e:
            print(f"⚠️ Application Default Credentials failed: {e}")
    
    # Approach 3: Minimal initialization for deployment environment
    if cred is None:
        print("ℹ️ Using minimal Firebase initialization for deployed environment")
        # In deployed environment, try with just project ID
        try:
            firebase_admin.initialize_app(options={'projectId': 'forkcast-460406'})
        except Exception as e:
            print(f"⚠️ Minimal Firebase init failed: {e}")
            raise
    else:
        firebase_admin.initialize_app(cred)
    
    print("✅ Firebase Admin initialized")

# Get Firestore client from Firebase Admin
try:
    db = admin_firestore.client()
    print("✅ Firestore client initialized")
except Exception as e:
    print(f"⚠️ Firestore client initialization failed: {e}")
    db = None

def extract_first_json_object(s: str) -> Optional[dict]:
    """
    Extracts the first valid JSON object from a string.
    """
    start = s.find('{')
    if start == -1:
        return None
    stack = []
    for i in range(start, len(s)):
        if s[i] == '{':
            stack.append('{')
        elif s[i] == '}':
            stack.pop()
            if not stack:
                try:
                    return json.loads(s[start:i+1])
                except Exception as e:
                    logger.error(f"Failed to parse extracted JSON: {e}")
                    return None
    return None

def upload_preferences(query_details: str, party_code: str, user_id: str) -> Dict[str, Any]:
    """
        Upload user preferences to Firestore under a specific party code.
        Args:
            query_details (str): JSON string containing user preferences.
            party_code (str) : Unique identifier for the party.
            user_id (str): Unique identifier for the user.
        Returns:
            Dict: Result of the upload operation, including success status and message.
    """
    
    # Check if Firestore is available
    if db is None:
        return {
            "success": False,
            "message": "Firestore is not available in this environment. Database operations are disabled."
        }
    
    try:
        preferences_data = extract_first_json_object(query_details)
        if preferences_data is None:
            return {
                "success": False,
                "message": "Could not extract a valid JSON object from input."
            }
        user_preferences = preferences_data.get('preferences', {})
        
        # CHECK: Verify party exists first
        party_ref = db.collection('parties').document(party_code)
        party_doc = party_ref.get()
        
        if not party_doc.exists:
            return {
                "success": False,
                "message": f"Party {party_code} not found. Please check the party code."
            }
        
        # Create guest document reference
        guest_ref = party_ref.collection('guests').document(user_id)
        
        # Upload guest data
        guest_ref.set({
            'preferences': user_preferences,
            'user_id': user_id,
            'uploaded_at': admin_firestore.SERVER_TIMESTAMP,
            'status': 'submitted'
        })
        
        # Update party status (safe because we verified it exists)
        party_ref.update({
            'last_updated': admin_firestore.SERVER_TIMESTAMP,
            'status': 'collecting_preferences'
        })
        
        logger.info(f"✅ Preferences uploaded for user {user_id} to party {party_code}")
        
        return {
            "success": True,
            "message": f"Preferences uploaded to party {party_code}",
            "party_code": party_code
        }
        
    except Exception as e:
        logger.error(f"❌ Upload failed: {e}")
        return {
            "success": False,
            "message": f"Upload failed: {str(e)}"
        }