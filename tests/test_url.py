import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import collection, cache

client = TestClient(app)

@pytest.fixture(autouse=True)
def clean_db():
    # Clean MongoDB and Redis before each test
    collection.delete_many({})
    cache.flushall()

def test_shorten_url_success():
    response = client.post("/shorten", json={"long_url": "https://example.com"})
    assert response.status_code == 200
    data = response.json()
    assert "short_url" in data
    assert data["short_url"].startswith("http://localhost:8000/")

def test_retrieve_url_success():
    # First, shorten a URL
    shorten = client.post("/shorten", json={"long_url": "https://test.com"})
    assert shorten.status_code == 200
    short_url = shorten.json()["short_url"].split("/")[-1]

    # Then, retrieve it
    retrieve = client.get(f"/{short_url}")
    assert retrieve.status_code == 200
    assert retrieve.json()["long_url"].rstrip("/") == "https://test.com"

def test_retrieve_url_not_found():
    response = client.get("/nonexistent")
    assert response.status_code == 404
    assert response.json()["detail"] == "Short URL cannot be found!"

def test_analytics_count():
    # Create and access URL
    shorten = client.post("/shorten", json={"long_url": "https://analytics.com"})
    assert shorten.status_code == 200
    short_url = shorten.json()["short_url"].split("/")[-1]

    # Hit the short URL multiple times
    for _ in range(5):
        retrieve = client.get(f"/{short_url}")
        assert retrieve.status_code == 200

    analytics = client.get(f"/analytics/{short_url}")
    assert analytics.status_code == 200
    assert analytics.json()["access_count"] == 5
