# Discord Bot API Documentation

The base url is http://localhost:5000/

## Endpoints

### POST /post
Post a message to a channel
- Body: `{"content": "message text", "channel": "channel_name"}`
- Channel defaults to "general" if not specified
- Returns: `{"status": "success", "message_id": "id"}`

### POST /send_message/{channel_id}
Send message to channel by ID
- Body: `{"content": "message text"}`
- Returns: Message ID and status

### POST /send_message_by_name/{channel_name}
Send message to channel by name
- Body: `{"content": "message text"}`
- Returns: Message ID and status

### POST /reply/{message_id}/{reply_text}
Reply to a specific message
- Returns: Reply message ID and status

### POST /send_dm
Send direct message to user defined in user.yaml
- Body: `{"content": "message text"}`
- Returns: Message ID and status

### POST /send_dm/{user_id}/{message}
Send direct message to user
- Returns: Message ID and status

### POST /edit/{message_id}
Edit a bot message
- Body: `{"content": "new text"}`
- Returns: Status and message ID

### GET /messages
List all bot messages

### GET /wip
Generate channel mapping JSON file
- Creates channels.json with name->id mapping
- Returns: Success status

### GET /kill
Shutdown the bot and server

## Available Channels

- général (1258679259434713091)
- general (1311278452933922837)
- lucy (1312108804036366346)
- coder-log (1312108841441427496)
- hitl (1312113326922137750)
- config (1312115776601194548)
- front (1312115830791602236)
- tool-maker (1312367815474286633)
- prompter (1312367843651747870)
- general-logs (1312367880150585427)

## Message Events

The bot automatically tracks messages from user "poltronsuperstar":
- Stores message content, timestamp, channel info
- Tracks attachments, mentions, embeds
- Records message edits and other metadata
- Maintains list of active channels
- Saves all data to user.yaml

For other users:
- Auto-replies to DMs with "I'll think about it"
- Forwards messages to external service endpoint:
  POST http://localhost:5555/post
  Body: {"id": "message_id", "content": "message_content", "channel": "channel_name"}
  Note: For DMs, channel is set to "DM"
