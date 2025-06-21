# conversational_agent/adk_agents/final_review_agent/schema.py

from pydantic import BaseModel, Field
from typing import List, Optional, Union
from datetime import datetime

class Coordinates(BaseModel):
    latitude: float = Field(description="Restaurant latitude coordinate")
    longitude: float = Field(description="Restaurant longitude coordinate")

class Contact(BaseModel):
    phone: Optional[str] = Field(default=None, description="Restaurant phone number")
    website: Optional[str] = Field(default=None, description="Restaurant website URL")

class Ratings(BaseModel):
    google_rating: float = Field(description="Google rating (0.0-5.0)")
    google_review_count: int = Field(description="Number of Google reviews")
    yelp_rating: Optional[float] = Field(default=None, description="Yelp rating (0.0-5.0)")
    yelp_review_count: Optional[int] = Field(default=None, description="Number of Yelp reviews")

class Pricing(BaseModel):
    price_level: int = Field(description="Price level (1-4)", ge=1, le=4)
    price_symbol: str = Field(description="Price symbol ($, $$, $$$, $$$$)")
    fits_budget: bool = Field(description="Whether the restaurant fits the user's budget")

class CuisineAndFeatures(BaseModel):
    primary_cuisine: str = Field(description="Primary cuisine type")
    secondary_cuisines: List[str] = Field(default_factory=list, description="Additional cuisine types")
    dietary_options: List[str] = Field(default_factory=list, description="Available dietary options")
    key_amenities: List[str] = Field(default_factory=list, description="Key amenities available")
    service_options: List[str] = Field(default_factory=list, description="Service options (dine_in, takeout, delivery)")

class Timing(BaseModel):
    currently_open: bool = Field(description="Whether the restaurant is currently open")
    hours_today: str = Field(description="Today's operating hours")
    best_times_to_visit: List[str] = Field(default_factory=list, description="Optimal visit times")
    current_busyness: Optional[str] = Field(default=None, description="Current busyness level")
    peak_days: List[str] = Field(default_factory=list, description="Peak days of the week")

class Highlights(BaseModel):
    why_recommended: str = Field(description="Personalized recommendation explanation")
    special_items: List[str] = Field(default_factory=list, description="Special menu items")
    standout_features: List[str] = Field(default_factory=list, description="Notable features")
    review_sentiment: Optional[str] = Field(default=None, description="Overall review sentiment")
    review_summary: Optional[str] = Field(default=None, description="Summary of key reviews")

class Media(BaseModel):
    primary_image: Optional[str] = Field(default=None, description="Primary image URL")
    image_alt_text: str = Field(description="Image alt text description")

class PreferenceAlignment(BaseModel):
    cuisine_match: str = Field(description="Cuisine matching quality (Perfect/Good/Partial/None)")
    price_match: str = Field(description="Price matching quality (Perfect/Good/Partial/None)")
    location_convenience: str = Field(description="Location convenience (Excellent/Good/Fair/Poor)")
    amenity_satisfaction: str = Field(description="Amenity satisfaction level (High/Medium/Low)")

class Recommendation(BaseModel):
    rank: int = Field(description="Recommendation rank")
    place_id: str = Field(description="Unique place identifier")
    name: str = Field(description="Restaurant name")
    formatted_address: str = Field(description="Full formatted address")
    coordinates: Coordinates
    contact: Contact
    ratings: Ratings
    pricing: Pricing
    cuisine_and_features: CuisineAndFeatures
    timing: Timing
    highlights: Highlights
    media: Media
    match_score: int = Field(description="Overall match score (0-100)", ge=0, le=100)
    preference_alignment: PreferenceAlignment
    potential_concerns: List[str] = Field(default_factory=list, description="Potential concerns or limitations")

class SearchMetadata(BaseModel):
    total_restaurants_analyzed: int = Field(description="Total number of restaurants analyzed")
    user_location: str = Field(description="User's primary location")
    search_radius_km: Optional[float] = Field(default=None, description="Search radius in kilometers")
    key_preferences: List[str] = Field(description="User's key preferences")
    generated_at: str = Field(description="ISO timestamp of generation")

class Summary(BaseModel):
    total_recommendations: int = Field(description="Total number of recommendations")
    confidence_level: str = Field(description="Confidence level (High/Medium/Low)")
    search_quality_notes: str = Field(description="Notes about data quality and completeness")
    alternative_suggestions: Optional[str] = Field(default=None, description="Alternative suggestions for the user")

class FinalResults(BaseModel):
    search_metadata: SearchMetadata
    recommendations: List[Recommendation] = Field(description="List of restaurant recommendations")
    summary: Summary

class FinalReviewOutput(BaseModel):
    final_results: FinalResults = Field(description="Complete final results with restaurant recommendations")