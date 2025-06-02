import uuid
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field

# === CORE PREFERENCE MODELS ===

class DateTimePreferences(BaseModel):
    """When the user wants to dine"""
    date_preference: Optional[str] = Field(None, description="e.g., 'tonight', 'tomorrow', '2024-01-15'")
    time_preference: Optional[str] = Field(None, description="e.g., 'dinner', '7pm', 'lunch'")

class ContextPreferences(BaseModel):
    """Context about the dining occasion"""
    group_size: Optional[int] = Field(None, description="Number of people dining", ge=1)
    occasion: Optional[str] = Field(None, description="e.g., 'date night', 'business meeting', 'family dinner'")
    date_time: DateTimePreferences = Field(default_factory=DateTimePreferences)

class Coordinates(BaseModel):
    """Geographic coordinates"""
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)

class LocationPreferences(BaseModel):
    """Where the user wants to dine"""
    text_input_primary: Optional[str] = Field(None, description="Main location text, e.g., 'downtown', 'near Central Park'")
    text_input_secondary: Optional[str] = Field(None, description="Secondary location or landmark")
    coordinates_primary: Coordinates = Field(default_factory=Coordinates)
    search_radius_km: Optional[int] = Field(None, description="Search radius in kilometers", ge=1, le=50)
    max_travel_time_minutes: Optional[int] = Field(None, description="Maximum travel time", ge=5, le=120)
    avoid_areas: List[str] = Field(default_factory=list, description="Areas to avoid")

class CuisineTypePreferences(BaseModel):
    """Food type preferences"""
    desired: List[str] = Field(default_factory=list, description="Preferred cuisines, e.g., ['Italian', 'Mexican']")
    open_to_suggestions: bool = Field(True, description="Whether open to other cuisine suggestions")
    avoid: List[str] = Field(default_factory=list, description="Cuisines to avoid")

class DietaryNeed(BaseModel):
    """Individual dietary requirement"""
    type: str = Field(..., description="e.g., 'vegetarian', 'gluten-free', 'halal', 'vegan'")
    strictness: Literal["must_have", "strong_preference", "nice_to_have"] = Field("must_have")
    details: Optional[str] = Field(None, description="Additional details about the dietary need")

class DietaryPreferences(BaseModel):
    """All dietary requirements and restrictions"""
    needs: List[DietaryNeed] = Field(default_factory=list)
    general_notes: Optional[str] = Field(None, description="General dietary notes, e.g., 'no nuts anywhere'")

class AttributePreference(BaseModel):
    """Restaurant attribute preference"""
    name: str = Field(..., description="e.g., 'outdoor_seating', 'good_for_kids', 'live_music'")
    preference_level: Literal["must_have", "nice_to_have", "must_not_have"] = Field("nice_to_have")

class RestaurantSpecificPreferences(BaseModel):
    """Specific restaurant requirements"""
    price_levels: List[int] = Field(default_factory=list, description="Price levels: 1=$, 2=$$, 3=$$$, 4=$$$$")
    min_rating: Optional[float] = Field(None, description="Minimum rating (1.0-5.0)", ge=1.0, le=5.0)
    attribute_preferences: List[AttributePreference] = Field(default_factory=list)
    exclude_chains: bool = Field(False, description="Whether to exclude chain restaurants")
    specific_restaurants_mentioned: List[str] = Field(default_factory=list, description="Specific restaurants mentioned by user")

class AmbianceAndAmenities(BaseModel):
    """Atmosphere and facility preferences"""
    ambiances: List[str] = Field(default_factory=list, description="e.g., ['romantic', 'casual', 'upscale']")
    amenities: List[str] = Field(default_factory=list, description="e.g., ['wifi', 'parking', 'bar', 'patio']")

# === MAIN PREFERENCES CONTAINER ===

class AllPreferences(BaseModel):
    """Complete user preferences for restaurant search"""
    context_preferences: ContextPreferences = Field(default_factory=ContextPreferences)
    location_preferences: LocationPreferences = Field(default_factory=LocationPreferences)
    cuisine_type_preferences: CuisineTypePreferences = Field(default_factory=CuisineTypePreferences)
    dietary_preferences: DietaryPreferences = Field(default_factory=DietaryPreferences)
    restaurant_specific_preferences: RestaurantSpecificPreferences = Field(default_factory=RestaurantSpecificPreferences)
    ambiance_and_amenities: AmbianceAndAmenities = Field(default_factory=AmbianceAndAmenities)
    
    # Flexibility indicators
    willing_to_compromise_on: List[str] = Field(default_factory=list, description="Areas user is flexible on")
    deal_breakers: List[str] = Field(default_factory=list, description="Non-negotiable requirements")

# === META AND PROCESSING MODELS ===

class MetaPreferences(BaseModel):
    """How to present results to user"""
    sorting_preference: Literal["relevance", "distance", "rating", "price_low_to_high", "price_high_to_low"] = "relevance"
    presentation_format: Literal["summary", "detailed_list", "comparison_table"] = "summary"
    number_of_options_to_present: int = Field(3, ge=1, le=10)

class ConstraintsSummary(BaseModel):
    """Summary of key constraints for search"""
    must_haves_summary: List[str] = Field(default_factory=list, description="Critical requirements")
    nice_to_haves_summary: List[str] = Field(default_factory=list, description="Preferred but not required")

class ProcessingFlags(BaseModel):
    """Internal processing state and guidance"""
    iteration_count: int = Field(0, description="Number of conversation turns processed")
    missing_critical_fields: List[str] = Field(default_factory=list, description="Fields needed for search")
    clarification_focus: Optional[str] = Field(None, description="What to clarify next: 'location', 'cuisine', 'price_level'")
    clarification_question_suggestion: Optional[str] = Field(None, description="Suggested question to ask user")
    last_agent_processed: Optional[Literal["ConversationalAgent", "UserPreferenceAgent"]] = None
    ready_for_search_by_upa: bool = Field(False, description="UPA assessment: ready for search")
    error_message: Optional[str] = Field(None, description="Any processing errors")

class ConversationTurn(BaseModel):
    """Single conversation exchange"""
    role: Literal["user", "agent"] = Field(..., description="Who spoke")
    content: str = Field(..., description="What was said")
    timestamp: str = Field(default_factory=lambda: str(uuid.uuid4().hex), description="Turn identifier")

# === MAIN QUERY DETAILS MODEL ===

class QueryDetails(BaseModel):
    """Complete state for a restaurant search conversation"""
    
    # Core identifiers
    query_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    session_id: Optional[str] = None
    user_id: Optional[str] = None
    
    # Processing status
    status: Literal[
        "NEW_QUERY",                        # Just started
        "GATHERING_PREFERENCES",            # Collecting user preferences
        "CLARIFICATION_NEEDED",             # Need more info from user
        "PREFERENCES_PARTIALLY_FILLED",     # Have some but not all preferences
        "PREFERENCES_COMPLETE",             # All needed preferences collected
        "READY_FOR_SEARCH",                 # Ready to search restaurants
        "MAX_ITERATIONS_REACHED_INCOMPLETE", # Hit conversation limit
        "ERROR_PROCESSING_PREFERENCES"      # Something went wrong
    ] = "NEW_QUERY"
    
    # Conversation state
    last_user_utterance: Optional[str] = Field(None, description="Most recent user message")
    conversation_history: List[ConversationTurn] = Field(default_factory=list)
    
    # User preferences and search configuration
    preferences: AllPreferences = Field(default_factory=AllPreferences)
    meta_preferences_for_results: MetaPreferences = Field(default_factory=MetaPreferences)
    constraints_summary: ConstraintsSummary = Field(default_factory=ConstraintsSummary)
    processing_flags: ProcessingFlags = Field(default_factory=ProcessingFlags)

    @classmethod
    def get_default_instance(cls, session_id: Optional[str] = None, user_id: Optional[str] = None) -> 'QueryDetails':
        """Create a new QueryDetails instance with all defaults populated"""
        return cls(
            session_id=session_id,
            user_id=user_id,
            preferences=AllPreferences(),
            meta_preferences_for_results=MetaPreferences(),
            constraints_summary=ConstraintsSummary(),
            processing_flags=ProcessingFlags(),
            conversation_history=[]
        )

    def add_user_message(self, message: str) -> None:
        """Helper to add user message to conversation history"""
        self.conversation_history.append(ConversationTurn(role="user", content=message))
        self.last_user_utterance = message

    def add_agent_message(self, message: str) -> None:
        """Helper to add agent message to conversation history"""
        self.conversation_history.append(ConversationTurn(role="agent", content=message))

    class Config:
        validate_assignment = True
        extra = "forbid"  # Prevent accidental field additions