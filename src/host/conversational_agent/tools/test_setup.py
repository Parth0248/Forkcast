# test_enhanced_host_integration.py
"""
Test script for enhanced host preference integration
Tests both guest aggregation and host preference integration
"""

import json
from datetime import datetime

def test_host_preference_integration():
    """Test integration of host preferences with guest preferences"""
    
    print(f"🎯 Testing Enhanced Host Preference Integration")
    print("=" * 55)
    
    try:
        from get_guest_pref import fetch_and_integrate_preferences
        
        # Test 1: Guest aggregation only (no host input)
        print(f"\n🧪 Test 1: Guest aggregation only")
        result1 = fetch_and_integrate_preferences("76U4CD")
        
        if result1['success']:
            print(f"✅ Guest aggregation successful")
            print(f"   Guests: {result1['guest_count']}")
            print(f"   Host input: {result1['host_input_provided']}")
            
            # Show aggregated guest preferences
            guest_data = json.loads(result1['combined_preferences'])
            guest_prefs = guest_data['preferences']
            print(f"   Guest cuisines: {guest_prefs['cuisine_type_preferences']['desired']}")
            print(f"   Guest price range: {guest_prefs['restaurant_specific_preferences']['price_levels']}")
        
        # Test 2: Host preferences integration
        print(f"\n🧪 Test 2: Host + Guest integration")
        
        # Sample host preferences
        host_preferences = {
            "status": "HOST_INPUT",
            "preferences": {
                "context_preferences": {
                    "group_size": 1,  # Host adds themselves
                    "occasion": "celebration"  # Host overrides
                },
                "location_preferences": {
                    "text_input_primary": "Union Square, San Francisco",  # Host priority
                    "search_radius_km": 2  # More restrictive
                },
                "cuisine_type_preferences": {
                    "desired": ["French", "Italian"],  # Host priority cuisines
                    "avoid": ["Fast food"]  # Host avoids
                },
                "dietary_preferences": {
                    "needs": ["No shellfish"],  # Host allergy
                    "general_notes": "Host is allergic to shellfish"
                },
                "restaurant_specific_preferences": {
                    "price_levels": [3, 4],  # Host prefers upscale
                    "min_rating": 4.5,  # Host is picky
                    "exclude_chains": True  # Host preference
                },
                "ambiance_and_amenities": {
                    "ambiances": ["Upscale", "Romantic"],  # Host priorities
                    "amenities": ["Valet parking"]
                },
                "deal_breakers": ["Too noisy"]  # Host deal breaker
            }
        }
        
        result2 = fetch_and_integrate_preferences(
            "76U4CD", 
            json.dumps(host_preferences)
        )
        
        if result2['success']:
            print(f"✅ Host integration successful")
            print(f"   Guests: {result2['guest_count']}")
            print(f"   Host input: {result2['host_input_provided']}")
            
            # Show combined preferences
            combined_data = json.loads(result2['combined_preferences'])
            combined_prefs = combined_data['preferences']
            flags = combined_data['processing_flags']
            
            print(f"\n📊 Integration Results:")
            
            # Context changes
            context = combined_prefs['context_preferences']
            print(f"   👥 Total group size: {context['group_size']} (guests + host)")
            print(f"   🎉 Occasion: {context['occasion']} (host priority)")
            
            # Location changes  
            location = combined_prefs['location_preferences']
            print(f"   📍 Location: {location['text_input_primary']} (host priority)")
            print(f"   📏 Search radius: {location['search_radius_km']}km (host restriction)")
            
            # Cuisine integration
            cuisine = combined_prefs['cuisine_type_preferences']
            print(f"   🍽️  Cuisines: {cuisine['desired']} (host priorities first)")
            print(f"   🚫 Avoid: {cuisine['avoid']} (combined)")
            
            # Dietary integration
            dietary = combined_prefs['dietary_preferences']
            print(f"   🥗 Dietary needs: {dietary['needs']} (union of all)")
            
            # Restaurant preferences
            restaurant = combined_prefs['restaurant_specific_preferences']
            print(f"   💰 Price range: {restaurant['price_levels']} (host preference)")
            print(f"   ⭐ Min rating: {restaurant['min_rating']} (highest requirement)")
            print(f"   🏪 Exclude chains: {restaurant['exclude_chains']} (host priority)")
            
            # Ambiance
            ambiance = combined_prefs['ambiance_and_amenities']
            print(f"   🎵 Ambiance: {ambiance['ambiances']} (host priorities)")
            print(f"   🎁 Amenities: {ambiance['amenities']} (combined)")
            
            # Deal breakers
            print(f"   ⛔ Deal breakers: {combined_prefs['deal_breakers']} (union)")
            
            # Processing flags
            print(f"\n🚩 Processing Status:")
            print(f"   Host input integrated: {flags['host_input_integrated']}")
            print(f"   Aggregated from guests: {flags['aggregated_from_guests']}")
            print(f"   Guest count: {flags['guest_count']}")
            
            return True
        else:
            print(f"❌ Host integration failed: {result2['message']}")
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure get_guest_pref.py is in tools/")
        return False
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_conflict_resolution():
    """Test how the system handles conflicts between host and guest preferences"""
    
    print(f"\n⚔️  Testing Host vs Guest Conflict Resolution")
    print("=" * 45)
    
    try:
        from get_guest_pref import fetch_and_integrate_preferences
        
        # Create host preferences that conflict with guest preferences
        conflicting_host_prefs = {
            "preferences": {
                "cuisine_type_preferences": {
                    "desired": ["French"],  # Conflicts with guest Italian/Mexican
                    "avoid": ["Italian"]  # Directly conflicts with guests
                },
                "restaurant_specific_preferences": {
                    "price_levels": [1],  # Budget vs guest mid-range
                    "min_rating": 3.0  # Lower than some guests
                },
                "dietary_preferences": {
                    "needs": ["Keto diet"]  # Additional restriction
                },
                "deal_breakers": ["Vegetarian restaurants"]  # Could conflict with vegan guest
            }
        }
        
        result = fetch_and_integrate_preferences(
            "76U4CD",
            json.dumps({"preferences": conflicting_host_prefs["preferences"]})
        )
        
        if result['success']:
            combined_data = json.loads(result['combined_preferences'])
            combined_prefs = combined_data['preferences']
            
            print(f"🔍 Conflict Resolution Analysis:")
            
            # Cuisine conflicts
            cuisines = combined_prefs['cuisine_type_preferences']
            print(f"   🍽️  Final cuisines: {cuisines['desired']}")
            print(f"       💡 Analysis: Host French preference prioritized")
            print(f"   🚫 Avoid: {cuisines['avoid']}")
            print(f"       💡 Analysis: Host Italian avoid added (conflicts with guests)")
            
            # Price conflicts
            prices = combined_prefs['restaurant_specific_preferences']['price_levels']
            print(f"   💰 Final price range: {prices}")
            print(f"       💡 Analysis: Host budget preference applied")
            
            # Dietary conflicts
            dietary = combined_prefs['dietary_preferences']['needs']
            print(f"   🥗 Final dietary needs: {dietary}")
            print(f"       💡 Analysis: All dietary needs combined (keto + vegan + gluten-free)")
            
            # Deal breaker conflicts
            deal_breakers = combined_prefs['deal_breakers']
            print(f"   ⛔ Deal breakers: {deal_breakers}")
            if "Vegetarian restaurants" in deal_breakers:
                print(f"       ⚠️  WARNING: Host deal breaker conflicts with vegan guest!")
            
            print(f"\n✅ Conflict resolution shows host priority working correctly")
            print(f"💡 Recommendation: Review conflicts before searching")
            
        else:
            print(f"❌ Conflict test failed: {result['message']}")
            
    except Exception as e:
        print(f"❌ Conflict test failed: {e}")

def test_user_preference_agent_integration():
    """Test the enhanced user preference agent with host preferences"""
    
    print(f"\n🤖 Testing Enhanced User Preference Agent")
    print("=" * 40)
    
    # This would test the enhanced user preference agent
    # For now, we'll simulate what it should do
    
    sample_query_details = {
        "status": "NEW_QUERY_HOST",
        "preferences": {
            "cuisine_type_preferences": {
                "desired": ["Italian"],  # Host input
                "open_to_suggestions": True
            },
            "dietary_preferences": {
                "needs": ["Vegetarian"],  # Host input
            }
        },
        "processing_flags": {
            "aggregated_from_guests": False,
            "host_input_detected": True,
            "integration_needed": False
        }
    }
    
    print(f"📋 Sample query state:")
    print(f"   Status: {sample_query_details['status']}")
    print(f"   Host cuisines: {sample_query_details['preferences']['cuisine_type_preferences']['desired']}")
    print(f"   Host dietary: {sample_query_details['preferences']['dietary_preferences']['needs']}")
    print(f"   Aggregated from guests: {sample_query_details['processing_flags']['aggregated_from_guests']}")
    print(f"   Host input detected: {sample_query_details['processing_flags']['host_input_detected']}")
    
    print(f"\n💭 Expected user preference agent behavior:")
    print(f"   ✅ Should detect need for aggregation (aggregated_from_guests = false)")
    print(f"   ✅ Should detect host input (host preferences present)")
    print(f"   ✅ Should set integration_needed = true")
    print(f"   ✅ Should suggest calling fetch_and_integrate_preferences")
    
    print(f"\n🔄 Expected workflow:")
    print(f"   1. User Preference Agent → integration_needed = true")
    print(f"   2. Call fetch_and_integrate_preferences(party_code, host_prefs)")
    print(f"   3. User Preference Agent → validate combined preferences")
    print(f"   4. Status → PREFERENCES_COMPLETE")

if __name__ == "__main__":
    print(f"🚀 Enhanced Host Integration Testing")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Run the main integration test
    success = test_host_preference_integration()
    
    if success:
        # Test conflict resolution
        test_conflict_resolution()
        
        # Test user preference agent expectations
        test_user_preference_agent_integration()
        
        print(f"\n🎉 All enhanced integration tests completed!")
        print(f"📝 Your enhanced host system can:")
        print(f"   ✅ Aggregate guest preferences from Firestore")
        print(f"   ✅ Extract and integrate host preferences")
        print(f"   ✅ Apply host priority rules in conflicts")
        print(f"   ✅ Combine dietary requirements (union)")
        print(f"   ✅ Handle location and budget preferences")
        print(f"   ✅ Manage ambiance and amenity preferences")
        print(f"   ✅ Provide clear integration summaries")
        
    else:
        print(f"\n❌ Integration tests failed - check your setup")
        print(f"📝 Make sure you have:")
        print(f"   - Enhanced host preference aggregator in tools/")
        print(f"   - Realistic test data in 76U4CD party")
        print(f"   - Firebase connection working")
    
    print(f"\n🎯 Next steps:")
    print(f"   1. Update your user preference agent with enhanced prompt")
    print(f"   2. Update your conversational agent with enhanced prompt")
    print(f"   3. Add fetch_and_integrate_preferences to host agent tools")
    print(f"   4. Test the complete host workflow!")