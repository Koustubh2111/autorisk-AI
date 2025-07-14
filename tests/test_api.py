from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from api.risk_scoring_api import app

client = TestClient(app)

valid_input = {
    "timestamp": "2025-07-14T10:22:00",
    "user": "user_10",
    "ip_address": "192.168.1.1",
    "event_type": "login_failure",
    "resource": "/secure/data"
}

@patch("api.risk_scoring_api.xgb.Booster.load_model")
def test_score_log_success(mock_load_model):
    mock_load_model.return_value = None  # Pretend the model loaded successfully
    response = client.post("/score-log", json=valid_input)
    assert response.status_code == 200
    assert "risk_score" in response.json()

@patch("api.risk_scoring_api.xgb.Booster.load_model")
def test_explain_risk_success(mock_load_model):
    mock_load_model.return_value = None
    response = client.post("/explain-risk", json=valid_input)
    assert response.status_code == 200
    assert "risk_score" in response.json()
    assert "explanations" in response.json()

def test_invalid_timestamp():
    bad_input = valid_input.copy()
    bad_input["timestamp"] = "invalid-date"
    response = client.post("/score-log", json=bad_input)
    assert response.status_code == 422
    assert "value_error" in response.json()["detail"][0]["type"]
