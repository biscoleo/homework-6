import requests
import pandas as pd 
from sklearn.metrics import accuracy_score
import argparse 
import json 

# Your script must read the file, loop through each item, send the text to the running FastAPI service's /predict endpoint 
# (e.g., at http://localhost:8000/predict), and print a final accuracy score.

API_URL = "http://localhost:8000/predict"

# evaluate function to test api using labeled test data test.json
def evaluate(api_url, test_file):
    with open(test_file, 'r') as f:
        test_data = json.load(f)

    # track correct predictions
    correct = 0
    # track total number of test samples
    total = len(test_data)

    # extract text and sentiment
    for entry in test_data:
        text = entry['text']
        true_sentiment = entry['true_label']

        # make the JSON payload to send in the request
        payload = {
            "text": text,
            "true_sentiment": true_sentiment}

        # send POST request to /predict endpoint
        response = requests.post(f"{api_url}/predict", json=payload)
        # if not successful
        if response.status_code != 200:
            # error message
            print(f"Request failed for text: {text}. Status code: {response.status_code}")
            continue
        # extract the predicted sentiment from the response
        predicted_sentiment = response.json().get('sentiment')

        # now compare the predicted sentiment wiht the actual sentiment
        if predicted_sentiment == true_sentiment:
            correct += 1
    # calculate accuracy
    accuracy = correct / total if total > 0 else 0
    print(f"Accuracy: {accuracy:.2%} ({correct}/{total})")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate Sentiment Analysis API")
    # required for path to test data
    parser.add_argument("--test-data", type=str, required=True, help="Path to test JSON file")
    # optional for api url -- default being localhost
    parser.add_argument("--api-url", type=str, default="http://localhost:8000", help="URL of the API")
    args = parser.parse_args()
    # run the evaluate fucntion
    evaluate(args.api_url, args.test_data)
