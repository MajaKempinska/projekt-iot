import pytest
from app import app
@pytest.fixture
def client():
    """Tworzy testowego klienta Flaska, przez którego odpytujemy endpointy."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
def test_strona_glowna(client):
    response = client.get("/")
    assert response.status_code == 200
def test_maja(client):
    response = client.get("/maja")
    assert response.status_code == 200
def test_wiadomosci(client):
    response = client.get("/wiadomosci")
    assert response.status_code == 200
def test_kontakt(client):
    response = client.get("/kontakt")
    assert response.status_code == 200
def test_post_kontakt(client):
    response = client.post("/kontakt", data={
    "imie": "Kuba",
    "email": "kuba@gmail.com",
    "wiadomosc": "Hej!"
    })
    assert response.status_code == 200