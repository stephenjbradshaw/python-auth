import models
from utils import valid_email, valid_password, hash_password, get_email_verification_token
import json


def register(handler, body):
    '''
    Register the user: Validate request, hash password,
    save unverified user to database, send verification email 
    '''
    json_body = json.loads(body)

    try:
        email = json_body['email']
        password = json_body['password']

    except KeyError:
        handler.response(400, 'Missing email or password')
        return

    if not valid_email(email):
        handler.response(400, 'Invalid email')

    if not valid_password(password):
        handler.response(400, 'Invalid password')
        return

    salt, hashed_password = hash_password(password)
    verification_token = get_email_verification_token(email)

    # Save user to database
    models.create_user(email, salt, hashed_password, verification_token)

    handler.response(200, "User created")


def verify_email(handler, body):
    None


def login(handler, body):
    None
