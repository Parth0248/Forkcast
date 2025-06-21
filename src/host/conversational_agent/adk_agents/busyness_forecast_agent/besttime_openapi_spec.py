# BESTTIME_OPENAPI_SPEC = {
#     "openapi": "3.0.0",
#     "info": {
#         "title": "BestTime API - Foot Traffic Forecasts",
#         "version": "v1",
#         "description": "OpenAPI specification for the BestTime API's foot traffic forecast endpoints. Requires API Key authentication."
#     },
#     "servers": [
#         {
#             "url": "https://besttime.app"
#         }
#     ],
#     "components": {
#         "securitySchemes": {
#            "BearerAuth": {  # This is the name you'll reference
#                 "type": "http",
#                 "scheme": "bearer",
#                 "bearerFormat": "JWT", # Or "APIKey" - descriptive for the token type
#                 "description": "Yelp API Key. Provide as a Bearer token."
#             }
#         }
#     },
#     "security": [
#         {
#             "BearerAuth": []
#         }
#     ],
#     "paths": {
#         "/api/v1/forecasts": {
#             "post": {
#                 "summary": "Create new foot-traffic forecast",
#                 "operationId": "createFootTrafficForecast",
#                 "description": "Returns foot-traffic forecast for a venue based on name and address. Creates a forecast using the most recent available data.",
#                 "parameters": [
#                     {
#                         "name": "venue_name",
#                         "in": "query",
#                         "required": False,
#                         "schema": {
#                             "type": "string",
#                             "maxLength": 256
#                         },
#                         "description": "Name of the venue (public business). Required when venue_id is not provided."
#                     },
#                     {
#                         "name": "venue_address",
#                         "in": "query",
#                         "required": False,
#                         "schema": {
#                             "type": "string",
#                             "maxLength": 1024
#                         },
#                         "description": "Address of the venue. Required when venue_id is not provided. Does not have to be exact but needs to be precise enough for geocoding."
#                     },
#                     {
#                         "name": "venue_id",
#                         "in": "query",
#                         "required": False,
#                         "schema": {
#                             "type": "string"
#                         },
#                         "description": "Unique ID for the venue. Can be used instead of venue_name and venue_address."
#                     },
#                     {
#                         "name": "collection_id",
#                         "in": "query",
#                         "required": False,
#                         "schema": {
#                             "type": "string"
#                         },
#                         "description": "Add venue to an existing collection."
#                     }
#                 ],
#                 "responses": {
#                     "200": {
#                         "description": "Successful forecast creation. Returns detailed foot traffic analysis.",
#                         "content": {
#                             "application/json": {
#                                 "schema": {
#                                     "type": "object",
#                                     "properties": {
#                                         "analysis": {
#                                             "type": "array",
#                                             "description": "List with analysis object for each day of the week",
#                                             "items": {
#                                                 "type": "object",
#                                                 "properties": {
#                                                     "day_info": {
#                                                         "type": "object",
#                                                         "properties": {
#                                                             "day_int": {"type": "integer", "description": "Day integer 0 (Monday) to 6 (Sunday)"},
#                                                             "day_text": {"type": "string", "description": "Day name"},
#                                                             "day_rank_max": {"type": "integer", "description": "Day ranking based on maximum busyness"},
#                                                             "day_rank_mean": {"type": "integer", "description": "Day ranking based on mean busyness"},
#                                                             "venue_open_close_v2": {
#                                                                 "type": "object",
#                                                                 "properties": {
#                                                                     "24h": {"type": "array", "items": {"type": "object"}},
#                                                                     "12h": {"type": "array", "items": {"type": "string"}}
#                                                                 }
#                                                             }
#                                                         }
#                                                     },
#                                                     "day_raw": {"type": "array", "items": {"type": "integer"}, "description": "Raw busyness data for each hour"},
#                                                     "busy_hours": {"type": "array", "items": {"type": "integer"}, "description": "List of busy hours in 24h format"},
#                                                     "quiet_hours": {"type": "array", "items": {"type": "integer"}, "description": "List of quiet hours in 24h format"},
#                                                     "peak_hours": {
#                                                         "type": "array",
#                                                         "items": {
#                                                             "type": "object",
#                                                             "properties": {
#                                                                 "peak_start": {"type": "integer"},
#                                                                 "peak_max": {"type": "integer"},
#                                                                 "peak_end": {"type": "integer"},
#                                                                 "peak_intensity": {"type": "integer"}
#                                                             }
#                                                         }
#                                                     },
#                                                     "surge_hours": {
#                                                         "type": "object",
#                                                         "properties": {
#                                                             "most_people_come": {"type": "integer"},
#                                                             "most_people_leave": {"type": "integer"}
#                                                         }
#                                                     }
#                                                 }
#                                             }
#                                         },
#                                         "epoch_analysis": {"type": "string", "description": "Timestamp when forecast was made"},
#                                         "status": {"type": "string", "description": "Status of the response"},
#                                         "venue_info": {
#                                             "type": "object",
#                                             "properties": {
#                                                 "venue_id": {"type": "string", "description": "Unique BestTime venue ID"},
#                                                 "venue_name": {"type": "string", "description": "Name of the venue"},
#                                                 "venue_address": {"type": "string", "description": "Address of the venue"},
#                                                 "venue_timezone": {"type": "string", "description": "Timezone of the venue"},
#                                                 "venue_type": {"type": "string", "description": "Type of venue"},
#                                                 "venue_types": {"type": "array", "items": {"type": "string"}},
#                                                 "venue_dwell_time_min": {"type": "integer"},
#                                                 "venue_dwell_time_max": {"type": "integer"},
#                                                 "venue_dwell_time_avg": {"type": "integer"},
#                                                 "venue_lat": {"type": "number"},
#                                                 "venue_lon": {"type": "number"}
#                                             }
#                                         }
#                                     }
#                                 }
#                             }
#                         }
#                     },
#                     "400": {"description": "Bad Request (e.g., invalid parameter)"},
#                     "401": {"description": "Unauthorized (e.g., API key issue)"}
#                 }
#             }
#         },
#         "/api/v1/forecasts/live": {
#             "post": {
#                 "summary": "Get live foot-traffic data",
#                 "operationId": "getLiveFootTrafficData",
#                 "description": "Returns live foot-traffic data for a venue based on venue name and address or venue_id. Provides current busyness compared to forecasted levels.",
#                 "parameters": [
#                     {
#                         "name": "venue_id",
#                         "in": "query",
#                         "required": False,
#                         "schema": {
#                             "type": "string"
#                         },
#                         "description": "Unique ID for the venue. Recommended for faster responses. Required when venue_name and venue_address are not provided."
#                     },
#                     {
#                         "name": "venue_name",
#                         "in": "query",
#                         "required": False,
#                         "schema": {
#                             "type": "string",
#                             "maxLength": 256
#                         },
#                         "description": "Name of the venue (public business). Required when venue_id is not provided."
#                     },
#                     {
#                         "name": "venue_address",
#                         "in": "query",
#                         "required": False,
#                         "schema": {
#                             "type": "string",
#                             "maxLength": 1024
#                         },
#                         "description": "Address of the venue. Required when venue_id is not provided."
#                     }
#                 ],
#                 "responses": {
#                     "200": {
#                         "description": "Successful live data retrieval. Returns current busyness information.",
#                         "content": {
#                             "application/json": {
#                                 "schema": {
#                                     "type": "object",
#                                     "properties": {
#                                         "analysis": {
#                                             "type": "object",
#                                             "properties": {
#                                                 "venue_forecasted_busyness": {"type": "integer", "description": "Forecasted busyness for this hour (0-100)"},
#                                                 "venue_live_busyness": {"type": "integer", "description": "Live busyness at the venue currently"},
#                                                 "venue_live_busyness_available": {"type": "boolean", "description": "Whether live data is available"},
#                                                 "venue_forecast_busyness_available": {"type": "boolean", "description": "Whether forecast data is available"},
#                                                 "venue_live_forecasted_delta": {"type": "integer", "description": "Difference between live and forecasted busyness"}
#                                             }
#                                         },
#                                         "status": {"type": "string", "description": "Status of the response"},
#                                         "venue_info": {
#                                             "type": "object",
#                                             "properties": {
#                                                 "venue_id": {"type": "string", "description": "Unique BestTime venue ID"},
#                                                 "venue_name": {"type": "string", "description": "Name of the venue"},
#                                                 "venue_current_gmttime": {"type": "string", "description": "Current GMT time at venue"},
#                                                 "venue_current_localtime": {"type": "string", "description": "Current local time at venue"},
#                                                 "venue_timezone": {"type": "string", "description": "Timezone of the venue"},
#                                                 "venue_dwell_time_min": {"type": "integer"},
#                                                 "venue_dwell_time_max": {"type": "integer"},
#                                                 "venue_dwell_time_avg": {"type": "integer"}
#                                             }
#                                         }
#                                     }
#                                 }
#                             }
#                         }
#                     },
#                     "400": {"description": "Bad Request (e.g., invalid parameter)"},
#                     "401": {"description": "Unauthorized (e.g., API key issue)"}
#                 }
#             }
#         }
#     }
# }

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
           "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "APIKey",
                "description": "BestTime API Key. Provide as a Bearer token. Get your key from besttime.app"
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
                "description": "Returns foot-traffic forecast for a venue based on name and address. Creates a forecast using the most recent available data. Note: Not all venues have sufficient data for forecasting.",
                "parameters": [
                    {
                        "name": "venue_name",
                        "in": "query", 
                        "required": False,
                        "schema": {
                            "type": "string",
                            "maxLength": 256
                        },
                        "description": "Name of the venue (public business). Required when venue_id is not provided. Use exact business name for best results."
                    },
                    {
                        "name": "venue_address",
                        "in": "query",
                        "required": False, 
                        "schema": {
                            "type": "string",
                            "maxLength": 1024
                        },
                        "description": "Address of the venue. Required when venue_id is not provided. Include city and state for better matching. Does not have to be exact but needs to be precise enough for geocoding."
                    },
                    {
                        "name": "venue_id",
                        "in": "query",
                        "required": False,
                        "schema": {
                            "type": "string"
                        },
                        "description": "Unique BestTime venue ID. Can be used instead of venue_name and venue_address for faster, more accurate results."
                    },
                    {
                        "name": "collection_id",
                        "in": "query",
                        "required": False,
                        "schema": {
                            "type": "string"
                        },
                        "description": "Add venue to an existing collection for organization."
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful forecast creation. Returns detailed foot traffic analysis for the venue.",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "analysis": {
                                            "type": "array",
                                            "description": "List with analysis object for each day of the week (Monday=0 to Sunday=6)",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    "day_info": {
                                                        "type": "object",
                                                        "properties": {
                                                            "day_int": {"type": "integer", "description": "Day integer 0 (Monday) to 6 (Sunday)"},
                                                            "day_text": {"type": "string", "description": "Day name (Monday, Tuesday, etc.)"},
                                                            "day_rank_max": {"type": "integer", "description": "Day ranking based on maximum busyness (1=busiest, 7=quietest)"},
                                                            "day_rank_mean": {"type": "integer", "description": "Day ranking based on mean busyness"},
                                                            "venue_open_close_v2": {
                                                                "type": "object",
                                                                "description": "Opening hours information",
                                                                "properties": {
                                                                    "24h": {"type": "array", "items": {"type": "object"}},
                                                                    "12h": {"type": "array", "items": {"type": "string"}}
                                                                }
                                                            }
                                                        }
                                                    },
                                                    "day_raw": {
                                                        "type": "array", 
                                                        "items": {"type": "integer"}, 
                                                        "description": "Raw busyness data for each hour (0-23), values 0-100"
                                                    },
                                                    "busy_hours": {
                                                        "type": "array", 
                                                        "items": {"type": "integer"}, 
                                                        "description": "List of busy hours in 24h format (e.g., [12, 13, 18, 19])"
                                                    },
                                                    "quiet_hours": {
                                                        "type": "array", 
                                                        "items": {"type": "integer"}, 
                                                        "description": "List of quiet hours in 24h format (e.g., [3, 4, 15, 16])"
                                                    },
                                                    "peak_hours": {
                                                        "type": "array",
                                                        "description": "Peak period information with intensity",
                                                        "items": {
                                                            "type": "object",
                                                            "properties": {
                                                                "peak_start": {"type": "integer", "description": "Peak start hour (24h format)"},
                                                                "peak_max": {"type": "integer", "description": "Hour of maximum crowd"},
                                                                "peak_end": {"type": "integer", "description": "Peak end hour (24h format)"},
                                                                "peak_intensity": {"type": "integer", "description": "Intensity level 0-100"}
                                                            }
                                                        }
                                                    },
                                                    "surge_hours": {
                                                        "type": "object",
                                                        "description": "Times when most people arrive/leave",
                                                        "properties": {
                                                            "most_people_come": {"type": "integer", "description": "Hour when most people arrive"},
                                                            "most_people_leave": {"type": "integer", "description": "Hour when most people leave"}
                                                        }
                                                    }
                                                }
                                            }
                                        },
                                        "epoch_analysis": {"type": "string", "description": "Timestamp when forecast was generated"},
                                        "status": {"type": "string", "description": "Status of the response (OK, Error, etc.)"},
                                        "venue_info": {
                                            "type": "object",
                                            "description": "Venue details and metadata",
                                            "properties": {
                                                "venue_id": {"type": "string", "description": "Unique BestTime venue ID for future calls"},
                                                "venue_name": {"type": "string", "description": "Confirmed venue name"},
                                                "venue_address": {"type": "string", "description": "Confirmed venue address"},
                                                "venue_timezone": {"type": "string", "description": "Timezone of the venue (e.g., America/Los_Angeles)"},
                                                "venue_type": {"type": "string", "description": "Type of venue (restaurant, cafe, etc.)"},
                                                "venue_types": {"type": "array", "items": {"type": "string"}, "description": "Array of venue categories"},
                                                "venue_dwell_time_min": {"type": "integer", "description": "Minimum typical visit duration (minutes)"},
                                                "venue_dwell_time_max": {"type": "integer", "description": "Maximum typical visit duration (minutes)"},
                                                "venue_dwell_time_avg": {"type": "integer", "description": "Average visit duration (minutes)"},
                                                "venue_lat": {"type": "number", "description": "Latitude coordinate"},
                                                "venue_lon": {"type": "number", "description": "Longitude coordinate"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "400": {"description": "Bad Request - Invalid parameters or venue not found"},
                    "401": {"description": "Unauthorized - Invalid or missing API key"},
                    "429": {"description": "Too Many Requests - Rate limit exceeded"},
                    "500": {"description": "Internal Server Error"}
                }
            }
        },
        "/api/v1/forecasts/live": {
            "post": {
                "summary": "Get live foot-traffic data",
                "operationId": "getLiveFootTrafficData",
                "description": "Returns live foot-traffic data for a venue. Provides current busyness compared to forecasted levels. Live data may not be available for all venues.",
                "parameters": [
                    {
                        "name": "venue_id",
                        "in": "query",
                        "required": False,
                        "schema": {
                            "type": "string"
                        },
                        "description": "Unique BestTime venue ID. Recommended for faster responses. Required when venue_name and venue_address are not provided."
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
                                            "description": "Live busyness analysis data",
                                            "properties": {
                                                "venue_forecasted_busyness": {"type": "integer", "description": "Forecasted busyness for this hour (0-100)"},
                                                "venue_live_busyness": {"type": "integer", "description": "Current live busyness at the venue (0-100)"},
                                                "venue_live_busyness_available": {"type": "boolean", "description": "Whether live data is currently available"},
                                                "venue_forecast_busyness_available": {"type": "boolean", "description": "Whether forecast data is available"},
                                                "venue_live_forecasted_delta": {"type": "integer", "description": "Difference between live and forecasted busyness (-100 to +100)"}
                                            }
                                        },
                                        "status": {"type": "string", "description": "Status of the response"},
                                        "venue_info": {
                                            "type": "object",
                                            "description": "Venue information and timing data",
                                            "properties": {
                                                "venue_id": {"type": "string", "description": "Unique BestTime venue ID"},
                                                "venue_name": {"type": "string", "description": "Venue name"},
                                                "venue_current_gmttime": {"type": "string", "description": "Current GMT time at venue"},
                                                "venue_current_localtime": {"type": "string", "description": "Current local time at venue"},
                                                "venue_timezone": {"type": "string", "description": "Timezone of the venue"},
                                                "venue_dwell_time_min": {"type": "integer", "description": "Minimum visit duration (minutes)"},
                                                "venue_dwell_time_max": {"type": "integer", "description": "Maximum visit duration (minutes)"},
                                                "venue_dwell_time_avg": {"type": "integer", "description": "Average visit duration (minutes)"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "400": {"description": "Bad Request - Invalid parameters or venue not found"},
                    "401": {"description": "Unauthorized - Invalid or missing API key"},
                    "429": {"description": "Too Many Requests - Rate limit exceeded"},
                    "500": {"description": "Internal Server Error"}
                }
            }
        }
    }
}