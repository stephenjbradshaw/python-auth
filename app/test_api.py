import time
import requests
import pytest
import subprocess
import db.setup
import os


@pytest.fixture()
def setup_server():
    # Setup test db
    os.environ["ENV"] = "test"
    db.setup.init_db()

    # Start server
    process = subprocess.Popen(["python", "app/server.py"])
    time.sleep(2)

    yield process

    # Stop server
    process.terminate()

    # Remove test db
    if os.path.exists("test.db"):
        os.remove("test.db")
    del os.environ["ENV"]


VALID_EMAIL = "test@example.com"
VALID_PASSWORD = "Password1"


def test_basic_api_functionality(setup_server):
    # Check the server is running
    response = requests.get("http://localhost:8000")
    assert response.status_code == 200
    assert response.text == "OK"

    # GET to unknown route should return 404
    response = requests.get("http://localhost:8000/oops")
    assert response.text == "Not Found"

    # POST to unknown route should return 404
    response = requests.post("http://localhost:8000/quatsch",
                             json={"email": VALID_EMAIL, "password": VALID_PASSWORD})
    assert response.status_code == 404

    # POST should return 400 if incorrect content type
    response = requests.post(
        "http://localhost:8000/register", headers={"Content-Type": "text/plain"})
    assert response.status_code == 400
    assert response.text == "Only JSON payloads allowed"

    # POST should return 400 if body is empty
    response = requests.post(
        "http://localhost:8000/register", headers={"Content-Type": "application/json"})
    assert response.status_code == 400
    assert response.text == "Empty request body"


def test_register_validation(setup_server):
    # Missing email
    response = requests.post("http://localhost:8000/register",
                             json={"password": VALID_PASSWORD})
    assert response.status_code == 400
    assert response.text == "Missing email or password"

    # Missing password
    response = requests.post("http://localhost:8000/register",
                             json={"email": VALID_EMAIL})
    assert response.status_code == 400
    assert response.text == "Missing email or password"

    # Invalid email
    response = requests.post("http://localhost:8000/register",
                             json={"email": "quatsch", "password": VALID_PASSWORD})
    assert response.status_code == 400
    assert response.text == "Invalid email"

    # Invalid password
    response = requests.post("http://localhost:8000/register",
                             json={"email": VALID_EMAIL, "password": "insecure"})
    assert response.status_code == 400
    assert response.text == "Invalid password"


def test_register_flow(setup_server):
    # Importing models here to get correct ENV from fixture
    import models

    # Register an (unverified) user
    response = requests.post("http://localhost:8000/register",
                             json={"email": VALID_EMAIL, "password": VALID_PASSWORD})
    assert response.status_code == 200
    assert response.text == "User created"

    # Check user cannot log in even with correct password, as email unverified
    response = requests.post("http://localhost:8000/login",
                             json={"email": VALID_EMAIL, "password": VALID_PASSWORD})
    assert response.status_code == 401
    assert response.text == "Unauthorized"

    # Try to verify user with wrong token
    response = requests.post("http://localhost:8000/verify-email",
                             json={"email": VALID_EMAIL, "token": "quatsch"})
    assert response.status_code == 401
    assert response.text == "Unauthorized"

    # Get the verification token from the database (this would be sent by email)
    user = models.get_user_by_email(VALID_EMAIL)
    token = user.email_verification_token

    # Verify the user
    response = requests.post("http://localhost:8000/verify-email",
                             json={"email": VALID_EMAIL, "token": token})
    assert response.status_code == 200
    assert response.text == "User verified"

    # User should now be able to log in, as they are verified
    response = requests.post("http://localhost:8000/login",
                             json={"email": VALID_EMAIL, "password": VALID_PASSWORD})
    assert response.status_code == 200
    assert response.text == "Login successful"

    # Incorrect password should not allow login
    response = requests.post("http://localhost:8000/login",
                             json={"email": VALID_EMAIL, "password": "quatsch"})
    assert response.status_code == 401
    assert response.text == "Unauthorized"
