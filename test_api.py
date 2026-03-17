from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200

def test_generate_text():
    response = client.post("/generate", data={"prompt": "Hello, world!"})
    assert response.status_code == 200


