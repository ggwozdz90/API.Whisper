from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.api.routers.health_router import router

app = FastAPI()
app.include_router(router)

client = TestClient(app)


def test_health_check() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.text == ""
