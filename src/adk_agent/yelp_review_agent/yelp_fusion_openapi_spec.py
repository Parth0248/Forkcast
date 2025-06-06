YELP_OPENAPI_SPEC = {
    "openapi": "3.0.0",
    "info": {
        "title": "Yelp Fusion API - Business Search", # Slightly more descriptive
        "version": "v3", # Consistent with Yelp API version
        "description": "OpenAPI specification for the Yelp Fusion API's /v3/businesses/search endpoint. Requires Bearer Token (API Key) authentication."
    },
    "servers": [
        {
            "url": "https://api.yelp.com"
        }
    ],
    "components": { # Define security schemes here
        "securitySchemes": {
            
        }
    },
    "security": [ # Apply 'BearerAuth' globally to all paths in this spec
        {
            
        }
    ],
    "paths": {
        "/v3/businesses/search": {
            "get": {
                "summary": "Search for businesses on Yelp",
                "operationId": "searchYelpBusinesses",
                "description": "Searches for businesses based on a term (e.g., restaurant name) and a location (e.g., address/city). Intended for finding specific matches or a limited list of relevant businesses.",
    
                "parameters": [
                    {
                        "name": "term",
                        "in": "query",
                        "required": False, # Yelp allows search by location/categories without a term
                        "schema": {
                            "type": "string"
                        },
                        "description": "Search term (e.g., 'restaurants', 'Sushi Gen')."
                    },
                    {
                        "name": "location",
                        "in": "query",
                        "required": True, # Location is generally required or highly recommended
                        "schema": {
                            "type": "string"
                        },
                        "description": "Search location (e.g., 'San Francisco', '422 E 2nd St, Los Angeles')."
                    },
                    {
                        "name": "limit",
                        "in": "query",
                        "required": False,
                        "schema": {
                            "type": "integer",
                            "default": 5, # A slightly more useful default than 1
                            "minimum": 1,
                            "maximum": 50 # Yelp's max
                        },
                        "description": "Number of business results to return (default: 5, max: 50)."
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful search operation. Returns a list of businesses.",
                        "content": {
                            "application/json": {
                                "schema": { # Using the detailed schema from our previous discussions
                                    "type": "object",
                                    "properties": {
                                        "businesses": {
                                            "type": "array",
                                            "description": "A list of business objects.",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    "id": {"type": "string", "description": "Unique Yelp ID."},
                                                    "alias": {"type": "string", "description": "Unique Yelp alias."},
                                                    "name": {"type": "string", "description": "Name of the business."},
                                                    "image_url": {"type": "string", "format": "url", "description": "URL of business's main photo."},
                                                    "is_closed": {"type": "boolean"},
                                                    "url": {"type": "string", "format": "url", "description": "URL for business page on Yelp."},
                                                    "review_count": {"type": "integer"},
                                                    "categories": {
                                                        "type": "array",
                                                        "items": {
                                                            "type": "object",
                                                            "properties": {
                                                                "alias": {"type": "string"},
                                                                "title": {"type": "string"}
                                                            }
                                                        }
                                                    },
                                                    "rating": {"type": "number", "format": "float"},
                                                    "coordinates": {
                                                        "type": "object",
                                                        "properties": {
                                                            "latitude": {"type": "number"},
                                                            "longitude": {"type": "number"}
                                                        }
                                                    },
                                                    "transactions": {"type": "array", "items": {"type": "string"}},
                                                    "price": {"type": "string", "description": "Price level (e.g., '$', '$$')."},
                                                    "location": {
                                                        "type": "object",
                                                        "properties": {
                                                            "address1": {"type": "string"},
                                                            "address2": {"type": "string", "nullable": True},
                                                            "address3": {"type": "string", "nullable": True},
                                                            "city": {"type": "string"},
                                                            "zip_code": {"type": "string"},
                                                            "country": {"type": "string"},
                                                            "state": {"type": "string"},
                                                            "display_address": {"type": "array", "items": {"type": "string"}}
                                                        }
                                                    },
                                                    "phone": {"type": "string"},
                                                    "display_phone": {"type": "string"},
                                                    "distance": {"type": "number", "format": "float"}
                                                }
                                            }
                                        },
                                        "total": {"type": "integer"},
                                    }
                                }
                            }
                        }
                    },
                    "400": {"description": "Bad Request (e.g., invalid parameter)."},
                    "401": {"description": "Unauthorized (e.g., API key issue)."}
                }
            }
        }
    }
}
