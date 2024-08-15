import sqlalchemy as sa
from models.models import Advertisement


def test_create_adv(client, user_factory):
    """
    Test for create advertisement
    """
    user = user_factory()
    token = user.get("token")
    response = (
        client.post(
            "advertisement",
            json={
                "title": "Flask",
                "description": "hehehe",
                "user_id": user.get("user").id,
            },
            headers={"Authorization": f"Bearer {token}"},
        ),
    )
    assert response[0].status_code == 200


def test_create_adv_not_auth(client, user_factory):
    """
    Test for create advertisement when user is not authorization
    """
    user = user_factory()
    response = client.post(
        "advertisement",
        json={"title": "Flask", "description": "hehehe", "user_id": user.get("user").id},
    )
    assert response.status_code == 401



def test_update_adv(client, user_factory, factory, fakery):
    """
    Test for update advertisement
    """
    user = user_factory()
    token = user.get("token")
    adv = factory(
        Advertisement,
        title=fakery.word(),
        description=fakery.word(),
        user_id=user.get("user").id,
    )
    response = (
        client.patch(
            f"advertisement/{adv.id}",
            json={"title": "hihihi", "description": "hehehe", "user_id": adv.user_id},
            headers={"Authorization": f"Bearer {token}"},
        ),
    )
    assert response[0].status_code == 200
    assert response[0].json["description"] == "hehehe"
    assert response[0].json["title"] == "hihihi"


def test_update_adv_not_auth(client, user_factory, factory, fakery):
    """
    Test for update advertisement when user not auth
    """
    adv = factory(
        Advertisement,
        title=fakery.word(),
        description=fakery.word(),
        user_id=user_factory().get("user").id,
    )
    response = client.patch(
        f"advertisement/{adv.id}",
        json={"title": "hihihi", "description": "hehehe", "user_id": adv.user_id},
    )
    assert response.status_code == 401


def test_part_update_adv(client, user_factory, factory, fakery):
    """
    Test for part update advertisement
    """
    user = user_factory()
    token = user.get("token")
    adv = factory(
        Advertisement,
        title=fakery.word(),
        description=fakery.word(),
        user_id=user.get("user").id,
    )
    response = (
        client.patch(
            f"advertisement/{adv.id}",
            json={"description": "hehehe", "user_id": adv.user_id},
            headers={"Authorization": f"Bearer {token}"},
        ),
    )
    assert response[0].status_code == 200
    assert response[0].json["description"] == "hehehe"


def test_part_update_not_owner(client, user_factory, factory, fakery):
    """
    Test for update advertisement when user is not owner
    """
    user_owner = user_factory()
    user_other = user_factory() 
    adv = factory(
        Advertisement,
        title=fakery.word(),
        description=fakery.word(),
        user_id=user_owner.get("user").id,
    )
    response = (
        client.patch(
            f"advertisement/{adv.id}",
            json={"description": "hehehe"},
            headers={"Authorization": f"Bearer {user_other["token"]}"},
        ),
    )
    assert response[0].status_code == 401


def test_delete_adv(client, user_factory, factory, fakery, session):
    """
    Test for delete advertisement
    """
    user = user_factory()
    token = user.get("token")
    adv = factory(
        Advertisement,
        title=fakery.word(),
        description=fakery.word(),
        user_id=user.get("user").id,
    )
    response = client.delete(
        f"advertisement/{adv.id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 204
    del_adv = session.scalar(sa.select(Advertisement).where(Advertisement.id == adv.id))
    assert del_adv is None


def test_delete_adv_not_owner(client, user_factory, factory, fakery):
    """
    Test for delete advertisement when user is not owner
    """
    user_owner = user_factory()
    user_other = user_factory()
    adv = factory(
        Advertisement,
        title=fakery.word(),
        description=fakery.word(),
        user_id=user_owner.get("user").id,
    )
    response = client.delete(
        f"advertisement/{adv.id}", headers={"Authorization": f"Bearer {user_other["token"]}"}
    )
    assert response.status_code == 401



def test_get_adv(client, user_factory, factory, fakery):
    """
    Test for get advertisement when user is not owner
    """
    user = user_factory()
    token = user.get("token")
    adv = factory(
        Advertisement,
        title=fakery.word(),
        description=fakery.word(),
        user_id=user.get("user").id,
    )
    response = client.get(
        f"advertisement/{adv.id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200


def test_get_adv_not_owner(client, user_factory, factory, fakery):
    """
    Test for get advertisement when user is not owner
    """
    user = user_factory()
    user_2 = user_factory()
    token = user_2.get("token")
    adv = factory(
        Advertisement,
        title=fakery.word(),
        description=fakery.word(),
        user_id=user.get("user").id,
    )
    response = client.get(
        f"advertisement/{adv.id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 401
