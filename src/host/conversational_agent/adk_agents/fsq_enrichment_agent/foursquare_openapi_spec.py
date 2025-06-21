# Assume FOURSQUARE_API_KEY is available in your environment for ADK to use
# from config.settings import FOURSQUARE_API_KEY

FOURSQUARE_OPENAPI_SPEC = {
    "openapi": "3.0.0",
    "info": {
        "title": "Foursquare API - Place Search (Detailed Output)",
        "version": "v3",
        "description": "OpenAPI specification for Foursquare API's /v3/places/search endpoint, returning a detailed structure for each place. Uses API Key in Authorization header."
    },
    "servers": [
        {
            "url": "https://api.foursquare.com"
        }
    ],
    "components": {
        "securitySchemes": {
            "FoursquareApiKeyAuth": {
                "type": "apiKey",
                "in": "header",
                "name": "Authorization",
                "description": "Foursquare API Key. The ADK OpenAPIToolset will use this scheme to manage the API key."
            }
        }
    },
    "security": [
        {
            "FoursquareApiKeyAuth": []
        }
    ],
    "paths": {
        "/v3/places/search": {
            "get": {
                "summary": "Search for a specific place on Foursquare to get its details.",
                "operationId": "searchFoursquarePlaceDetails",
                "description": "Searches for businesses on Foursquare. Intended to find a specific place using its name and location (address or lat/lon) and retrieve a comprehensive set of fields.",
                "parameters": [
                    {
                        "name": "query",
                        "in": "query",
                        "required": False,
                        "description": "The name of the venue or a general search term.",
                        "schema": {"type": "string"}
                    },
                    {
                        "name": "near",
                        "in": "query",
                        "required": False,
                        "description": "The general area or address for the search. Used if 'll' is not provided.",
                        "schema": {"type": "string"}
                    },
                    {
                        "name": "ll",
                        "in": "query",
                        "required": False,
                        "description": "Latitude and longitude, comma-separated (e.g., '34.0522,-118.2437').",
                        "schema": {"type": "string"}
                    },
                    {
                        "name": "limit",
                        "in": "query",
                        "required": False,
                        "description": "Number of results. For an exact match, use 1 or a small number.",
                        "schema": {"type": "integer", "default": 1, "minimum": 1}
                    },
                    {
                        "name": "fields",
                        "in": "query",
                        "required": False, # Make it optional; Foursquare returns a default set if not specified
                        "description": "Comma-separated list of Foursquare fields to return (e.g., fsq_id,name,location,categories,features,attributes,hours,menu,photos,price,rating,stats,tips,tastes,website,social_media,hours_popular,description,email,fax,closed_bucket,date_closed,distance,geocodes,link,popularity,related_places,store_id,timezone,verified,venue_reality_bucket).",
                        "schema": {"type": "string"}
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful search. Returns an object containing a list of 'results' (places).",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "results": {
                                            "type": "array",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    "fsq_id": {"type": "string", "nullable": True},
                                                    "categories": {
                                                        "type": "array",
                                                        "nullable": True,
                                                        "items": {
                                                            "type": "object",
                                                            "properties": {
                                                                "id": {"type": "integer", "nullable": True},
                                                                "name": {"type": "string", "nullable": True},
                                                                "short_name": {"type": "string", "nullable": True},
                                                                "plural_name": {"type": "string", "nullable": True},
                                                                "icon": {
                                                                    "type": "object",
                                                                    "nullable": True,
                                                                    "properties": {
                                                                        "id": {"type": "string", "nullable": True},
                                                                        "created_at": {"type": "string", "format": "date-time", "nullable": True},
                                                                        "prefix": {"type": "string", "nullable": True},
                                                                        "suffix": {"type": "string", "nullable": True},
                                                                        "width": {"type": "integer", "nullable": True},
                                                                        "height": {"type": "integer", "nullable": True},
                                                                        "classifications": {"type": "array", "items": {"type": "string"}, "nullable": True},
                                                                        "tip": {
                                                                            "type": "object",
                                                                            "nullable": True,
                                                                            "properties": {
                                                                                "id": {"type": "string", "nullable": True},
                                                                                "created_at": {"type": "string", "format": "date-time", "nullable": True},
                                                                                "text": {"type": "string", "nullable": True},
                                                                                "url": {"type": "string", "format": "url", "nullable": True},
                                                                                "lang": {"type": "string", "nullable": True},
                                                                                "agree_count": {"type": "integer", "nullable": True},
                                                                                "disagree_count": {"type": "integer", "nullable": True}
                                                                            }
                                                                        }
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    },
                                                    "chains": {
                                                        "type": "array",
                                                        "nullable": True,
                                                        "items": {
                                                            "type": "object",
                                                            "properties": {
                                                                "id": {"type": "string", "nullable": True},
                                                                "name": {"type": "string", "nullable": True}
                                                            }
                                                        }
                                                    },
                                                    "closed_bucket": {"type": "string", "nullable": True},
                                                    "date_closed": {"type": "string", "format": "date", "nullable": True},
                                                    "description": {"type": "string", "nullable": True},
                                                    "distance": {"type": "number", "format": "float", "nullable": True},
                                                    "email": {"type": "string", "format": "email", "nullable": True},
                                                    "fax": {"type": "string", "nullable": True},
                                                    "features": {
                                                        "type": "object",
                                                        "nullable": True,
                                                        "properties": {
                                                            "payment": {
                                                                "type": "object", "nullable": True, "additionalProperties": True,
                                                                "properties": { "credit_cards": {"type": "object", "nullable": True, "additionalProperties": True}, "digital_wallet": {"type": "object", "nullable": True, "additionalProperties": True}}
                                                            },
                                                            "food_and_drink": {
                                                                "type": "object", "nullable": True, "additionalProperties": True,
                                                                "properties": { "alcohol": {"type": "object", "nullable": True, "additionalProperties": True}, "meals": {"type": "object", "nullable": True, "additionalProperties": True}}
                                                            },
                                                            "services": {
                                                                "type": "object", "nullable": True, "additionalProperties": True,
                                                                "properties": { "delivery": {"type": "object", "nullable": True}, "takeout": {"type": "object", "nullable": True}, "drive_through": {"type": "object", "nullable": True}, "dine_in": {"type": "object", "nullable": True, "additionalProperties": True}}
                                                            },
                                                            "amenities": {
                                                                "type": "object", "nullable": True, "additionalProperties": True,
                                                                "properties": { "restroom": {"type": "object", "nullable": True}, "smoking": {"type": "object", "nullable": True}, "jukebox": {"type": "object", "nullable": True}, "music": {"type": "object", "nullable": True}, "live_music": {"type": "object", "nullable": True}, "private_room": {"type": "object", "nullable": True}, "outdoor_seating": {"type": "object", "nullable": True}, "tvs": {"type": "object", "nullable": True}, "atm": {"type": "object", "nullable": True}, "coat_check": {"type": "object", "nullable": True}, "wheelchair_accessible": {"type": "object", "nullable": True}, "parking": {"type": "object", "nullable": True, "additionalProperties": True}, "sit_down_dining": {"type": "object", "nullable": True}, "wifi": {"type": "string", "nullable": True} }
                                                            }
                                                        }
                                                    },
                                                    "attributes": {
                                                        "type": "object",
                                                        "nullable": True,
                                                        "additionalProperties": {"type": "string", "nullable": True},
                                                        "description": "Key-value pairs of attributes; values are typically strings indicating yes/no/level or specific details."
                                                    },
                                                    "geocodes": {
                                                        "type": "object",
                                                        "nullable": True,
                                                        "properties": {
                                                            "drop_off": {"type": "object", "nullable": True, "properties": {"latitude": {"type": "number"}, "longitude": {"type": "number"}}},
                                                            "front_door": {"type": "object", "nullable": True, "properties": {"latitude": {"type": "number"}, "longitude": {"type": "number"}}},
                                                            "main": {"type": "object", "nullable": True, "properties": {"latitude": {"type": "number"}, "longitude": {"type": "number"}}},
                                                            "road": {"type": "object", "nullable": True, "properties": {"latitude": {"type": "number"}, "longitude": {"type": "number"}}},
                                                            "roof": {"type": "object", "nullable": True, "properties": {"latitude": {"type": "number"}, "longitude": {"type": "number"}}}
                                                        }
                                                    },
                                                    "hours": {
                                                        "type": "object",
                                                        "nullable": True,
                                                        "properties": {
                                                            "display": {"type": "string", "nullable": True},
                                                            "is_local_holiday": {"type": "boolean", "nullable": True},
                                                            "open_now": {"type": "boolean", "nullable": True},
                                                            "regular": {
                                                                "type": "array", "nullable": True,
                                                                "items": {"type": "object", "properties": {"close": {"type": "string"}, "day": {"type": "integer"}, "open": {"type": "string"}}}
                                                            }
                                                        }
                                                    },
                                                    "hours_popular": {
                                                        "type": "array", "nullable": True,
                                                        "items": {"type": "object", "properties": {"close": {"type": "string"}, "day": {"type": "integer"}, "open": {"type": "string"}}}
                                                    },
                                                    "link": {"type": "string", "format": "url", "nullable": True},
                                                    "location": {
                                                        "type": "object",
                                                        "nullable": True,
                                                        "properties": {
                                                            "address": {"type": "string", "nullable": True},
                                                            "address_extended": {"type": "string", "nullable": True},
                                                            "admin_region": {"type": "string", "nullable": True},
                                                            "census_block": {"type": "string", "nullable": True},
                                                            "country": {"type": "string", "nullable": True},
                                                            "cross_street": {"type": "string", "nullable": True},
                                                            "dma": {"type": "string", "nullable": True},
                                                            "formatted_address": {"type": "string", "nullable": True},
                                                            "locality": {"type": "string", "nullable": True},
                                                            "neighborhood": {"type": "array", "items": {"type": "string"}, "nullable": True},
                                                            "po_box": {"type": "string", "nullable": True},
                                                            "post_town": {"type": "string", "nullable": True},
                                                            "postcode": {"type": "string", "nullable": True},
                                                            "region": {"type": "string", "nullable": True}
                                                        }
                                                    },
                                                    "menu": {"type": "string", "format": "url", "nullable": True},
                                                    "name": {"type": "string", "nullable": True},
                                                    "photos": {
                                                        "type": "array", "nullable": True,
                                                        "items": {
                                                            "type": "object",
                                                            "properties": {
                                                                "id": {"type": "string", "nullable": True},
                                                                "created_at": {"type": "string", "format": "date-time", "nullable": True},
                                                                "prefix": {"type": "string", "nullable": True},
                                                                "suffix": {"type": "string", "nullable": True},
                                                                "width": {"type": "integer", "nullable": True},
                                                                "height": {"type": "integer", "nullable": True},
                                                                "classifications": {"type": "array", "items": {"type": "string"}, "nullable": True},
                                                                "tip": {
                                                                    "type": "object", "nullable": True,
                                                                }
                                                            }
                                                        }
                                                    },
                                                    "popularity": {"type": "number", "format": "float", "nullable": True},
                                                    "price": {"type": "integer", "nullable": True, "description": "Price tier (1-4)."},
                                                    "rating": {"type": "number", "format": "float", "nullable": True, "description": "Rating, usually 0-10 scale."},
                                                    "related_places": {"type": "object", "nullable": True, "additionalProperties": True},
                                                    "social_media": {
                                                        "type": "object", "nullable": True,
                                                        "properties": {
                                                            "facebook_id": {"type": "string", "nullable": True},
                                                            "instagram": {"type": "string", "nullable": True},
                                                            "twitter": {"type": "string", "nullable": True}
                                                        }
                                                    },
                                                    "stats": {
                                                        "type": "object", "nullable": True,
                                                        "properties": {
                                                            "total_photos": {"type": "integer", "nullable": True},
                                                            "total_ratings": {"type": "integer", "nullable": True},
                                                            "total_tips": {"type": "integer", "nullable": True}
                                                        }
                                                    },
                                                    "store_id": {"type": "string", "nullable": True},
                                                    "tastes": {"type": "array", "items": {"type": "string"}, "nullable": True},
                                                    "tel": {"type": "string", "nullable": True},
                                                    "timezone": {"type": "string", "nullable": True},
                                                    "tips": {
                                                        "type": "array", "nullable": True,
                                                        "items": {
                                                            "type": "object",
                                                            "properties": {
                                                                "id": {"type": "string", "nullable": True},
                                                                "created_at": {"type": "string", "format": "date-time", "nullable": True},
                                                                "text": {"type": "string", "nullable": True},
                                                                "url": {"type": "string", "format": "url", "nullable": True},
                                                                "lang": {"type": "string", "nullable": True},
                                                                "agree_count": {"type": "integer", "nullable": True},
                                                                "disagree_count": {"type": "integer", "nullable": True}
                                                            }
                                                        }
                                                    },
                                                    "venue_reality_bucket": {"type": "string", "nullable": True},
                                                    "verified": {"type": "boolean", "nullable": True},
                                                    "website": {"type": "string", "format": "url", "nullable": True}
                                                }
                                            }
                                        },
                                        "context": {
                                            "type": "object",
                                            "nullable": True,
                                            "properties": {
                                                "geo_bounds": {
                                                    "type": "object", "nullable": True,
                                                    "properties": {
                                                        "circle": {
                                                            "type": "object", "nullable": True,
                                                            "properties": {
                                                                "center": {"type": "object", "properties": {"latitude": {"type": "number"}, "longitude": {"type": "number"}}},
                                                                "radius": {"type": "integer"}
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "400": {"description": "Bad Request"},
                    "401": {"description": "Unauthorized - API key issue"}
                }
            }
        }
    }
}