# """
# Forkcast Callback Functions
# ==========================

# This module contains callback functions for the Forkcast conversational agent system.
# These callbacks help validate user input relevance and protect the system from 
# irrelevant or malicious queries.
# """

# import re
# from typing import Optional, List, Set

# from google.adk.callback import CallbackContext
# from google.adk import types

# def validate_restaurant_relevance(callback_context: CallbackContext) -> Optional[types.Content]:
#     """
#     Before agent callback to validate if user input is relevant to restaurant/food domain.
#     Prevents irrelevant queries from reaching the conversational agent.
    
#     Returns:
#         None: If query is relevant, allows normal agent execution
#         types.Content: If query is irrelevant, returns a polite redirection message
#     """
#     agent_name = callback_context.agent_name
#     invocation_id = callback_context.invocation_id
    
#     # Get the current conversation state and user input
#     current_state = callback_context.state.to_dict()
    
#     # Extract user input from the most recent message
#     user_input = ""
#     if hasattr(callback_context, 'messages') and callback_context.messages:
#         # Get the last user message
#         for message in reversed(callback_context.messages):
#             if message.role == "user" and message.parts:
#                 user_input = message.parts[0].text if message.parts[0].text else ""
#                 break
    
#     # If no user input found, check state for current input
#     if not user_input and "current_user_input" in current_state:
#         user_input = current_state.get("current_user_input", "")
    
#     print(f"\n[Callback] Validating relevance for agent: {agent_name} (Inv: {invocation_id})")
#     print(f"[Callback] User input: {user_input[:100]}...")  # Log first 100 chars
    
#     # If no input to validate, proceed normally
#     if not user_input or len(user_input.strip()) < 3:
#         print(f"[Callback] No substantial input to validate, proceeding normally.")
#         return None
    
#     # Check if the input is relevant to restaurant/food domain
#     if not _is_restaurant_relevant(user_input):
#         print(f"[Callback] Input deemed irrelevant to restaurant domain, blocking execution.")
        
#         # Return a polite redirection message
#         redirect_message = (
#             "I'm Forkcast, your restaurant recommendation assistant! 🍽️ "
#             "I'm here to help you find the perfect dining spots based on your preferences. "
#             "Please let me know what type of food you're in the mood for, your budget, "
#             "location preferences, or any specific dining requirements you have. "
#             "How can I help you find a great restaurant today?"
#         )
        
#         return types.Content(
#             parts=[types.Part(text=redirect_message)],
#             role="model"
#         )
    
#     print(f"[Callback] Input is relevant to restaurant domain, proceeding normally.")
#     return None


# def _is_restaurant_relevant(user_input: str) -> bool:
#     """
#     Determine if user input is relevant to restaurant/food domain.
    
#     Args:
#         user_input: The user's message text
        
#     Returns:
#         bool: True if relevant, False if irrelevant
#     """
#     if not user_input:
#         return False
    
#     # Normalize input for analysis
#     text = user_input.lower().strip()
    
#     # Very short inputs that might be spam or testing
#     if len(text) < 3:
#         return False
    
#     # Keywords that indicate restaurant/food relevance
#     food_keywords = {
#         # Food types and cuisines
#         'food', 'eat', 'hungry', 'restaurant', 'cafe', 'dine', 'dining', 'meal', 'lunch', 'dinner', 
#         'breakfast', 'brunch', 'snack', 'cuisine', 'dish', 'menu', 'order', 'delivery', 'takeout',
#         'italian', 'chinese', 'mexican', 'indian', 'thai', 'japanese', 'american', 'french', 
#         'mediterranean', 'asian', 'european', 'latin', 'african', 'korean', 'vietnamese',
        
#         # Food items
#         'pizza', 'burger', 'pasta', 'sushi', 'tacos', 'sandwich', 'salad', 'soup', 'steak', 
#         'chicken', 'seafood', 'vegetarian', 'vegan', 'dessert', 'drinks', 'coffee', 'tea',
        
#         # Dining preferences and attributes
#         'cheap', 'expensive', 'budget', 'fancy', 'casual', 'formal', 'fast', 'slow', 'romantic',
#         'family', 'kids', 'date', 'group', 'business', 'quiet', 'loud', 'outdoor', 'indoor',
#         'reservation', 'booking', 'table', 'bar', 'patio', 'terrace', 'rooftop',
        
#         # Location and logistics
#         'near', 'nearby', 'close', 'around', 'location', 'address', 'directions', 'distance',
#         'walk', 'drive', 'uber', 'delivery', 'pickup', 'open', 'hours', 'closed',
        
#         # Restaurant features
#         'rating', 'review', 'recommend', 'good', 'best', 'popular', 'favorite', 'new', 'trendy',
#         'authentic', 'fresh', 'quality', 'service', 'atmosphere', 'ambiance', 'vibe',
        
#         # Dietary requirements
#         'gluten', 'dairy', 'nuts', 'allergy', 'kosher', 'halal', 'organic', 'healthy', 'diet',
        
#         # Common greetings/conversation starters that might be relevant
#         'hello', 'hi', 'hey', 'morning', 'afternoon', 'evening', 'hungry', 'craving', 'want', 'need',
#         'looking', 'search', 'find', 'help', 'suggest', 'recommend'
#     }
    
#     # Location indicators (common in restaurant queries)
#     location_patterns = [
#         r'\b(in|near|around|at|by)\s+[a-zA-Z\s]+\b',  # "in downtown", "near me", etc.
#         r'\b\d+\s*(mile|km|block|min|minute)s?\b',      # Distance references
#         r'\b(downtown|uptown|city|suburb|mall|plaza|street|avenue|boulevard)\b'
#     ]
    
#     # Check for obvious irrelevant patterns first
#     irrelevant_patterns = [
#         r'\b(weather|news|sports|politics|science|technology|programming|code|math|history)\b',
#         r'\b(cat|dog|pet|animal|car|house|movie|book|game|music|song)\b',
#         r'\b(job|work|career|school|study|homework|assignment)\b',
#         r'\b(health|doctor|medicine|symptom|sick|pain|ache)\b',
#         r'\b(stock|investment|money|bank|finance|crypto|bitcoin)\b',
#         r'^\s*(test|testing|hello world|123|abc|xyz|asdf|qwerty)\s*$',  # Common test inputs
#         r'^\s*[!@#$%^&*()_+=\[\]{}|;:,.<>?]+\s*$',  # Only special characters
#         r'^(.)\1{4,}$',  # Repeated characters (aaaaa, 11111, etc.)
#     ]
    
#     # First check if it's obviously irrelevant
#     for pattern in irrelevant_patterns:
#         if re.search(pattern, text):
#             # But give benefit of doubt if it also contains food keywords
#             food_word_count = sum(1 for word in food_keywords if word in text)
#             if food_word_count < 1:
#                 return False
    
#     # Check for food/restaurant keywords
#     food_word_count = sum(1 for word in food_keywords if word in text)
    
#     # Check for location patterns
#     location_match = any(re.search(pattern, text) for pattern in location_patterns)
    
#     # Determine relevance based on multiple factors
#     word_count = len(text.split())
    
#     # Short messages need stronger food relevance
#     if word_count <= 3:
#         return food_word_count >= 1
    
#     # Medium messages need some food relevance or location context
#     elif word_count <= 10:
#         return food_word_count >= 1 or location_match
    
#     # Longer messages can be relevant with less strict requirements
#     else:
#         return food_word_count >= 1 or location_match or _contains_question_about_recommendations(text)


# def _contains_question_about_recommendations(text: str) -> bool:
#     """Check if the text contains questions that could be about recommendations."""
#     question_patterns = [
#         r'\b(what|where|which|how|can you|could you|would you)\b.*\b(recommend|suggest|good|best|find)\b',
#         r'\b(i want|i need|i\'m looking|looking for|help me)\b',
#         r'\b(any suggestions|any recommendations|what do you think)\b'
#     ]
    
#     return any(re.search(pattern, text, re.IGNORECASE) for pattern in question_patterns)

"""
Forkcast Callback Functions
==========================

This module contains callback functions for the Forkcast conversational agent system.
These callbacks help validate user input relevance and protect the system from 
irrelevant or malicious queries.

Author: Forkcast Team
"""

import re
from typing import Optional, List, Set

from google.adk.callback import CallbackContext
from google.adk import types


# ===================================================================
# MAIN CALLBACK FUNCTIONS
# ===================================================================

def validate_restaurant_relevance(callback_context: CallbackContext) -> Optional[types.Content]:
    """
    Before agent callback to validate if user input is relevant to restaurant/food domain.
    Prevents irrelevant queries from reaching the conversational agent.
    
    Args:
        callback_context: The callback context containing agent info, state, and messages
        
    Returns:
        None: If query is relevant, allows normal agent execution
        types.Content: If query is irrelevant, returns a polite redirection message
    """
    agent_name = callback_context.agent_name
    invocation_id = callback_context.invocation_id
    
    # Get the current conversation state and user input
    current_state = callback_context.state.to_dict()
    
    # Extract user input from the most recent message
    user_input = _extract_user_input(callback_context, current_state)
    
    print(f"\n[Callback] Validating relevance for agent: {agent_name} (Inv: {invocation_id})")
    print(f"[Callback] User input: {user_input[:100]}...")  # Log first 100 chars
    
    # If no input to validate, proceed normally
    if not user_input or len(user_input.strip()) < 3:
        print(f"[Callback] No substantial input to validate, proceeding normally.")
        return None
    
    # Check if the input is relevant to restaurant/food domain
    if not is_restaurant_relevant(user_input):
        print(f"[Callback] Input deemed irrelevant to restaurant domain, blocking execution.")
        
        # Return a polite redirection message
        redirect_message = _get_redirection_message()
        
        return types.Content(
            parts=[types.Part(text=redirect_message)],
            role="model"
        )
    
    print(f"[Callback] Input is relevant to restaurant domain, proceeding normally.")
    return None


def log_agent_execution(callback_context: CallbackContext) -> Optional[types.Content]:
    """
    Optional callback for logging agent execution details.
    Can be used for monitoring and debugging purposes.
    
    Args:
        callback_context: The callback context
        
    Returns:
        None: Always allows normal execution
    """
    agent_name = callback_context.agent_name
    invocation_id = callback_context.invocation_id
    current_state = callback_context.state.to_dict()
    
    print(f"\n[Log Callback] Agent: {agent_name} | Invocation: {invocation_id}")
    print(f"[Log Callback] State keys: {list(current_state.keys())}")
    
    # Always proceed with normal execution
    return None


# ===================================================================
# CORE RELEVANCE VALIDATION FUNCTIONS
# ===================================================================

def is_restaurant_relevant(user_input: str) -> bool:
    """
    Determine if user input is relevant to restaurant/food domain.
    
    Args:
        user_input: The user's message text
        
    Returns:
        bool: True if relevant, False if irrelevant
    """
    if not user_input:
        return False
    
    # Normalize input for analysis
    text = user_input.lower().strip()
    
    # Very short inputs that might be spam or testing
    if len(text) < 3:
        return False
    
    # Check for obvious irrelevant patterns first
    if _is_obviously_irrelevant(text):
        # But give benefit of doubt if it also contains food keywords
        food_word_count = _count_food_keywords(text)
        if food_word_count < 1:
            return False
    
    # Check for food/restaurant keywords
    food_word_count = _count_food_keywords(text)
    
    # Check for location patterns
    location_match = _contains_location_patterns(text)
    
    # Determine relevance based on multiple factors
    word_count = len(text.split())
    
    # Short messages need stronger food relevance
    if word_count <= 3:
        return food_word_count >= 1
    
    # Medium messages need some food relevance or location context
    elif word_count <= 10:
        return food_word_count >= 1 or location_match
    
    # Longer messages can be relevant with less strict requirements
    else:
        return food_word_count >= 1 or location_match or _contains_recommendation_request(text)


# ===================================================================
# HELPER FUNCTIONS
# ===================================================================

def _extract_user_input(callback_context: CallbackContext, current_state: dict) -> str:
    """Extract user input from callback context or state."""
    user_input = ""
    
    # Try to get from messages first
    if hasattr(callback_context, 'messages') and callback_context.messages:
        # Get the last user message
        for message in reversed(callback_context.messages):
            if message.role == "user" and message.parts:
                user_input = message.parts[0].text if message.parts[0].text else ""
                break
    
    # If no user input found, check state for current input
    if not user_input and "current_user_input" in current_state:
        user_input = current_state.get("current_user_input", "")
    
    return user_input


def _get_redirection_message() -> str:
    """Get a polite redirection message for irrelevant queries."""
    return (
        "I'm Forkcast, your restaurant recommendation assistant! 🍽️ "
        "I'm here to help you find the perfect dining spots based on your preferences. "
        "Please let me know what type of food you're in the mood for, your budget, "
        "location preferences, or any specific dining requirements you have. "
        "How can I help you find a great restaurant today?"
    )


def _get_food_keywords() -> Set[str]:
    """Get the comprehensive set of food and restaurant related keywords."""
    return {
        # Food types and cuisines
        'food', 'eat', 'hungry', 'restaurant', 'cafe', 'dine', 'dining', 'meal', 'lunch', 'dinner', 
        'breakfast', 'brunch', 'snack', 'cuisine', 'dish', 'menu', 'order', 'delivery', 'takeout',
        'italian', 'chinese', 'mexican', 'indian', 'thai', 'japanese', 'american', 'french', 
        'mediterranean', 'asian', 'european', 'latin', 'african', 'korean', 'vietnamese',
        'greek', 'turkish', 'lebanese', 'persian', 'moroccan', 'ethiopian', 'brazilian',
        
        # Food items
        'pizza', 'burger', 'pasta', 'sushi', 'tacos', 'sandwich', 'salad', 'soup', 'steak', 
        'chicken', 'seafood', 'vegetarian', 'vegan', 'dessert', 'drinks', 'coffee', 'tea',
        'burrito', 'quesadilla', 'ramen', 'pho', 'curry', 'noodles', 'rice', 'bread',
        'fish', 'beef', 'pork', 'lamb', 'shrimp', 'lobster', 'crab', 'oyster',
        
        # Dining preferences and attributes
        'cheap', 'expensive', 'budget', 'fancy', 'casual', 'formal', 'fast', 'slow', 'romantic',
        'family', 'kids', 'date', 'group', 'business', 'quiet', 'loud', 'outdoor', 'indoor',
        'reservation', 'booking', 'table', 'bar', 'patio', 'terrace', 'rooftop', 'cozy',
        'upscale', 'fine dining', 'fast food', 'street food', 'food truck', 'buffet',
        
        # Location and logistics
        'near', 'nearby', 'close', 'around', 'location', 'address', 'directions', 'distance',
        'walk', 'drive', 'uber', 'delivery', 'pickup', 'open', 'hours', 'closed',
        'downtown', 'uptown', 'neighborhood', 'area', 'district', 'zone',
        
        # Restaurant features
        'rating', 'review', 'recommend', 'good', 'best', 'popular', 'favorite', 'new', 'trendy',
        'authentic', 'fresh', 'quality', 'service', 'atmosphere', 'ambiance', 'vibe',
        'clean', 'busy', 'crowded', 'empty', 'wait time', 'reservation', 'book',
        
        # Dietary requirements
        'gluten', 'dairy', 'nuts', 'allergy', 'kosher', 'halal', 'organic', 'healthy', 'diet',
        'lactose', 'celiac', 'paleo', 'keto', 'low carb', 'sugar free', 'fat free',
        
        # Common greetings/conversation starters that might be relevant
        'hello', 'hi', 'hey', 'morning', 'afternoon', 'evening', 'hungry', 'craving', 'want', 'need',
        'looking', 'search', 'find', 'help', 'suggest', 'recommend', 'advice', 'opinion',
        
        # Restaurant types
        'bistro', 'pub', 'gastropub', 'tavern', 'grill', 'steakhouse', 'diner', 'bakery',
        'pizzeria', 'taqueria', 'sushi bar', 'wine bar', 'cocktail bar', 'lounge',
        'food court', 'market', 'delicatessen', 'deli', 'cafeteria', 'brewery'
    }


def _get_irrelevant_patterns() -> List[str]:
    """Get regex patterns for obviously irrelevant content."""
    return [
        r'\b(weather|news|sports|politics|science|technology|programming|code|math|history)\b',
        r'\b(cat|dog|pet|animal|car|house|movie|book|game|music|song)\b',
        r'\b(job|work|career|school|study|homework|assignment)\b',
        r'\b(health|doctor|medicine|symptom|sick|pain|ache)\b',
        r'\b(stock|investment|money|bank|finance|crypto|bitcoin)\b',
        r'^\s*(test|testing|hello world|123|abc|xyz|asdf|qwerty)\s*$',  # Common test inputs
        r'^\s*[!@#$%^&*()_+=\[\]{}|;:,.<>?]+\s*$',  # Only special characters
        r'^(.)\1{4,}$',  # Repeated characters (aaaaa, 11111, etc.)
        r'\b(shopping|clothing|fashion|shoes|makeup|beauty)\b',
        r'\b(travel|vacation|hotel|flight|airline|ticket)\b',
        r'\b(love|relationship|dating|marriage|family drama)\b'
    ]


def _get_location_patterns() -> List[str]:
    """Get regex patterns for location-related content."""
    return [
        r'\b(in|near|around|at|by)\s+[a-zA-Z\s]+\b',  # "in downtown", "near me", etc.
        r'\b\d+\s*(mile|km|block|min|minute)s?\b',      # Distance references
        r'\b(downtown|uptown|city|suburb|mall|plaza|street|avenue|boulevard)\b',
        r'\b(zip|zipcode|postal|area code)\b',
        r'\b\d{5}(-\d{4})?\b',  # ZIP codes
        r'\b[A-Z]{2}\s+\d{5}\b'  # State + ZIP
    ]


def _count_food_keywords(text: str) -> int:
    """Count food-related keywords in the text."""
    food_keywords = _get_food_keywords()
    return sum(1 for word in food_keywords if word in text)


def _is_obviously_irrelevant(text: str) -> bool:
    """Check if text matches obviously irrelevant patterns."""
    irrelevant_patterns = _get_irrelevant_patterns()
    
    for pattern in irrelevant_patterns:
        if re.search(pattern, text):
            return True
    return False


def _contains_location_patterns(text: str) -> bool:
    """Check if text contains location-related patterns."""
    location_patterns = _get_location_patterns()
    return any(re.search(pattern, text) for pattern in location_patterns)


def _contains_recommendation_request(text: str) -> bool:
    """Check if the text contains questions that could be about recommendations."""
    question_patterns = [
        r'\b(what|where|which|how|can you|could you|would you)\b.*\b(recommend|suggest|good|best|find)\b',
        r'\b(i want|i need|i\'m looking|looking for|help me)\b',
        r'\b(any suggestions|any recommendations|what do you think)\b',
        r'\b(show me|tell me|give me)\b.*\b(options|choices|places)\b'
    ]
    
    return any(re.search(pattern, text, re.IGNORECASE) for pattern in question_patterns)
