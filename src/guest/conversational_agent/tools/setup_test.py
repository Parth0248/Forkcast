# upload_realistic_test_data.py
"""
Upload realistic preference data for multiple guests to test system robustness
"""

import json
import sys
from datetime import datetime
from typing import List, Dict, Any

def create_realistic_guest_profiles() -> List[Dict[str, Any]]:
    """Create diverse, realistic guest preference profiles"""
    
    guest_profiles = [
        {
            "user_id": "alice_foodie_2024",
            "user_name": "Alice (Foodie)",
            "preferences": {
                "context_preferences": {
                    "group_size": 4,
                    "occasion": "birthday celebration", 
                    "date_time": {
                        "date_preference": "Saturday night",
                        "time_preference": "8:00 PM"
                    }
                },
                "location_preferences": {
                    "text_input_primary": "Downtown San Francisco, Union Square area",
                    "search_radius_km": 2,
                    "max_travel_time_minutes": 15,
                    "avoid_areas": ["Tenderloin"]
                },
                "cuisine_type_preferences": {
                    "desired": ["Italian", "French", "Mediterranean"],
                    "open_to_suggestions": True,
                    "avoid": ["Fast food", "Chain restaurants"]
                },
                "restaurant_specific_preferences": {
                    "price_levels": [3, 4],  # Mid to high-end
                    "min_rating": 4.2,
                    "exclude_chains": True,
                    "attribute_preferences": ["Farm-to-table", "Wine selection"],
                    "specific_restaurants_mentioned": ["Atelier Crenn", "Benu"]
                },
                "dietary_preferences": {
                    "needs": ["Gluten-free options"],
                    "general_notes": "One person has celiac disease, need dedicated gluten-free menu"
                },
                "ambiance_and_amenities": {
                    "ambiances": ["Upscale", "Romantic", "Intimate"],
                    "amenities": ["Valet parking", "Private dining", "Wine sommelier"]
                },
                "willing_to_compromise_on": ["Price range", "Distance"],
                "deal_breakers": ["No gluten-free options", "Too noisy for conversation"]
            }
        },
        
        {
            "user_id": "bob_budget_conscious",
            "user_name": "Bob (Budget-Conscious)",
            "preferences": {
                "context_preferences": {
                    "group_size": 3,
                    "occasion": "casual hangout",
                    "date_time": {
                        "date_preference": "tonight",
                        "time_preference": "6:30 PM"
                    }
                },
                "location_preferences": {
                    "text_input_primary": "Mission District, San Francisco",
                    "search_radius_km": 5,
                    "max_travel_time_minutes": 25,
                    "avoid_areas": []
                },
                "cuisine_type_preferences": {
                    "desired": ["Mexican", "Vietnamese", "Thai", "Indian"],
                    "open_to_suggestions": True,
                    "avoid": ["Expensive fusion", "Fine dining"]
                },
                "restaurant_specific_preferences": {
                    "price_levels": [1, 2],  # Budget to mid-range
                    "min_rating": 3.8,
                    "exclude_chains": False,
                    "attribute_preferences": ["Large portions", "BYOB", "Cash only OK"],
                    "specific_restaurants_mentioned": ["La Taqueria", "Pho Hoa"]
                },
                "dietary_preferences": {
                    "needs": [],
                    "general_notes": "Love spicy food, not picky"
                },
                "ambiance_and_amenities": {
                    "ambiances": ["Casual", "Lively", "Authentic"],
                    "amenities": ["Street parking OK", "No reservations needed"]
                },
                "willing_to_compromise_on": ["Ambiance", "Service quality"],
                "deal_breakers": ["Over $25 per person", "Pretentious atmosphere"]
            }
        },
        
        {
            "user_id": "carol_vegan_health",
            "user_name": "Carol (Health-Conscious Vegan)",
            "preferences": {
                "context_preferences": {
                    "group_size": 2,
                    "occasion": "health-focused dinner",
                    "date_time": {
                        "date_preference": "Friday",
                        "time_preference": "7:00 PM"
                    }
                },
                "location_preferences": {
                    "text_input_primary": "Hayes Valley, San Francisco",
                    "search_radius_km": 4,
                    "max_travel_time_minutes": 20,
                    "avoid_areas": ["Tourist areas"]
                },
                "cuisine_type_preferences": {
                    "desired": ["Vegan", "Plant-based", "Organic", "Mediterranean"],
                    "open_to_suggestions": False,
                    "avoid": ["Meat-heavy", "Fried food", "Heavy dairy"]
                },
                "restaurant_specific_preferences": {
                    "price_levels": [2, 3],
                    "min_rating": 4.0,
                    "exclude_chains": True,
                    "attribute_preferences": ["Organic ingredients", "Local sourcing", "Sustainable practices"],
                    "specific_restaurants_mentioned": ["Loving Hut", "Verdure"]
                },
                "dietary_preferences": {
                    "needs": ["Strictly vegan", "Organic preferred", "No processed foods"],
                    "general_notes": "Looking for clean, whole food options with minimal oil"
                },
                "ambiance_and_amenities": {
                    "ambiances": ["Health-focused", "Peaceful", "Natural"],
                    "amenities": ["Nutritional information available", "Outdoor seating"]
                },
                "willing_to_compromise_on": ["Location"],
                "deal_breakers": ["No vegan options", "Heavily processed food", "Non-organic"]
            }
        },
        
        {
            "user_id": "david_adventure_eater",
            "user_name": "David (Adventure Eater)",
            "preferences": {
                "context_preferences": {
                    "group_size": 5,
                    "occasion": "trying something new",
                    "date_time": {
                        "date_preference": "this weekend",
                        "time_preference": "7:30 PM"
                    }
                },
                "location_preferences": {
                    "text_input_primary": "Richmond District, San Francisco",
                    "search_radius_km": 8,
                    "max_travel_time_minutes": 35,
                    "avoid_areas": []
                },
                "cuisine_type_preferences": {
                    "desired": ["Ethiopian", "Korean", "Peruvian", "Moroccan", "Burmese"],
                    "open_to_suggestions": True,
                    "avoid": ["Basic American", "Chain restaurants"]
                },
                "restaurant_specific_preferences": {
                    "price_levels": [2, 3, 4],
                    "min_rating": 4.1,
                    "exclude_chains": True,
                    "attribute_preferences": ["Authentic", "Chef-owned", "Unique dishes"],
                    "specific_restaurants_mentioned": ["Zuni Cafe", "Mensho"]
                },
                "dietary_preferences": {
                    "needs": [],
                    "general_notes": "Love trying new flavors, no dietary restrictions"
                },
                "ambiance_and_amenities": {
                    "ambiances": ["Authentic", "Adventurous", "Cultural"],
                    "amenities": ["Knowledgeable staff", "Tasting menus available"]
                },
                "willing_to_compromise_on": ["Price", "Wait time"],
                "deal_breakers": ["Boring food", "Overly Americanized versions"]
            }
        },
        
        {
            "user_id": "emma_family_friendly",
            "user_name": "Emma (Family with Kids)",
            "preferences": {
                "context_preferences": {
                    "group_size": 6,
                    "occasion": "family dinner with kids",
                    "date_time": {
                        "date_preference": "Sunday",
                        "time_preference": "5:30 PM"
                    }
                },
                "location_preferences": {
                    "text_input_primary": "Castro District, San Francisco",
                    "search_radius_km": 3,
                    "max_travel_time_minutes": 15,
                    "avoid_areas": ["Too busy areas"]
                },
                "cuisine_type_preferences": {
                    "desired": ["American", "Italian", "Pizza", "Comfort food"],
                    "open_to_suggestions": True,
                    "avoid": ["Very spicy", "Exotic cuisines", "Raw foods"]
                },
                "restaurant_specific_preferences": {
                    "price_levels": [1, 2, 3],
                    "min_rating": 3.9,
                    "exclude_chains": False,
                    "attribute_preferences": ["Kids menu", "High chairs", "Quick service"],
                    "specific_restaurants_mentioned": ["Tony's Pizza", "Mel's Diner"]
                },
                "dietary_preferences": {
                    "needs": ["Kids-friendly options", "Not too spicy"],
                    "general_notes": "Two kids (ages 6 and 9), need simple options they'll actually eat"
                },
                "ambiance_and_amenities": {
                    "ambiances": ["Family-friendly", "Casual", "Kid-tolerant"],
                    "amenities": ["High chairs", "Kids menu", "Crayons/activities", "Fast service"]
                },
                "willing_to_compromise_on": ["Food quality", "Ambiance"],
                "deal_breakers": ["No kids menu", "Too fancy/stuffy", "Long wait times"]
            }
        }
    ]
    
    return guest_profiles

def upload_realistic_test_data(party_code: str = "ROBUST_TEST"):
    """Upload realistic preference data for multiple guests"""
    
    print(f"🎯 Uploading Realistic Test Data to Party: {party_code}")
    print("=" * 60)
    
    try:
        # Import required functions
        from party_management import create_party, join_party
        from firestore_upload import upload_preferences_simple
        
        # Step 1: Create the test party
        print(f"\n🎉 Step 1: Creating test party")
        party_result = create_party(
            host_id="host_robust_test",
            host_name="Alex (Host - Robust Test)"
        )
        
        if party_result['success']:
            party_code = party_result['party_code']
            print(f"✅ Party created: {party_code}")
        else:
            print(f"❌ Failed to create party, using provided code: {party_code}")
            # Continue with provided party code
        
        # Step 2: Get guest profiles
        guest_profiles = create_realistic_guest_profiles()
        print(f"\n👥 Step 2: Uploading {len(guest_profiles)} realistic guest profiles")
        
        successful_uploads = 0
        
        for i, guest in enumerate(guest_profiles, 1):
            print(f"\n   Guest {i}: {guest['user_name']}")
            
            # Join the party
            join_result = join_party(
                party_code=party_code,
                user_id=guest['user_id'],
                user_name=guest['user_name']
            )
            
            if not join_result['success']:
                print(f"      ❌ Failed to join party: {join_result['message']}")
                continue
            
            # Prepare preferences in the correct format
            guest_data = {
                "status": "PREFERENCES_COMPLETE",
                "preferences": guest['preferences']
            }
            
            # Upload preferences
            upload_result = upload_preferences_simple(
                query_details=json.dumps(guest_data),
                party_code=party_code,
                user_id=guest['user_id']
            )
            
            if upload_result['success']:
                successful_uploads += 1
                print(f"      ✅ Preferences uploaded successfully")
                
                # Show key preferences
                prefs = guest['preferences']
                cuisines = prefs.get('cuisine_type_preferences', {}).get('desired', [])
                price_levels = prefs.get('restaurant_specific_preferences', {}).get('price_levels', [])
                location = prefs.get('location_preferences', {}).get('text_input_primary', 'Unknown')
                dietary = prefs.get('dietary_preferences', {}).get('needs', [])
                
                print(f"         🍽️  Cuisines: {cuisines}")
                print(f"         💰 Price: {price_levels}")
                print(f"         📍 Location: {location}")
                if dietary:
                    print(f"         🥗 Dietary: {dietary}")
            else:
                print(f"      ❌ Upload failed: {upload_result['message']}")
        
        print(f"\n📊 Upload Summary:")
        print(f"   ✅ Successfully uploaded: {successful_uploads}/{len(guest_profiles)} guests")
        print(f"   🎉 Party Code: {party_code}")
        
        # Step 3: Verify data structure
        print(f"\n🔍 Step 3: Verifying uploaded data")
        
        import firebase_admin
        from firebase_admin import firestore as admin_firestore
        
        db = admin_firestore.client()
        
        # Get all guests
        guests_ref = db.collection('parties').document(party_code).collection('guests')
        guest_docs = list(guests_ref.stream())
        
        print(f"   📋 Found {len(guest_docs)} guest documents in Firestore")
        
        # Show aggregated data (what host agent would see)
        print(f"\n📈 Aggregated Preference Analysis:")
        
        all_cuisines = []
        all_price_levels = []
        all_locations = []
        all_dietary_needs = []
        
        for doc in guest_docs:
            data = doc.to_dict()
            prefs = data.get('preferences', {})
            
            # Collect cuisines
            cuisines = prefs.get('cuisine_type_preferences', {}).get('desired', [])
            all_cuisines.extend(cuisines)
            
            # Collect price levels
            price_levels = prefs.get('restaurant_specific_preferences', {}).get('price_levels', [])
            all_price_levels.extend(price_levels)
            
            # Collect locations
            location = prefs.get('location_preferences', {}).get('text_input_primary')
            if location:
                all_locations.append(location)
            
            # Collect dietary needs
            dietary = prefs.get('dietary_preferences', {}).get('needs', [])
            all_dietary_needs.extend(dietary)
        
        # Show aggregated insights
        from collections import Counter
        
        print(f"   🍽️  Most popular cuisines: {dict(Counter(all_cuisines).most_common(3))}")
        print(f"   💰 Price level distribution: {dict(Counter(all_price_levels))}")
        print(f"   📍 Location preferences: {set(all_locations)}")
        if all_dietary_needs:
            print(f"   🥗 Dietary requirements: {set(all_dietary_needs)}")
        
        # Create aggregation preview (what host agent would work with)
        print(f"\n🤖 Host Agent Preview - Preference Aggregation Data:")
        
        aggregation_data = {
            "party_code": party_code,
            "total_guests": len(guest_docs),
            "cuisine_preferences": {
                "most_wanted": list(Counter(all_cuisines).most_common(3)),
                "all_requested": list(set(all_cuisines))
            },
            "price_consensus": {
                "range": [min(all_price_levels), max(all_price_levels)] if all_price_levels else [],
                "most_common": Counter(all_price_levels).most_common(1)[0] if all_price_levels else None
            },
            "location_consensus": list(set(all_locations)),
            "dietary_requirements": list(set(all_dietary_needs)),
            "group_size_total": sum([
                doc.to_dict().get('preferences', {}).get('context_preferences', {}).get('group_size', 0) 
                for doc in guest_docs
            ])
        }
        
        print(json.dumps(aggregation_data, indent=2))
        
        print(f"\n🎯 Ready for Host Agent Testing!")
        print(f"   Party Code: {party_code}")
        print(f"   Use this data to test preference aggregation and restaurant search")
        
        return {
            "success": True,
            "party_code": party_code,
            "guests_uploaded": successful_uploads,
            "aggregation_preview": aggregation_data
        }
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure party_management.py and firestore_upload.py are in the same directory")
        return {"success": False, "error": str(e)}
        
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        return {"success": False, "error": str(e)}

def view_uploaded_test_data(party_code: str):
    """View the uploaded test data in detail"""
    
    print(f"🔍 Viewing Uploaded Test Data for Party: {party_code}")
    print("=" * 50)
    
    try:
        import firebase_admin
        from firebase_admin import firestore as admin_firestore
        
        db = admin_firestore.client()
        
        # Get party info
        party_doc = db.collection('parties').document(party_code).get()
        if not party_doc.exists:
            print(f"❌ Party {party_code} not found")
            return
        
        party_data = party_doc.to_dict()
        print(f"🎉 Party: {party_data.get('host_name', 'Unknown Host')}")
        print(f"   Status: {party_data.get('status')}")
        print(f"   Members: {party_data.get('member_count', 0)}")
        
        # Get all guests
        guests_ref = db.collection('parties').document(party_code).collection('guests')
        guest_docs = guests_ref.stream()
        
        print(f"\n👥 Guest Details:")
        
        for i, doc in enumerate(guest_docs, 1):
            data = doc.to_dict()
            prefs = data.get('preferences', {})
            
            print(f"\n   Guest {i}: {doc.id}")
            print(f"   📅 Uploaded: {data.get('uploaded_at')}")
            
            # Show key preferences in a readable format
            context = prefs.get('context_preferences', {})
            location = prefs.get('location_preferences', {})
            cuisine = prefs.get('cuisine_type_preferences', {})
            restaurant = prefs.get('restaurant_specific_preferences', {})
            dietary = prefs.get('dietary_preferences', {})
            ambiance = prefs.get('ambiance_and_amenities', {})
            
            print(f"   🍽️  Cuisines: {cuisine.get('desired', [])} (avoid: {cuisine.get('avoid', [])})")
            print(f"   📍 Location: {location.get('text_input_primary', 'Not specified')}")
            print(f"   💰 Price Range: {restaurant.get('price_levels', [])} (min rating: {restaurant.get('min_rating', 'any')})")
            print(f"   👥 Group Size: {context.get('group_size', 'Not specified')}")
            print(f"   🕐 Time: {context.get('date_time', {}).get('time_preference', 'Flexible')}")
            
            if dietary.get('needs'):
                print(f"   🥗 Dietary: {dietary['needs']}")
            if dietary.get('general_notes'):
                print(f"   📝 Notes: {dietary['general_notes']}")
            
            if ambiance.get('ambiances'):
                print(f"   🎵 Ambiance: {ambiance['ambiances']}")
                
    except Exception as e:
        print(f"❌ Error viewing data: {e}")

if __name__ == "__main__":
    print(f"🚀 Forkcast Realistic Test Data Uploader")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Upload the realistic test data
    result = upload_realistic_test_data()
    
    if result['success']:
        party_code = result['party_code']
        
        print(f"\n" + "="*60)
        print(f"🎉 SUCCESS! Uploaded {result['guests_uploaded']} realistic guest profiles")
        print(f"🎯 Party Code: {party_code}")
        print(f"📋 Ready for robust testing of your preference aggregation system!")
        
        # Optionally view the detailed data
        print(f"\n🔍 Detailed view of uploaded data:")
        view_uploaded_test_data(party_code)
        
    else:
        print(f"❌ Upload failed: {result.get('error')}")
    
    print(f"\n📝 Next Steps:")
    print(f"   1. Use party code '{result.get('party_code', 'N/A')}' for testing")
    print(f"   2. Test your host agent's preference aggregation")
    print(f"   3. Verify search results with diverse preferences")
    print(f"   4. Check conflict resolution (vegan vs non-vegan, budget vs luxury)")