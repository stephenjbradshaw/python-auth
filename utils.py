import re
import hashlib
import secrets


def valid_password(password: str) -> bool:
    # 8+ characters, 1 uppercase, 1 lowercase, 1 number
    password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$'
    return re.match(password_regex, password)


def valid_email(email: str) -> bool:
    email_regex = r'^[\w\.]+@([\w-]+\.)+[\w-]{2,4}$'
    return re.match(email_regex, email)


def hash_password(password: str) -> tuple[str, str]:
    '''
    Hash the password with random salt and return salt and hash to
    store in the database
    '''
    salt = secrets.token_bytes(16)
    derived_key = hashlib.pbkdf2_hmac(
        'sha256', password.encode("utf-8"), salt, 100000)

    return salt.hex(), derived_key.hex()


def get_email_verification_token(email: str) -> str:
    '''
    Generate a random token to be used for email verification
    The user will click on a link containing this token to verify their email
    '''
    data = email + secrets.token_urlsafe(16)
    token = hashlib.sha256(data.encode()).hexdigest()
    return token
