# main.py - FIXED VERSION
import asyncio
import uuid
from typing import cast, Dict, Any
import json
from agent import root_agent as agent
from dotenv import load_dotenv
from google.adk.cli.utils import logs
from google.adk.runners import InMemoryRunner
from google.adk.sessions import Session
from google.genai import types as genai_types

from schemas.query_details_schema import QueryDetails, ConversationTurn

load_dotenv(override=True)
logs.log_to_tmp_folder()

# Add logging setup
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def run_single_turn(
    runner: InMemoryRunner,
    app_name: str,
    user_id: str,
    session: Session,
    new_message_text: str
) -> Session:
    """Runs a single turn of the conversation."""
    logger.info(f"Starting turn for user: {user_id}, message: '{new_message_text}'")
    
    content = genai_types.Content(
        role='user', parts=[genai_types.Part.from_text(text=new_message_text)]
    )
    print(f"\n>> User: {new_message_text}")

    final_agent_response_parts = []

    async for event in runner.run_async(
        user_id=user_id,
        session_id=session.id,
        new_message=content,
    ):
        if event.author == "USER":
            continue

        if not event.content or not event.content.parts:
            continue

        current_part_text = ""
        if event.content.parts[0].text:
            current_part_text = event.content.parts[0].text
            logger.info(f"{event.author} text response: {current_part_text[:100]}...")
            print(f"   ** {event.author}: {current_part_text}")
        elif event.content.parts[0].function_call:
            fc = event.content.parts[0].function_call
            logger.info(f"{event.author} calling tool: {fc.name}")
            current_part_text = f"Tool Call: {fc.name} with args: {fc.args}"
            # print(f"   ** {event.author}: Calls {fc.name}({json.dumps(fc.args, indent=2)})")
            print(f"   ** {event.author}: Calls {fc.name}")
        elif event.content.parts[0].function_response:
            fr = event.content.parts[0].function_response
            logger.info(f"Tool {fr.name} responded")
            # Better response parsing
            response_summary = fr.response
            if isinstance(fr.response, dict):
                if fr.response.get("name") == "UserPreferenceAgent":
                    try:
                        response_data = json.loads(fr.response.get("response", "{}"))
                        status = response_data.get('status', 'N/A')
                        missing = response_data.get('processing_flags', {}).get('missing_critical_fields', [])
                        response_summary = f"UPA processed. Status: {status}, Missing: {missing}"
                        logger.info(f"UPA Response - Status: {status}, Missing fields: {missing}")
                    except Exception as e:
                        logger.error(f"Failed to parse UPA response: {e}")
                        response_summary = "UserPreferenceAgent response (parsing error)"
                elif fr.name == "update_session_query_details":
                    response_summary = "Session QueryDetails updated."
                    logger.info("Session state updated successfully")

            current_part_text = f"Tool Response: {fr.name} -> {response_summary}"
            print(f"   ** {event.author}: Receives result from {fr.name}")

        # Collect final response from the root agent
        if event.is_final_response() and event.content.parts[0].text:
            final_agent_response_parts.append(event.content.parts[0].text)

    # Fetch the updated session
    updated_session = cast(
        Session,
        await runner.session_service.get_session(
            app_name=app_name, user_id=user_id, session_id=session.id
        ),
    )

    # Debug session state
    if updated_session.state and "search_results" in updated_session.state:
        print("\n   ---- UPDATED search_results in Session ----")
        print(updated_session.state['search_results'])
        print("  --------------------------------------\n\n")
           
    elif updated_session.state and "query_details" in updated_session.state:
        query_details = updated_session.state['query_details']
        # status = query_details.get('status', 'UNKNOWN')
        # iteration = query_details.get('processing_flags', {}).get('iteration_count', 0)
        # logger.info(f"Session state - Status: {status}, Iteration: {iteration}")
        
        print("\n   ---- UPDATED query_detail in Session ----")
        print(query_details)
        print("  --------------------------------------\n\n")
    else:
        logger.warning("No query_details found in session state")
        print("\n   (No query_detail found in session state yet)")

    if final_agent_response_parts:
        final_response = ''.join(final_agent_response_parts)
        logger.info(f"Agent final response: {final_response[:100]}...")
        print(f"\n<<--->> Forkcast: {final_response}\n\n")
    else:
        logger.info("Agent responded with tool action only, no text response")
        print("\n<<--->> Forkcast: (Responded with a tool action, no direct text for user this turn)\n\n")
        
    return updated_session

async def main():
    app_name = 'forkcast_app'
    user_id = f"user_{uuid.uuid4().hex[:6]}"
    session_id = f"session_{uuid.uuid4().hex[:6]}"

    logger.info(f"Starting Forkcast session for {user_id} on app {app_name}")
    print(f"Starting Forkcast session for {user_id} on app {app_name}")

    runner = InMemoryRunner(
        app_name=app_name,
        agent=agent.root_agent,
    )

    # FIXED: Initialize QueryDetails and create session with initial state
    initial_query_details = QueryDetails.get_default_instance(
        session_id=session_id,
        user_id=user_id
    )
    
    # Create session with initial state containing query_details
    initial_state = {
        "query_details": initial_query_details.model_dump()
    }
    
    # Create session with initial state
    current_session = await runner.session_service.create_session(
        app_name=app_name, 
        user_id=user_id,
        state=initial_state,
        session_id=session_id
    )
    
    logger.info(f"New session created: {current_session.id}")
    print(f"New session created: {current_session.id}")
    print("\ncurrent_session.state['query_details'] initialized with default preferences.", json.dumps(current_session.state['query_details'], indent=2, default=str))

    print("\nWelcome to Forkcast! How can I help you find a great place to eat today?")
    print("Type 'exit' or 'quit' to end the conversation.")

    while True:
        try:
            user_input = await asyncio.to_thread(input, f"\n[{current_session.id[:6]}] Your turn: ")
        except KeyboardInterrupt:
            print("\nExiting...")
            break
            
        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye! Hope you find a great restaurant!")
            break
            
        if not user_input.strip():
            continue

        try:
            current_session = await run_single_turn(
                runner, app_name, user_id, current_session, user_input
            )
        except Exception as e:
            logger.error(f"Error during conversation turn: {e}")
            print(f"Sorry, I encountered an error: {e}")
            continue

        # # Check for terminal state
        # if current_session.state.get("query_details", {}).get("status") == "READY_FOR_SEARCH":
        #     logger.info("Query ready for search - preferences complete")
        #     print("\nForkcast: Preferences seem complete and ready for search!")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nForkcast session ended by user.")