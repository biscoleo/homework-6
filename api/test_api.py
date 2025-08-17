from fastapi.testclient import TestClient 
from api.main import app

client = TestClient(app)

def test_predict_pos():
    """
    Test the predict positive reviews
    """
    payload = {
        "text": "This movie was so funny!",
        "true_sentiment": "positive"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "sentiment" in data
    assert data["sentiment"] in ["positive", "negative"]


def test_predict_neg():
    """
    Test the predict negative reviews
    """
    payload = {
        "text": "This put me to sleep",
        "true_sentiment": "negative"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "sentiment" in data
    assert data["sentiment"] in ["positive", "negative"]


def test_predict_missing():
    """
    Test if field is missing from payload / request
    """
    payload = {
        "true_sentiment": "positive"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422


def test_predict_empty_text():
    payload = {
        "text": "",
        "true_sentiment": "negative"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422