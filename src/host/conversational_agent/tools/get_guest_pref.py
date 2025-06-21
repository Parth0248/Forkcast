# tools/host_preference_aggregator_simple.py
import json
import logging
from typing import Dict, Any, List, Optional
from collections import Counter
import firebase_admin
from firebase_admin import credentials, firestore as admin_firestore

logger = logging.getLogger(__name__)

# Initialize Firebase Admin (same as other files)
try:
    firebase_admin.get_app()
except ValueError:
    cred = credentials.Certificate("conversational_agent/config/forkcast-0248-firebase-adminsdk-fbsvc-c8f0336fb6.json")
    firebase_admin.initialize_app(cred)

db = admin_firestore.client()

def fetch_and_integrate_preferences(party_code: str, host_preferences: Optional[str] = None) -> Dict[str, Any]:
    """
    Fetch guest preferences from Firestore and integrate with host preferences
    
    Args:
        party_code (str): The party code to fetch preferences for
        host_preferences (str): Optional JSON string of host preferences to integrate
        
    Returns:
        Dict with combined preferences in standard format
    """
    try:
        # Step 1: Fetch guest preferences from Firestore
        guests_ref = db.collection('parties').document(party_code).collection('guests')
        guest_docs = list(guests_ref.stream())
        
        if not guest_docs:
            return {
                "success": False,
                "message": f"No guest preferences found for party {party_code}",
                "guest_count": 0
            }
        
        # Collect all guest preferences
        all_guest_preferences = []
        for doc in guest_docs:
            guest_data = doc.to_dict()
            preferences = guest_data.get('preferences', {})
            if preferences:
                all_guest_preferences.append({
                    'user_id': doc.id,
                    'preferences': preferences,
                    'uploaded_at': guest_data.get('uploaded_at')
                })
        
        # Step 2: Aggregate guest preferences
        aggregated_guest_prefs = _aggregate_guest_preferences(all_guest_preferences)
        
        # Step 3: Integrate host preferences if provided
        if host_preferences:
            try:
                host_prefs_data = json.loads(host_preferences)
                host_prefs_section = host_prefs_data.get('preferences', {})
                final_prefs = _integrate_host_with_guest_preferences(aggregated_guest_prefs, host_prefs_section)
                integration_message = f"Integrated host preferences with {len(all_guest_preferences)} guest preferences"
            except (json.JSONDecodeError, KeyError) as e:
                logger.warning(f"Invalid host preferences format: {e}")
                final_prefs = aggregated_guest_prefs
                integration_message = f"Used guest preferences only (host preferences invalid)"
        else:
            final_prefs = aggregated_guest_prefs
            integration_message = f"Aggregated {len(all_guest_preferences)} guest preferences"
        
        # Step 4: Format in standard query_details structure
        combined_query_details = {
            "status": "PREFERENCES_AGGREGATED",
            "last_user_utterance": f"Combined preferences from {len(all_guest_preferences)} guests" + (" + host input" if host_preferences else ""),
            "preferences": final_prefs,
            "meta_preferences_for_results": {
                "sorting_preference": "relevance",
                "presentation_format": "summary", 
                "number_of_options_to_present": 6
            },
            "constraints_summary": {
                "must_haves_summary": [],
                "nice_to_haves_summary": []
            },
            "processing_flags": {
                "iteration_count": 1,
                "missing_critical_fields": [],
                "clarification_focus": None,
                "clarification_question_suggestion": None,
                "last_agent_processed": "HostPreferenceAggregator",
                "ready_for_search_by_upa": True,
                "aggregated_from_guests": True,
                "host_input_integrated": bool(host_preferences),
                "guest_count": len(all_guest_preferences),
                "error_message": None
            }
        }
        
        logger.info(f"✅ {integration_message} for party {party_code}")
        
        return {
            "success": True,
            "message": integration_message,
            "party_code": party_code,
            "guest_count": len(all_guest_preferences),
            "host_input_provided": bool(host_preferences),
            "combined_preferences": json.dumps(combined_query_details)
        }
        
    except Exception as e:
        logger.error(f"❌ Preference integration failed: {e}")
        return {
            "success": False,
            "message": f"Failed to process preferences: {str(e)}",
            "error": str(e)
        }

def _integrate_host_with_guest_preferences(guest_prefs: Dict[str, Any], host_prefs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Integrate host preferences with aggregated guest preferences. Host preferences take priority in conflicts.
    Args:
        guest_prefs: Aggregated guest preferences
        host_prefs: Host's individual preferences
        
    Returns:
        Combined preferences with host priority
    """
    # Start with guest preferences as base
    combined = guest_prefs.copy()
    
    # Context preferences - host overrides for occasion, host additions for group size
    if 'context_preferences' in host_prefs:
        host_context = host_prefs['context_preferences']
        
        # Host occasion takes priority
        if host_context.get('occasion'):
            combined['context_preferences']['occasion'] = host_context['occasion']
        
        # Add host group size to total (host might add +1 for themselves)
        if host_context.get('group_size'):
            current_size = combined['context_preferences'].get('group_size') or 0
            host_size = host_context['group_size'] or 0
            combined['context_preferences']['group_size'] = current_size + host_size
        
        # Host time preference takes priority if more specific
        if host_context.get('date_time', {}).get('time_preference'):
            combined['context_preferences']['date_time']['time_preference'] = host_context['date_time']['time_preference']
        if host_context.get('date_time', {}).get('date_preference'):
            combined['context_preferences']['date_time']['date_preference'] = host_context['date_time']['date_preference']
    
    # Location preferences - host takes priority
    if 'location_preferences' in host_prefs:
        host_location = host_prefs['location_preferences']
        
        if host_location.get('text_input_primary'):
            combined['location_preferences']['text_input_primary'] = host_location['text_input_primary']
        
        if host_location.get('search_radius_km') is not None:
            # Use more restrictive radius - fix None comparison issue
            guest_radius = combined['location_preferences'].get('search_radius_km')
            if guest_radius is None or host_location['search_radius_km'] < guest_radius:
                combined['location_preferences']['search_radius_km'] = host_location['search_radius_km']
        
        # Add host avoid areas to guest avoid areas
        if host_location.get('avoid_areas'):
            combined['location_preferences']['avoid_areas'].extend(host_location['avoid_areas'])
            combined['location_preferences']['avoid_areas'] = list(set(combined['location_preferences']['avoid_areas']))
    
    # Cuisine preferences - combine with host priority
    if 'cuisine_type_preferences' in host_prefs:
        host_cuisine = host_prefs['cuisine_type_preferences']
        
        # Add host desired cuisines to front of list (priority)
        if host_cuisine.get('desired'):
            guest_desired = combined['cuisine_type_preferences'].get('desired', [])
            # Host cuisines first, then unique guest cuisines
            combined_desired = host_cuisine['desired'] + [c for c in guest_desired if c not in host_cuisine['desired']]
            combined['cuisine_type_preferences']['desired'] = combined_desired
        
        # Combine avoid lists (union)
        if host_cuisine.get('avoid'):
            combined['cuisine_type_preferences']['avoid'].extend(host_cuisine['avoid'])
            combined['cuisine_type_preferences']['avoid'] = list(set(combined['cuisine_type_preferences']['avoid']))
        
        # Host open_to_suggestions takes priority if false (more restrictive)
        if 'open_to_suggestions' in host_cuisine and not host_cuisine['open_to_suggestions']:
            combined['cuisine_type_preferences']['open_to_suggestions'] = False
    
    # Dietary preferences - union (accommodate everyone including host)
    if 'dietary_preferences' in host_prefs:
        host_dietary = host_prefs['dietary_preferences']
        
        if host_dietary.get('needs'):
            combined['dietary_preferences']['needs'].extend(host_dietary['needs'])
            combined['dietary_preferences']['needs'] = list(set(combined['dietary_preferences']['needs']))
        
        # Host dietary notes take priority or get combined
        if host_dietary.get('general_notes'):
            guest_notes = combined['dietary_preferences'].get('general_notes', '')
            if guest_notes:
                combined['dietary_preferences']['general_notes'] = f"{host_dietary['general_notes']}; {guest_notes}"
            else:
                combined['dietary_preferences']['general_notes'] = host_dietary['general_notes']
    
    # Restaurant preferences - host takes priority on restrictive preferences
    if 'restaurant_specific_preferences' in host_prefs:
        host_restaurant = host_prefs['restaurant_specific_preferences']
        
        # Price levels - use intersection if host is more restrictive, otherwise host preference
        if host_restaurant.get('price_levels'):
            guest_prices = set(combined['restaurant_specific_preferences'].get('price_levels', []))
            host_prices = set(host_restaurant['price_levels'])
            
            # If there's overlap, use intersection; otherwise use host preference
            intersection = guest_prices.intersection(host_prices)
            if intersection:
                combined['restaurant_specific_preferences']['price_levels'] = sorted(list(intersection))
            else:
                combined['restaurant_specific_preferences']['price_levels'] = sorted(host_restaurant['price_levels'])
        
        # Minimum rating - use higher rating (more restrictive) - fix None comparison issue
        if host_restaurant.get('min_rating') is not None:
            guest_rating = combined['restaurant_specific_preferences'].get('min_rating')
            if guest_rating is None:
                combined['restaurant_specific_preferences']['min_rating'] = host_restaurant['min_rating']
            else:
                combined['restaurant_specific_preferences']['min_rating'] = max(guest_rating, host_restaurant['min_rating'])
        
        # Exclude chains - use True if either host or guests want it
        if 'exclude_chains' in host_restaurant:
            guest_exclude = combined['restaurant_specific_preferences'].get('exclude_chains', False)
            combined['restaurant_specific_preferences']['exclude_chains'] = guest_exclude or host_restaurant['exclude_chains']
        
        # Attribute preferences - combine
        if host_restaurant.get('attribute_preferences'):
            combined['restaurant_specific_preferences']['attribute_preferences'].extend(host_restaurant['attribute_preferences'])
            combined['restaurant_specific_preferences']['attribute_preferences'] = list(set(combined['restaurant_specific_preferences']['attribute_preferences']))
    
    # Ambiance and amenities - combine all
    if 'ambiance_and_amenities' in host_prefs:
        host_ambiance = host_prefs['ambiance_and_amenities']
        
        if host_ambiance.get('ambiances'):
            combined['ambiance_and_amenities']['ambiances'].extend(host_ambiance['ambiances'])
            combined['ambiance_and_amenities']['ambiances'] = list(set(combined['ambiance_and_amenities']['ambiances']))
        
        if host_ambiance.get('amenities'):
            combined['ambiance_and_amenities']['amenities'].extend(host_ambiance['amenities'])
            combined['ambiance_and_amenities']['amenities'] = list(set(combined['ambiance_and_amenities']['amenities']))
    
    # Deal breakers - union (respect everyone's deal breakers)
    if host_prefs.get('deal_breakers'):
        combined['deal_breakers'].extend(host_prefs['deal_breakers'])
        combined['deal_breakers'] = list(set(combined['deal_breakers']))
    
    return combined

def _aggregate_guest_preferences(guest_preferences: List[Dict]) -> Dict[str, Any]:
    """
    Aggregate guest preferences into a single preference structure
    
    Args:
        guest_preferences: List of guest preference dictionaries
        
    Returns:
        Aggregated preferences in standard format
    """
    if not guest_preferences:
        return {}
    
    # Initialize aggregated structure with safe defaults
    aggregated = {
        "context_preferences": {
            "group_size": 0,
            "occasion": None,
            "date_time": {
                "date_preference": None,
                "time_preference": None
            }
        },
        "location_preferences": {
            "text_input_primary": None,
            "text_input_secondary": None,
            "coordinates_primary": {
                "latitude": None,
                "longitude": None
            },
            "search_radius_km": None,
            "max_travel_time_minutes": None,
            "avoid_areas": []
        },
        "cuisine_type_preferences": {
            "desired": [],
            "open_to_suggestions": True,
            "avoid": []
        },
        "dietary_preferences": {
            "needs": [],
            "general_notes": None
        },
        "restaurant_specific_preferences": {
            "price_levels": [],
            "min_rating": None,
            "attribute_preferences": [],
            "exclude_chains": False,
            "specific_restaurants_mentioned": []
        },
        "ambiance_and_amenities": {
            "ambiances": [],
            "amenities": []
        },
        "willing_to_compromise_on": [],
        "deal_breakers": []
    }
    
    # Collect all values for aggregation
    all_cuisines = []
    all_avoid_cuisines = []
    all_price_levels = []
    all_dietary_needs = []
    all_locations = []
    all_ambiances = []
    all_amenities = []
    all_deal_breakers = []
    all_group_sizes = []
    all_occasions = []
    all_times = []
    all_dates = []
    min_ratings = []
    exclude_chains_votes = []
    
    # Extract data from all guests
    for guest in guest_preferences:
        prefs = guest['preferences']
        
        # Context preferences
        context = prefs.get('context_preferences', {})
        if context.get('group_size') is not None:
            all_group_sizes.append(context['group_size'])
        if context.get('occasion'):
            all_occasions.append(context['occasion'])
        
        date_time = context.get('date_time', {})
        if date_time.get('time_preference'):
            all_times.append(date_time['time_preference'])
        if date_time.get('date_preference'):
            all_dates.append(date_time['date_preference'])
        
        # Location preferences
        location = prefs.get('location_preferences', {})
        if location.get('text_input_primary'):
            all_locations.append(location['text_input_primary'])
        
        # Cuisine preferences
        cuisine = prefs.get('cuisine_type_preferences', {})
        all_cuisines.extend(cuisine.get('desired', []))
        all_avoid_cuisines.extend(cuisine.get('avoid', []))
        
        # Dietary preferences
        dietary = prefs.get('dietary_preferences', {})
        all_dietary_needs.extend(dietary.get('needs', []))
        
        # Restaurant preferences
        restaurant = prefs.get('restaurant_specific_preferences', {})
        all_price_levels.extend(restaurant.get('price_levels', []))
        if restaurant.get('min_rating') is not None:
            min_ratings.append(restaurant['min_rating'])
        if 'exclude_chains' in restaurant:
            exclude_chains_votes.append(restaurant['exclude_chains'])
        
        # Ambiance and amenities
        ambiance = prefs.get('ambiance_and_amenities', {})
        all_ambiances.extend(ambiance.get('ambiances', []))
        all_amenities.extend(ambiance.get('amenities', []))
        
        # Deal breakers
        all_deal_breakers.extend(prefs.get('deal_breakers', []))
    
    # Aggregate the data using most common/consensus logic
    
    # Context - sum group sizes, most common occasion/time
    aggregated['context_preferences']['group_size'] = sum(all_group_sizes) if all_group_sizes else 0
    aggregated['context_preferences']['occasion'] = Counter(all_occasions).most_common(1)[0][0] if all_occasions else None
    aggregated['context_preferences']['date_time']['time_preference'] = Counter(all_times).most_common(1)[0][0] if all_times else None
    aggregated['context_preferences']['date_time']['date_preference'] = Counter(all_dates).most_common(1)[0][0] if all_dates else None
    
    # Location - most common location
    aggregated['location_preferences']['text_input_primary'] = Counter(all_locations).most_common(1)[0][0] if all_locations else None
    
    # Cuisines - keep popular ones, combine all avoids
    cuisine_counts = Counter(all_cuisines)
    aggregated['cuisine_type_preferences']['desired'] = [cuisine for cuisine, count in cuisine_counts.most_common(5)]
    aggregated['cuisine_type_preferences']['avoid'] = list(set(all_avoid_cuisines))
    
    # Dietary - union of all needs (everyone must be accommodated)
    aggregated['dietary_preferences']['needs'] = list(set(all_dietary_needs))
    
    # Restaurant - consensus on price range and rating
    if all_price_levels:
        price_counter = Counter(all_price_levels)
        # Include price levels that appear more than once OR if only a few unique levels
        popular_prices = [price for price, count in price_counter.items() if count > 1 or len(price_counter) <= 3]
        aggregated['restaurant_specific_preferences']['price_levels'] = sorted(list(set(popular_prices))) if popular_prices else sorted(list(set(all_price_levels)))
    
    if min_ratings:
        # Use the highest minimum rating to satisfy everyone - ensure no None values
        valid_ratings = [r for r in min_ratings if r is not None]
        aggregated['restaurant_specific_preferences']['min_rating'] = max(valid_ratings) if valid_ratings else None
    
    # Exclude chains if majority wants it
    if exclude_chains_votes:
        aggregated['restaurant_specific_preferences']['exclude_chains'] = sum(exclude_chains_votes) > len(exclude_chains_votes) / 2
    
    # Ambiance - popular choices
    ambiance_counts = Counter(all_ambiances)
    aggregated['ambiance_and_amenities']['ambiances'] = [amb for amb, count in ambiance_counts.most_common(3)]
    
    amenity_counts = Counter(all_amenities)
    aggregated['ambiance_and_amenities']['amenities'] = [amt for amt, count in amenity_counts.most_common(3)]
    
    # Deal breakers - union (respect everyone's deal breakers)
    aggregated['deal_breakers'] = list(set(all_deal_breakers))
    
    return aggregated