from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
from pathlib import Path
import json
from datetime import datetime, UTC

app = FastAPI()

# LOGGING
LOG_DIR = Path("/logs")
LOG_FILE = LOG_DIR/ "prediction_logs.json"
LOG_DIR.mkdir(parents=True, exist_ok=True)


# Field and min_length at 1 allow me to use pydantic so I don't need to manually do if not input.text.strip() in my endpoint functions
class TextInput(BaseModel):
    text: str = Field(..., min_length=1)
    true_sentiment: str = Field(..., pattern="^(positive|negative)$")

class SentimentResponse(BaseModel):
    sentiment: str

# load the model just once at startup
try:
    model = joblib.load('sentiment_model.pkl')
except Exception:
    raise HTTPException(status_code=500, detail='Model could not be loaded')


# read_root from slideshow - i hear this is nice for setting up a friendly welcome or for tutorials
@app.get('/')
def read_root():
    return {'message': 'Welcome to the Sentiment Analysis API!'}

@app.get('/health')
def health_check():
    return{'status': 'ok'}

@app.post('/predict', response_model=SentimentResponse)
def predict_sentiment(input: TextInput):
    try:
        prediction = model.predict([input.text])[0]
        # waht to store in log entry
        log_entry = {
            "timestamp": datetime.now(UTC).isoformat(),
            "request_text": input.text,
            "predicted_sentiment": prediction,
            "true_sentiment": input.true_sentiment
        }
        # add it to the log file
        with LOG_FILE.open("a") as f:
            f.write(json.dumps(log_entry) + "\n")
        # return the sentiment prediction
        return {'sentiment': prediction}
    except Exception as e:
        raise HTTPException(status_code = 500, detail=f'Prediction failed: {str(e)}')