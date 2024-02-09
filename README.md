# Basic Python auth API

A REST API that allows a user to register, verify their email address and login.
Endpoints (all POST, accepting JSON body):

- `/register` – `{"email": "<email>", "password": "<password>"}`
- `/verify-email` – `{"email": "<email>", "token": "<token>"}`
- `/login` – `{"email": "<email>", "password": "<password>"}`

## Run locally

1. Use environment: `python -m venv .venv && source .venv/bin/activate`
2. Install dependencies: `pip install -r requirements.txt`
3. Initialize database: `python setup.py`
4. Start server: `python server.py`

## Testing

1. Run `pytest` which will test each endpoint
