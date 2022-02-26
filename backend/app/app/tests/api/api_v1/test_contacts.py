from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from backend.app.app.tests.utils.contact import create_random_contact


def test_create_contact(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    data = {"title": "Foo", "description": "Fighters"}
    response = client.post(
        f"{settings.API_V1_STR}/contacts/", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == data["title"]
    assert content["description"] == data["description"]
    assert "id" in content
    assert "owner_id" in content


def test_read_contact(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    contact = create_random_contact(db)
    response = client.get(
        f"{settings.API_V1_STR}/contacts/{contact.id}", headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == contact.title
    assert content["description"] == contact.description
    assert content["id"] == contact.id
    assert content["owner_id"] == contact.owner_id
