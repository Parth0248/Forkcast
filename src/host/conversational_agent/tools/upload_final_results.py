# tools/firestore_upload.py
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional
import firebase_admin
from firebase_admin import credentials, firestore as admin_firestore

# from google.adk.tools import Tool

logger = logging.getLogger(__name__)

# Initialize Firebase Admin (do this only once)
try:
    # Check if already initialized
    firebase_admin.get_app()
    print("✅ Firebase Admin already initialized")
except ValueError:
    # Initialize if not already done
    cred = credentials.Certificate("conversational_agent/config/forkcast-0248-firebase-adminsdk-fbsvc-c8f0336fb6.json")
    firebase_admin.initialize_app(cred)
    print("✅ Firebase Admin initialized")

# Get Firestore client from Firebase Admin
db = admin_firestore.client()


def upload_final_results(final_results_json: str, party_code: str) -> Dict[str, Any]:
    """
        Upload final restaurant recommendations to Firestore under a specific party code.
        Args:
            final_results_json (str): JSON string containing final restaurant recommendations.
            party_code (str): Unique identifier for the party.
        Returns:
            Dict: Result of the upload operation, including success status and message.
    """
    
    try:
        results_data = json.loads(final_results_json)
        
        # Validate required structure from Final Review Agent output
        if 'final_results' not in results_data:
            return {
                "success": False,
                "message": "Invalid results format: missing 'final_results' key"
            }
        
        final_results = results_data.get('final_results', {})
        
        # CHECK: Verify party exists first
        party_ref = db.collection('parties').document(party_code)
        party_doc = party_ref.get()
        
        if not party_doc.exists:
            return {
                "success": False,
                "message": f"Party {party_code} not found. Please check the party code."
            }
        
        # Prepare results document
        results_document = {
            'final_results': final_results,
            'party_code': party_code,
            'uploaded_at': admin_firestore.SERVER_TIMESTAMP,
            'status': 'completed',
            'total_recommendations': final_results.get('summary', {}).get('total_recommendations', 0),
            'confidence_level': final_results.get('summary', {}).get('confidence_level', 'Unknown')
        }
        
        # Upload final results to party's results subcollection as 'latest'
        results_ref = party_ref.collection('results').document('latest')
        results_ref.set(results_document)
        
        # Also store a timestamped version for history
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        timestamped_ref = party_ref.collection('results').document(session_doc_id)
        timestamped_ref.set(results_document)
        
        # Update party status (safe because we verified it exists)
        party_ref.update({
            'status': 'results_ready',
            'results_available': True,
            'last_updated': admin_firestore.SERVER_TIMESTAMP,
            'total_recommendations': final_results.get('summary', {}).get('total_recommendations', 0),
            'confidence_level': final_results.get('summary', {}).get('confidence_level', 'Unknown')
        })
        
        total_recs = final_results.get('summary', {}).get('total_recommendations', 0)
        logger.info(f"✅ Final results uploaded for party {party_code} with {total_recs} recommendations")
        
        return {
            "success": True,
            "message": f"Final results uploaded to party {party_code}",
            "party_code": party_code,
            "total_recommendations": total_recs,
            "confidence_level": final_results.get('summary', {}).get('confidence_level', 'Unknown')
        }
        
    except json.JSONDecodeError as e:
        return {
            "success": False,
            "message": f"Invalid JSON format: {str(e)}"
        }
        
    except Exception as e:
        logger.error(f"❌ Results upload failed: {e}")
        return {
            "success": False,
            "message": f"Results upload failed: {str(e)}"
        }