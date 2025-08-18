# Sentiment Analysis Deployment on AWS EC2

---

### **DESCRIPTION**

This project deploys a complete sentiment analysis system on an AWS EC2 instance using Docker containers. It includes two main services running on the EC2 server:

- **FastAPI Backend:** Serves sentiment prediction requests.
- **Streamlit Monitoring Dashboard:** Visualizes prediction logs and model performance metrics.

The two services run in separate Docker containers sharing a volume for logs, enabling communication. The EC2 instance acts as the host for these containers, allowing remote access via the public IP.

---

### **SYSTEM ARCHITECTURE**

| Component           | Description                                                  |
|---------------------|--------------------------------------------------------------|
| AWS EC2 Instance    | Ubuntu server hosting Docker containers                      |
| Docker             | Containerizes the FastAPI and Streamlit apps                 |
| Docker Volume      | Shared log volume mounted to both containers                 |
| Security Groups    | Configured to allow ports 8000 (API) and 8501 (Streamlit)    |

---

### **PROJECT STRUCTURE**

| File/Folder          | Purpose                                               |
|---------------------|-------------------------------------------------------|
| `api/`              | FastAPI application serving sentiment predictions     |
| `monitoring/`       | Streamlit dashboard for monitoring logs and metrics   |
| `logs/`             | Shared directory for prediction logs                   |
| `Makefile`          | Automates Docker build, run, and cleanup tasks         |
| `evaluate.py`       | Script to test API predictions and collect feedback    |
| `test.json`         | Sample test data used by `evaluate.py`                  |
| `README.md`         | Project documentation                                   |

---

### **DEPLOYMENT ON AWS EC2**

#### Setup Summary:

1. Launched Ubuntu EC2 instance with proper security group rules:
   - Port 22 open for SSH (your IP only recommended)
   - Port 8000 open for FastAPI
   - Port 8501 open for Streamlit

2. Connected via SSH using the PEM key.

3. Installed Docker, Git, and other dependencies.

4. Cloned the repo and built Docker images:
   ```bash
   make build-api
   make build-monitor
   ```

5. Run the containers (Makefile updated from previous assignemnt to run in detached mode).
    ```bash
    make run-api
    make run-monitor
    ```

6. To access the FastAPI and the Streamlit dashboard:
- FastAPI docs at ```http://<EC2-Public-IP>:8000/docs```
- Streamlit dashboard at ```http://<EC2-Public_IP>:8501```

