import streamlit as st
import pandas as pd 
import json 
from datetime import datetime 
import matplotlib.pyplot as plt 
import os 
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score

# get the logs to access that data for visuals
LOG_PATH = "/logs/prediction_logs.json"
def load_logs():
    logs = []
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r") as f:
            for line in f:
                try:
                    # load in json file 
                    logs.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return pd.DataFrame(logs)

# get the imdb dataset, from this same folder
IMDB_PATH = "/app/IMDB Dataset.csv"
def load_imdb_dataset():
    return pd.read_csv(IMDB_PATH)


# The dashboard must display the following monitoring plots:
# Data Drift Analysis: 
# Create a histogram or density plot comparing the distribution of sentence lengths from your IMDB Dataset.csv against the lengths from the logged inference requests. 

def plot_sent_len_drift(logs_df, imdb_df):
    # get the text length from each entry in logs and imdb
    logs_df['text_length'] = logs_df['request_text'].apply(len)
    imdb_df['text_length'] = imdb_df['review'].apply(len)

    # little comment on dashboard to see what the length is for each
    st.write(f"IMDB dataset average sentence length: {imdb_df['text_length'].mean():.2f}")
    st.write(f"Logged requests average sentence length: {logs_df['text_length'].mean():.2f}")

    # plotting the data
    fig, ax = plt.subplots()
    ax.hist(imdb_df['text_length'], bins=30, alpha=0.5, label='IMDB Dataset', color='blue')
    ax.hist(logs_df['text_length'], bins=30, alpha=0.5, label='Logged requests', color='orange')
    ax.set_xlabel('Sentence length')
    ax.set_ylabel('Frequency')
    ax.legend()
    # get it to show up in streamlit
    st.pyplot(fig)



# Target Drift Analysis: 
# Create a bar chart showing the distribution of predicted sentiments from the logs vs trained sentiments

def plot_target_drift(logs_df, imdb_df):
    # positive and negative preds 
    pred_counts = logs_df['predicted_sentiment'].value_counts(normalize=True)
    train_counts = imdb_df['sentiment'].value_counts(normalize=True)
    # drift df to store / plot
    drift_df = pd.DataFrame({
        'Predicted': pred_counts,
        'Training': train_counts
    }).fillna(0)

    st.subheader('Target drift - sentiment distribution')
    # bar plot for target drift 
    fig, ax = plt.subplots()
    drift_df.plot(kind='bar', ax=ax)
    ax.set_ylabel('Proportion')
    ax.set_xlabel('Sentiment')
    st.pyplot(fig)



# Model Accuracy & User Feedback:
# From the true_sentiment logged in the logs
# Calculate and display the model's accuracy and precision based on all collected feedback.

def calc_metrics(logs_df):
    # get feedback logs that exist
    feedback_df = logs_df.dropna(subset=['true_sentiment'])
    # if there are none yet
    if feedback_df.empty:
        return None, None
    # get true labels and predicted labels
    y_true = feedback_df['true_sentiment']
    y_pred = feedback_df['predicted_sentiment']
    # calculate accuracy and precision
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, average='weighted')
    return acc, prec


# Implement Alerting: 
# If the calculated accuracy drops below 80%, display a prominent warning banner at the top of the dashboard using st.error().
st.title("Sentiment Model Monitoring Dashboard")

logs_df = load_logs()
imdb_df = load_imdb_dataset()

# st.subheader('raw logs preview')
# st.write(logs_df.head())
# st.subheader("IMDB dataset preview")
# st.write(imdb_df.head())

# warn if empty
if logs_df.empty:
    st.warning("No log data found yet")
else:
    st.success(f"Loaded {len(logs_df)} entries")

    # call the funcs that generate graphs to display the data
    plot_sent_len_drift(logs_df, imdb_df)
    plot_target_drift(logs_df, imdb_df)

    acc, prec = calc_metrics(logs_df)
    st.subheader('Model Performance based on use feedback')

    if acc is not None:
        # show accuracy and precision and show warning message if accuracy goes below 80%
        st.write(f"Accuracy: {acc*100:.2f}%")
        st.write(f"Precision: {prec*100:.2f}%")
        if acc < 0.8:
            st.error("ALERT: the model accuracy has dropped below 80%")
    else:
        st.info("No use feedback yet to calculate")