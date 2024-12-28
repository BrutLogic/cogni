# Creating HTTP Endpoints

Cogni makes it easy to expose your agents and tools via HTTP endpoints.

## Basic Endpoint

```python
from cogni import endpoint

@endpoint
def hello():
    return {"message": "Hello World"}
```

## Custom Routes

```python
from cogni import endpoint

@endpoint('/api/v1/data')
def get_data():
    return {"data": "some data"}

@endpoint('/users/<user_id>')
def get_user(user_id: str):
    return {"user_id": user_id}
```

## HTTP Methods

```python
from cogni import get, post, put, delete

@get('/items')
def list_items():
    return {"items": [...]}

@post('/items')
def create_item():
    return {"status": "created"}

@put('/items/<id>')
def update_item(id: str):
    return {"status": "updated"}

@delete('/items/<id>')
def delete_item(id: str):
    return {"status": "deleted"}
```

## Agent Endpoints

```python
from cogni import endpoint, Agent

@endpoint('/chat')
def chat():
    message = request.json['message']
    agent = Agent['ChatBot']
    response = agent(message)
    return {"response": response}
```

## Request Handling

```python
from cogni import endpoint
from flask import request

@endpoint('/upload')
def upload():
    if 'file' not in request.files:
        return {"error": "No file"}, 400
        
    file = request.files['file']
    # Process file
    return {"status": "uploaded"}
```

## Authentication

```python
from cogni import endpoint
from functools import wraps

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization')
        if not auth:
            return {"error": "No auth"}, 401
        return f(*args, **kwargs)
    return decorated

@endpoint('/secure')
@require_auth
def secure():
    return {"data": "secret"}
```

## WebSocket Support

```python
from cogni import websocket

@websocket('/ws')
def ws_handler(ws):
    while True:
        message = ws.receive()
        ws.send(f"Echo: {message}")
```

## Error Handling

```python
from cogni import endpoint, HTTPError

@endpoint('/risky')
def risky():
    try:
        # Risky operation
        raise ValueError("Something went wrong")
    except ValueError as e:
        raise HTTPError(400, str(e))
```

## Running the Server

```bash
cogni serve --port 5000
```

## Next Steps

- Add [state management](states.md)
- Create a [swarm of agents](first_swarm.md)
- Implement monitoring
