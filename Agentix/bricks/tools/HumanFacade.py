from agentix import tool, State
from typing import Optional, List, Dict, Callable, Any, Union
import requests
import json
import time

# Base URL for Discord bot API
DISCORD_API_BASE = "http://localhost:5000"


@tool
def HF_send_message(
    message: str,
    channel: str = "general",
    msg_type: str = "info",
) -> str:
    """
    Send a message to a specific channel
    Returns: Message ID that can be used for editing
    """
    try:
        response = requests.post(
            f"{DISCORD_API_BASE}/send_message_by_name/{channel}",
            json={"content": message}
        )
        response.raise_for_status()
        return response.json().get('message_id', '')
    except Exception as e:
        print(f"Error sending message: {e}")
        return ''


@tool
def HF_ask_human(message: str) -> str:
    from agentix import Stuff, State
    """
    Ask the human a question via DM and wait for their response
    Returns: The human's response as a string
    """
    print("\n[HF_ask_human] Starting to ask human:", message)

    # Send the question

    # Set up response handling
    # if not 'ask' in State:
    State['ask'] = {"asking": False, 'reply': None}
    assert not State['ask']['asking']
    State['ask']['asking'] = True
    msg_id = HF_send_dm(message)

    print(f"[HF_ask_human] Sent DM, got message ID: {msg_id}")

    if not msg_id:
        print("[HF_ask_human] Failed to send DM")
        return ''
    print('waiting for human to reply.', end='')
    while not State['ask']['reply']:
        print('.', end='')
        time.sleep(0.5)
        State.reset_cache()

    reply = State['ask']['reply']
    State['ask']['asking'] = False
    State['ask']['reply'] = None
    return reply

    # Store the question details
    State['ask_human']['pending_questions'][msg_id] = True
    print(f"[HF_ask_human] Added pending question {msg_id}")

    # Register DM callback if not already done
    def dm_callback(content: str, response_id: str):
        print(
            f"[HF_ask_human] Got DM callback - content: {content}, response_id: {response_id}")
        # Check if this is a response to a pending question
        for question_id in State['ask_human']['pending_questions']:
            if State['ask_human']['pending_questions'][question_id]:
                print(f"[HF_ask_human] Found matching question {question_id}")
                # Store the response
                State['ask_human']['responses'][question_id] = content
                # Mark question as answered
                State['ask_human']['pending_questions'][question_id] = False
                print(
                    "[HF_ask_human] Stored response and marked question as answered")
                break

    print("[HF_ask_human] Registering DM callback")
    HF_on_dm(dm_callback)

    # Wait for response with timeout
    max_wait = 3000  # 5 minutes timeout
    wait_time = 0
    print("[HF_ask_human] Starting to wait for response")

    while wait_time < max_wait:
        if msg_id in State['ask_human']['responses']:
            response = State['ask_human']['responses'][msg_id]
            print(f"[HF_ask_human] Got response: {response}")
            # Cleanup
            del State['ask_human']['pending_questions'][msg_id]
            del State['ask_human']['responses'][msg_id]
            print("[HF_ask_human] Cleaned up state")
            return response
        time.sleep(1)
        wait_time += 1
        if wait_time % 10 == 0:  # Print every 10 seconds
            print(f"[HF_ask_human] Still waiting... {wait_time}/{max_wait}")

    print("[HF_ask_human] Timed out waiting for response")
    return 'Human timed out'


@tool
def HF_edit_message(
    message_id: str,
    new_content: str,
) -> bool:
    """
    Edit an existing message
    Returns: True if successful, False otherwise
    """
    try:
        response = requests.post(
            f"{DISCORD_API_BASE}/edit/{message_id}",
            json={"content": new_content}
        )
        response.raise_for_status()
        print(response, f"{response=}")
        input('ca')
        return True
    except Exception as e:
        print(f"Error editing message: {e}")
        return False


@tool
def HF_send_dm(
    message: str,
) -> str:
    """
    Send a direct message to the configured user
    Returns: Message ID that can be used for editing
    """
    try:
        response = requests.post(
            f"{DISCORD_API_BASE}/send_dm",
            json={"content": message}
        )
        response.raise_for_status()
        result = response.json()
        if result.get('status') != 'success':
            print(
                f"Error sending DM: {result.get('message', 'Unknown error')}")
            return ''
        return result.get('message_id', '')
    except Exception as e:
        print(f"Error sending DM: {e}")
        return ''


@tool
def HF_on_message(channel: str, callback: Callable[[str, str, str], None]) -> None:
    """
    Register a callback for messages in a specific channel
    Callback receives: channel_name, message_content, message_id
    """
    if 'discord' not in State:
        State['discord'] = {
            'callbacks': {},
            'message_map': {}
        }
    State['discord']['callbacks'][channel] = callback


@tool
def HF_on_dm(callback: Callable[[str, str], None]) -> None:
    """
    Register a callback for direct messages
    Callback receives: message_content, message_id
    """
    HF_on_message('DM', lambda _, content, msg_id: callback(content, msg_id))
