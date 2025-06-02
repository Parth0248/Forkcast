import uuid

def get_default_query_details():
    """
    Returns the default structure for query_details to be stored in session.state.
    """
    return {
        "query_id": str(uuid.uuid4()), # Generate a unique ID for each new query
        "session_id": None, # Will be populated by ADK session
        "user_id": None, # string, for future personalization via BigQuery
        "status": "NEW_QUERY",
        # Possible statuses:
        # "NEW_QUERY" -> "GATHERING_PREFERENCES" -> "CLARIFICATION_NEEDED" ->
        # "PREFERENCES_PARTIALLY_FILLED" -> "PREFERENCES_COMPLETE" -> "READY_FOR_SEARCH"
        "last_user_utterance": None,
        "conversation_history": [], # List of {"role": "user" or "agent", "content": "message"}
        "preferences": {
            "context": {
                "group_size": None, # integer (e.g., 4)
                "occasion": None, # string (e.g., "casual lunch", "birthday dinner", "date night")
                "date_time": {
                    "date_preference": None, # string ("tonight", "tomorrow", "YYYY-MM-DD", "next Friday")
                    "time_preference": None # string ("around 7 PM", "lunchtime", "HH:MM", "anytime")
                }
            },
            "location": {
                "text_input_primary": None, # string (e.g., "downtown", "near Eiffel Tower", "123 Main St, Surat")
                "text_input_secondary": None,
                "coordinates_primary": {
                    "latitude": None, # float
                    "longitude": None # float
                },
                "search_radius_km": None, # integer (e.g., 2, 5)
                "max_travel_time_minutes": None, # integer (e.g., 15, 30)
                "avoid_areas": [] # list of strings
            },
            "food_drink": {
                "cuisine_types": {
                    "desired": [], # list of strings (e.g., ["Italian", "Pizza", "North Indian"])
                    "open_to_suggestions": True, # boolean
                    "avoid": [] # list of strings (e.g., ["Very Spicy Food", "Fast Food Chains"])
                },
                "dietary_needs": [], # list of objects, e.g., { "type": "Vegan", "strictness": "must_have", "details": "Whole group is vegan" }
                "specific_dishes_keywords": [], # list of strings (e.g., ["wood-fired pizza", "fresh pasta", "craft beer"])
                "drink_preferences": {
                    "alcoholic": [], # e.g., ["craft beer", "wine list"]
                    "non_alcoholic": [], # e.g., ["fresh juice", "specialty coffee"]
                    "bar_type_desired": None
                }
            },
            "establishment": {
                "price_range_preference": None, # string (e.g., "budget-friendly", "$$", "upscale")
                "price_per_person": {
                    "min": None, "max": None, "currency": "INR"
                },
                "ambiance_atmosphere": {
                    "desired": [], # list of strings (e.g., "not too noisy", "casual", "romantic")
                    "avoid": [],
                    "lighting": None,
                    "music": None
                },
                "service_qualities": {
                    "speed": None, # "quick bite", "leisurely meal"
                    "type": None # "attentive service", "self-service"
                },
                "operational": {
                    "open_now_required": False, # boolean
                    "reservations_preference": None, # "required", "preferred", "not_needed"
                    "wait_time_tolerance_minutes": None
                },
                "facilities_amenities": {
                    "desired": [], # e.g., ["outdoor seating", "pet-friendly", "parking available"]
                    "deal_breakers": []
                },
                "type_of_place": [], # e.g., ["restaurant", "cafe", "bar"]
                "chain_preference": None # "prefer_independents", "no_chains", "chains_ok"
            }
        },
        "meta_preferences_for_results": {
            "number_of_options_to_see": 3,
            "ranking_priority": [], # e.g., [{"field": "dietary_needs.vegan", "weight": 1.0}]
            "leeway_factor_acceptable": False
        },
        "constraints_summary": { # Populated by UserPreferenceAgent
            "must_have_tags": [],
            "deal_breaker_tags": []
        },
        "processing_flags":{ # For internal agent communication within the loop
            "missing_critical_fields": [], # List of dot-notation paths to fields
            "clarification_needed_for_field": None, # Dot-notation path to a field
            "clarification_question_suggestion": None, # Suggested question string
            "last_agent_processed": None # "ConversationalAgent" or "UserPreferenceAgent"
        }
    }