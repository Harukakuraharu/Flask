def test_create_user(client):
    """
    Test for create user
    """
    response = client.post(
        "users", json={"email": "e1@e.org", "password": "pass12345", "name": "Flask"}
    )
    assert response.status_code == 200


def test_create_user_dublicate(client):
    """
    Test for create user if user already exists
    """
    client.post(
        "users", json={"email": "e1@e.org", "password": "pass12345", "name": "Flask"}
    )
    response = client.post(
        "users", json={"email": "e1@e.org", "password": "pass12345", "name": "Flask"}
    )
    assert response.status_code == 400


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


def test_create_with_invalid_password(client):
    """
    Test for create user with invalid password
    """
    response = client.post(
        "users", json={"email": "aa@ru.ru", "password": "pass", "name": "Flask"}
    )
    assert response.status_code == 400
    res = response.json["error"]["msg"]
    assert res == "Assertion failed, Password is too short"
