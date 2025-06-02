# import json
# from google.adk.tools.tool_context import ToolContext # Make sure this import path is correct for your ADK version

# # The function name will be the tool name.
# # The docstring will be the tool description.
# # Parameter names and type hints will define the schema for the LLM.
# def update_session_query_details(tool_context: ToolContext, query_details_json: str) -> str:
#     """Saves the complete query_details JSON string to the current session state. Input must be a valid JSON string representing query_details.
    
#     Args: tool_context: The context of the tool invocation, which includes the session state.
#     query_details_json: A JSON string containing the complete query_details to be saved.
    
#     Returns:
#         A message indicating success or failure.
#     """
#     try:
#         query_details_data = json.loads(query_details_json)
#         # Use 'tool_context' consistently
#         if tool_context.state and "query_details" in tool_context.state:
#             tool_context.state["query_details"] = query_details_data
#             return "Successfully updated session with query_details."
#         else:
#             return "Error: Session context not found, cannot update query_details."
#     except json.JSONDecodeError as e:
#         return f"Error: Invalid JSON provided for query_details. Details: {str(e)}"
#     except Exception as e:
#         return f"Error updating session with query_details: {str(e)}"


# import json
# import logging
# from google.adk.tools.tool_context import ToolContext

# logger = logging.getLogger(__name__)

# def update_session_query_details(tool_context: ToolContext, query_details_json: str) -> str:
#     """Saves the complete query_details JSON string to the current session state.
    
#     Args:
#         tool_context: The context of the tool invocation, which includes the session state.
#         query_details_json: A JSON string containing the complete query_details to be saved.
    
#     Returns:
#         A message indicating success or failure.
#     """
    
#     try:
#         # Parse and validate JSON
#         query_details_data = json.loads(query_details_json)
#         logger.info(f"Parsed query_details JSON successfully. Status: {query_details_data.get('status', 'UNKNOWN')}")
        
#         # FIXED: Initialize state if it doesn't exist
#         if tool_context.state is None:
#             tool_context.state = {}
#             logger.info("Initialized empty session state")
        
#         # Save to session state
#         tool_context.state["query_details"] = query_details_data
        
#         # Log key information for debugging
#         status = query_details_data.get('status', 'UNKNOWN')
#         iteration = query_details_data.get('processing_flags', {}).get('iteration_count', 0)
#         missing_fields = query_details_data.get('processing_flags', {}).get('missing_critical_fields', [])
        
#         logger.info(f"Successfully updated session state - Status: {status}, Iteration: {iteration}, Missing: {missing_fields}")
        
#         return f"Successfully updated session with query_details. Status: {status}, Iteration: {iteration}"
        
#     except json.JSONDecodeError as e:
#         error_msg = f"Invalid JSON provided for query_details: {str(e)}"
#         logger.error(error_msg)
#         return f"Error: {error_msg}"
#     except Exception as e:
#         error_msg = f"Error updating session with query_details: {str(e)}"
#         logger.error(error_msg)
#         return f"Error: {error_msg}"
    
    

import json
import logging
from google.adk.tools.tool_context import ToolContext
from google.adk.events import Event, EventActions
from google.genai.types import Content, Part
import time

logger = logging.getLogger(__name__)

def update_session_query_details(tool_context: ToolContext, query_details_json: str) -> str:
    """Saves the complete query_details JSON string to the current session state using proper ADK protocol.
    
    Args:
        tool_context: The context of the tool invocation, which includes the session state.
        query_details_json: A JSON string containing the complete query_details to be saved.
    
    Returns:
        A message indicating success or failure.
    """
    
    try:
        # Parse and validate JSON
        query_details_data = json.loads(query_details_json)
        logger.info(f"Parsed query_details JSON successfully. Status: {query_details_data.get('status', 'UNKNOWN')}")
        
        # Prepare state delta for proper ADK state update
        state_delta = {
            "query_details": query_details_data
        }
        
        # Create EventActions with state_delta
        actions = EventActions(state_delta=state_delta)
        
        # Create an event to record this state update
        update_event = Event(
            invocation_id=f"update_query_details_{int(time.time())}",
            author="update_session_query_details_tool",
            actions=actions,
            timestamp=time.time(),
            content=Content(parts=[Part.from_text(
                f"Updated query_details with status: {query_details_data.get('status', 'UNKNOWN')}"
            )])
        )
        
        # Use the proper ADK method to update state through session service
        # The session should be available through tool_context
        if hasattr(tool_context, 'session') and tool_context.session:
            # Access the session service through the runner/context
            # This assumes the session service is accessible through the tool context
            if hasattr(tool_context, 'session_service'):
                tool_context.session_service.append_event(tool_context.session, update_event)
            else:
                # Fallback: If session_service is not directly accessible, 
                # we need to add the event through the proper channel
                # This might require accessing the runner or session service differently
                logger.warning("Session service not directly accessible through tool_context")
                
                # For now, we'll use the direct state modification as a fallback
                # but log that this should be improved
                if tool_context.state is None:
                    tool_context.state = {}
                tool_context.state.update(state_delta)
                logger.warning("Using direct state modification as fallback - should be improved")
        else:
            # Fallback to direct state modification if session is not available
            logger.warning("Session not available through tool_context, using direct state modification")
            if tool_context.state is None:
                tool_context.state = {}
            tool_context.state.update(state_delta)
        
        # Log key information for debugging
        status = query_details_data.get('status', 'UNKNOWN')
        iteration = query_details_data.get('processing_flags', {}).get('iteration_count', 0)
        missing_fields = query_details_data.get('processing_flags', {}).get('missing_critical_fields', [])
        
        logger.info(f"Successfully updated session state - Status: {status}, Iteration: {iteration}, Missing: {missing_fields}")
        
        return f"Successfully updated session with query_details. Status: {status}, Iteration: {iteration}"
        
    except json.JSONDecodeError as e:
        error_msg = f"Invalid JSON provided for query_details: {str(e)}"
        logger.error(error_msg)
        return f"Error: {error_msg}"
    except Exception as e:
        error_msg = f"Error updating session with query_details: {str(e)}"
        logger.error(error_msg)
        return f"Error: {error_msg}"