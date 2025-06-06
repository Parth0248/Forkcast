BESTTIME_OPENAPI_SPEC = {
    "openapi": "3.0.0",
    "info": {
        "title": "BestTime API - Foot Traffic Forecasts",
        "version": "v1",
        "description": "OpenAPI specification for the BestTime API's foot traffic forecast endpoints. Requires API Key authentication."
    },
    "servers": [
        {
            "url": "https://besttime.app"
        }
    ],
    "components": {
        "securitySchemes": {
           "BearerAuth": {  # This is the name you'll reference
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT", # Or "APIKey" - descriptive for the token type
                "description": "Yelp API Key. Provide as a Bearer token."
            }
        }
    },
    "security": [
        {
            "BearerAuth": []
        }
    ],
    "paths": {
        "/api/v1/forecasts": {
            "post": {
                "summary": "Create new foot-traffic forecast",
                "operationId": "createFootTrafficForecast",
                "description": "Returns foot-traffic forecast for a venue based on name and address. Creates a forecast using the most recent available data.",
                "parameters": [
                    {
                        "name": "venue_name",
                        "in": "query",
                        "required": False,
                        "schema": {
                            "type": "string",
                            "maxLength": 256
                        },
                        "description": "Name of the venue (public business). Required when venue_id is not provided."
                    },
                    {
                        "name": "venue_address",
                        "in": "query",
                        "required": False,
                        "schema": {
                            "type": "string",
                            "maxLength": 1024
                        },
                        "description": "Address of the venue. Required when venue_id is not provided. Does not have to be exact but needs to be precise enough for geocoding."
                    },
                    {
                        "name": "venue_id",
                        "in": "query",
                        "required": False,
                        "schema": {
                            "type": "string"
                        },
                        "description": "Unique ID for the venue. Can be used instead of venue_name and venue_address."
                    },
                    {
                        "name": "collection_id",
                        "in": "query",
                        "required": False,
                        "schema": {
                            "type": "string"
                        },
                        "description": "Add venue to an existing collection."
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful forecast creation. Returns detailed foot traffic analysis.",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "analysis": {
                                            "type": "array",
                                            "description": "List with analysis object for each day of the week",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    "day_info": {
                                                        "type": "object",
                                                        "properties": {
                                                            "day_int": {"type": "integer", "description": "Day integer 0 (Monday) to 6 (Sunday)"},
                                                            "day_text": {"type": "string", "description": "Day name"},
                                                            "day_rank_max": {"type": "integer", "description": "Day ranking based on maximum busyness"},
                                                            "day_rank_mean": {"type": "integer", "description": "Day ranking based on mean busyness"},
                                                            "venue_open_close_v2": {
                                                                "type": "object",
                                                                "properties": {
                                                                    "24h": {"type": "array", "items": {"type": "object"}},
                                                                    "12h": {"type": "array", "items": {"type": "string"}}
                                                                }
                                                            }
                                                        }
                                                    },
                                                    "day_raw": {"type": "array", "items": {"type": "integer"}, "description": "Raw busyness data for each hour"},
                                                    "busy_hours": {"type": "array", "items": {"type": "integer"}, "description": "List of busy hours in 24h format"},
                                                    "quiet_hours": {"type": "array", "items": {"type": "integer"}, "description": "List of quiet hours in 24h format"},
                                                    "peak_hours": {
                                                        "type": "array",
                                                        "items": {
                                                            "type": "object",
                                                            "properties": {
                                                                "peak_start": {"type": "integer"},
                                                                "peak_max": {"type": "integer"},
                                                                "peak_end": {"type": "integer"},
                                                                "peak_intensity": {"type": "integer"}
                                                            }
                                                        }
                                                    },
                                                    "surge_hours": {
                                                        "type": "object",
                                                        "properties": {
                                                            "most_people_come": {"type": "integer"},
                                                            "most_people_leave": {"type": "integer"}
                                                        }
                                                    }
                                                }
                                            }
                                        },
                                        "epoch_analysis": {"type": "string", "description": "Timestamp when forecast was made"},
                                        "status": {"type": "string", "description": "Status of the response"},
                                        "venue_info": {
                                            "type": "object",
                                            "properties": {
                                                "venue_id": {"type": "string", "description": "Unique BestTime venue ID"},
                                                "venue_name": {"type": "string", "description": "Name of the venue"},
                                                "venue_address": {"type": "string", "description": "Address of the venue"},
                                                "venue_timezone": {"type": "string", "description": "Timezone of the venue"},
                                                "venue_type": {"type": "string", "description": "Type of venue"},
                                                "venue_types": {"type": "array", "items": {"type": "string"}},
                                                "venue_dwell_time_min": {"type": "integer"},
                                                "venue_dwell_time_max": {"type": "integer"},
                                                "venue_dwell_time_avg": {"type": "integer"},
                                                "venue_lat": {"type": "number"},
                                                "venue_lon": {"type": "number"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "400": {"description": "Bad Request (e.g., invalid parameter)"},
                    "401": {"description": "Unauthorized (e.g., API key issue)"}
                }
            }
        },
        "/api/v1/forecasts/live": {
            "post": {
                "summary": "Get live foot-traffic data",
                "operationId": "getLiveFootTrafficData",
                "description": "Returns live foot-traffic data for a venue based on venue name and address or venue_id. Provides current busyness compared to forecasted levels.",
                "parameters": [
                    {
                        "name": "venue_id",
                        "in": "query",
                        "required": False,
                        "schema": {
                            "type": "string"
                        },
                        "description": "Unique ID for the venue. Recommended for faster responses. Required when venue_name and venue_address are not provided."
                    },
                    {
                        "name": "venue_name",
                        "in": "query",
                        "required": False,
                        "schema": {
                            "type": "string",
                            "maxLength": 256
                        },
                        "description": "Name of the venue (public business). Required when venue_id is not provided."
                    },
                    {
                        "name": "venue_address",
                        "in": "query",
                        "required": False,
                        "schema": {
                            "type": "string",
                            "maxLength": 1024
                        },
                        "description": "Address of the venue. Required when venue_id is not provided."
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful live data retrieval. Returns current busyness information.",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "analysis": {
                                            "type": "object",
                                            "properties": {
                                                "venue_forecasted_busyness": {"type": "integer", "description": "Forecasted busyness for this hour (0-100)"},
                                                "venue_live_busyness": {"type": "integer", "description": "Live busyness at the venue currently"},
                                                "venue_live_busyness_available": {"type": "boolean", "description": "Whether live data is available"},
                                                "venue_forecast_busyness_available": {"type": "boolean", "description": "Whether forecast data is available"},
                                                "venue_live_forecasted_delta": {"type": "integer", "description": "Difference between live and forecasted busyness"}
                                            }
                                        },
                                        "status": {"type": "string", "description": "Status of the response"},
                                        "venue_info": {
                                            "type": "object",
                                            "properties": {
                                                "venue_id": {"type": "string", "description": "Unique BestTime venue ID"},
                                                "venue_name": {"type": "string", "description": "Name of the venue"},
                                                "venue_current_gmttime": {"type": "string", "description": "Current GMT time at venue"},
                                                "venue_current_localtime": {"type": "string", "description": "Current local time at venue"},
                                                "venue_timezone": {"type": "string", "description": "Timezone of the venue"},
                                                "venue_dwell_time_min": {"type": "integer"},
                                                "venue_dwell_time_max": {"type": "integer"},
                                                "venue_dwell_time_avg": {"type": "integer"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "400": {"description": "Bad Request (e.g., invalid parameter)"},
                    "401": {"description": "Unauthorized (e.g., API key issue)"}
                }
            }
        }
    }
}