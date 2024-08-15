def test_create_user(client):
    """
    Test for create user
    """
    response = client.post(
        "users", json={"email": "e1@e.org", "password": "pass12345", "name": "Flask"}
    )
    assert response.status_code == 200


def test_login(client, user_factory):
    """
    Test for auth user and get token
    """
    user_data = user_factory()
    response = client.post(
        "login",
        json={
            "email": user_data.get("user").email,
            "password": user_data.get("password"),
        },
    )
    assert response.status_code == 200
    assert response.json.get("access_token") is not None


def test_login_invalid_password(client, user_factory):
    """
    Test for login user with invald password
    """
    user_data = user_factory()
    response = client.post(
        "login",
        json={
            "email": user_data.get("user").email,
            "password": "hihihi",
        },
    )
    assert response.status_code == 401
    assert response.json.get("text") == "Incorrect email or password"


def test_create_user_dublicate(client, user_factory):
    """
    Test for create user if user already exists
    """
    user_data = user_factory()
    client.post(
        "users",
        json={
            "email": user_data.get("user").email,
            "password": user_data.get("password"),
            "name": user_data.get("user").name,
        },
    )
    response = client.post(
        "users",
        json={
            "email": user_data.get("user").email,
            "password": user_data.get("password"),
            "name": user_data.get("user").name,
        },
    )
    assert response.status_code == 400
    assert response.json["error"] == "User already exists"


def test_create_with_invalid_email(client):
    """
    Test for create user with invalid email
    """
    response = client.post(
        "users", json={"email": "hehehe", "password": "pass12345", "name": "Flask"}
    )
    assert response.status_code == 400
    res = response.json["error"]["msg"]
    assert (
        res
        == "value is not a valid email address: An email address must have an @-sign."
    )


def test_create_with_incorrect_password(client):
    """
    Test for create user with incorrect password
    """
    response = client.post(
        "users", json={"email": "aa@ru.ru", "password": "pass", "name": "Flask"}
    )
    assert response.status_code == 400
    res = response.json["error"]["msg"]
    assert res == "Assertion failed, Password is too short"
