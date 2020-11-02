from fastapi.testclient import TestClient

import server.main as server

app = server.app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 404
