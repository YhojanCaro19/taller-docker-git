from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_index_responde_ok():
    respuesta = client.get("/")
    assert respuesta.status_code == 200
    cuerpo = respuesta.json()
    assert "mensaje" in cuerpo
    assert "version" in cuerpo


def test_health_responde_healthy():
    respuesta = client.get("/health")
    assert respuesta.status_code == 200
    assert respuesta.json() == {"status": "healthy"}
