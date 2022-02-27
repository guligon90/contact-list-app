from fastapi.responses import Response
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.contact import GroupTags
from app.tests.utils.contact import (
    create_random_contact,
    format_phone_number,
    random_phone_number,
)
from app.tests.utils.utils import random_lower_string


def test_create_contact(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    data = {
        "name": "What Ever",
        "description": "What Ever's contact",
        "phone_number": random_phone_number(),
        "email": "what@ever.com",
        "group_tag": GroupTags.PERSONAL,
    }

    response = client.post(
        f"{settings.API_V1_STR}/contacts/", headers=superuser_token_headers, json=data,
    )

    assert response.status_code == 200

    content = response.json()

    assert content["name"] == data["name"]
    assert content["description"] == data["description"]
    assert content["phone_number"] == format_phone_number(data["phone_number"])
    assert content["email"] == data["email"]
    assert content["deleted"] is False
    assert content["group_tag"] == data["group_tag"]
    assert "id" in content
    assert "owner_id" in content


def test_create_contact_with_same_phone_number(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    phone_number = random_phone_number()

    def make_post(_phone_number: str) -> Response:
        payload = {
            "name": random_lower_string(),
            "description": random_lower_string(),
            "phone_number": _phone_number,
        }

        return client.post(
            f"{settings.API_V1_STR}/contacts/",
            headers=superuser_token_headers,
            json=payload,
        )

    response = make_post(phone_number)

    assert response.status_code == 200

    response = make_post(phone_number)

    assert response.status_code == 400

    content = response.json()

    assert content["detail"] == {
        "error": "ContactDuplicatedException",
        "message": f"A contact with the phone number {format_phone_number(phone_number)} already exists",
    }


def test_read_contact(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    contact = create_random_contact(db)

    response = client.get(
        f"{settings.API_V1_STR}/contacts/{contact.id}", headers=superuser_token_headers,
    )

    assert response.status_code == 200

    content = response.json()

    assert content["name"] == contact.name
    assert content["description"] == contact.description
    assert content["id"] == contact.id
    assert content["owner_id"] == contact.owner_id


def test_delete_contact(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    contact = create_random_contact(db)

    response = client.delete(
        f"{settings.API_V1_STR}/contacts/{contact.id}", headers=superuser_token_headers,
    )

    # Here, the contacts are not excluded from
    # the DB,so, it's expected a HTTP 200
    assert response.status_code == 200

    content = response.json()

    assert content["deleted"] is True


def test_update_contact(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    contact = create_random_contact(db)

    update_payload = {
        "phone_number": random_phone_number(),
        "name": random_lower_string(),
        "description": random_lower_string(),
        "group_tag": GroupTags.PERSONAL,
    }

    response = client.put(
        f"{settings.API_V1_STR}/contacts/{contact.id}",
        headers=superuser_token_headers,
        json=update_payload,
    )

    assert response.status_code == 200

    content = response.json()

    assert content["name"] == update_payload["name"]
    assert content["description"] == update_payload["description"]
    assert content["group_tag"] == update_payload["group_tag"]
    assert content["phone_number"] == format_phone_number(
        update_payload["phone_number"]
    )


def test_update_contact_with_same_phone_number(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    contact_1 = create_random_contact(db)
    contact_2 = create_random_contact(db)

    assert contact_1.phone_number != contact_2.phone_number

    update_payload = {
        "phone_number": contact_2.phone_number,
    }

    response = client.put(
        f"{settings.API_V1_STR}/contacts/{contact_1.id}",
        headers=superuser_token_headers,
        json=update_payload,
    )

    assert response.status_code == 400

    content = response.json()

    assert content["detail"] == {
        "error": "ContactDuplicatedException",
        "message": f"A contact with the phone number {contact_2.phone_number} already exists",
    }
