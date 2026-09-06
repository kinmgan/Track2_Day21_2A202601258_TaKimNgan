from fastapi.testclient import TestClient
from unittest.mock import MagicMock
import src.serve as serve_module

client = TestClient(serve_module.app)


def test_healthz():
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_score_valid():
    # Mock model
    mock_model = MagicMock()
    mock_model.predict.return_value = [1]
    serve_module.model = mock_model

    features = [39.0, 2.0, 13.0, 4.0, 3.0, 1.0, 1.0, 2174.0, 0.0, 40.0]
    response = client.post("/score", json={"features": features})
    assert response.status_code == 200
    assert response.json() == {"prediction": 1, "label": "thu_nhap_cao"}


def test_score_invalid_len():
    features = [1.0, 2.0]
    response = client.post("/score", json={"features": features})
    assert response.status_code == 400
