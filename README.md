# Basic Python auth API

A REST API that allows a user to register, verify their email address and login.
Endpoints:

| Endpoint               | Sample JSON body                                 | Description                                                                                                                                                                                                                              |
| ---------------------- | ------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `/` (GET)              | N/A                                              | Responds with 200                                                                                                                                                                                                                        |
| `/register` (POST)     | `{"email": "<email>", "password": "<password>"}` | Creates user in database, with hashed & salted password and verification token. In a real app a link containing the token would be sent by email. This link would open a page in the front end which calls the `/verify-email` endpoint. |
| `/verify-email` (POST) | `{"email": "<email>", "token": "<token>"}`       | If supplied email and token match those in the database, verify the user so that they can log in.                                                                                                                                        |
| `/login` (POST)        | `{"email": "<email>", "password": "<password>"}` | Providing the user has been verified, authorize login if the email and password match those in the database. A real app would then issue a JWT or similar.                                                                               |

## Run locally

1. Use environment: `python -m venv .venv && source .venv/bin/activate`
2. Install dependencies: `pip install -r requirements.txt`
3. Initialize database: `python app/db/setup.py`
4. Start server: `python app/server.py`

## Testing

1. Run `pytest` which will test each endpoint
