import sqlalchemy as sa
from models.models import Advertisement


def test_create_adv(client, user_factory):
    """
    Test for create advertisement for not exists user
    """
    user = user_factory
    response = client.post(
        "advertisement",
        json={"title": "Flask", "description": "hehehe", "user_id": user.id},
    )
    assert response.status_code == 200


def test_create_adv_not_exist_user(client):
    """
    Test for create advertisement for not exists user
    """
    response = client.post(
        "advertisement",
        json={"title": "Flask", "description": "hehehe", "user_id": "1"},
    )
    assert response.status_code == 404


def test_update_adv(client, user_factory, factory, fakery):
    """
    Test for update advertisement
    """
    adv = factory(
        Advertisement,
        title=fakery.word(),
        description=fakery.word(),
        user_id=user_factory.id,
    )
    response = client.patch(
        f"advertisement/{adv.id}",
        json={"title": "hihihi", "description": "hehehe", "user_id": user_factory.id},
    )
    assert response.status_code == 200
    assert response.json["description"] == "hehehe"
    assert response.json["title"] == "hihihi"


def test_part_update_adv(client, user_factory, factory, fakery):
    """
    Test for part update advertisement
    """
    adv = factory(
        Advertisement,
        title=fakery.word(),
        description=fakery.word(),
        user_id=user_factory.id,
    )
    response = client.patch(
        f"advertisement/{adv.id}",
        json={"description": "hehehe", "user_id": user_factory.id},
    )
    assert response.status_code == 200
    assert response.json["description"] == "hehehe"


def test_delete_adv(client, user_factory, factory, fakery, session):
    adv = factory(
        Advertisement,
        title=fakery.word(),
        description=fakery.word(),
        user_id=user_factory.id,
    )
    response = client.delete(f"advertisement/{adv.id}")
    assert response.status_code == 200
    del_adv = session.scalar(sa.select(Advertisement).where(Advertisement.id == adv.id))
    assert del_adv is None


def test_get_adv(client, user_factory, factory, fakery):
    adv = factory(
        Advertisement,
        title=fakery.word(),
        description=fakery.word(),
        user_id=user_factory.id,
    )
    response = client.get(f"advertisement/{adv.id}")
    assert response.status_code == 200
