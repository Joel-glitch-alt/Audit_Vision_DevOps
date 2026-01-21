# Audit Vision – CI/CD Pipeline with Jenkins, SonarQube & Docker

## 📌 Project Overview

Audit Vision is a Python-based application with a fully automated **CI/CD pipeline** built using **Jenkins**, **SonarQube**, ***AWS***, ***Kubernetes*** and **Docker**.
The pipeline ensures code quality, security, and consistency by integrating static code analysis, quality gates, containerization, and image publishing to Docker Hub.

This project demonstrates a **real-world DevOps workflow** using distributed infrastructure on AWS EC2.

---

## 🏗️ Architecture Overview

**Infrastructure Setup:**

* **Jenkins Master / Agent**: Runs on a dedicated EC2 instance
* **SonarQube Server**: Runs on a separate EC2 instance (Dockerized)
* **Docker Hub**: Stores built application images
* **GitHub**: Source code repository

**Pipeline Flow:**

1. Developer pushes code to GitHub
2. Jenkins pipeline is triggered
3. Code is checked out
4. SonarQube analysis is executed remotely
5. Quality Gate is evaluated
6. Docker image is built
7. Docker image is pushed to Docker Hub

---

## 🧰 Tech Stack

* **Language**: Python 3.9
* **CI/CD**: Jenkins (Declarative Pipeline)
* **Code Quality**: SonarQube (remote EC2)
* **Containerization**: Docker
* **Registry**: Docker Hub
* **Cloud Provider**: AWS EC2

---

## 📂 Project Structure

```
Audit-Vision/
│
├── app.py                  # Main application entry point
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker image definition
├── Jenkinsfile             # Jenkins CI/CD pipeline
├── .gitignore              # Ignored files
├── README.md               # Project documentation
└── .scannerwork/           # SonarQube working directory (generated)
```

---

## ⚙️ Jenkins Pipeline Stages

### 1️⃣ Checkout Code

Pulls the latest code from the GitHub repository.

### 2️⃣ Build

Basic build stage (can be extended for testing or compilation).

### 3️⃣ SonarQube Analysis

* Uses **SonarScanner CLI Docker image**
* Sends analysis results to a **remote SonarQube EC2 server**
* Authenticates using a secure token stored in Jenkins credentials

### 4️⃣ Quality Gate

* Jenkins waits for SonarQube result
* Pipeline **fails automatically** if quality gate is not passed

### 5️⃣ Docker Build & Push

* Builds Docker image from `Dockerfile`
* Authenticates to Docker Hub using Jenkins credentials
* Pushes image to Docker Hub repository

---

## 🔐 Credentials Management

The following credentials are securely stored in Jenkins:

* **SonarQube Token** – Used for code analysis authentication
* **Docker Hub Credentials** – Used for image push

> ⚠️ Credentials are never hard-coded in the pipeline.

---

## 🐳 Docker Image Details

**Base Image:**

```dockerfile
python:3.9-slim
```

**Features:**

* Non-root user for security
* Health check enabled
* Lightweight and production-ready

---

## 🚀 How to Run Locally

```bash
# Build Docker image
docker build -t audit-vision .

# Run container
docker run -p 8000:8000 audit-vision
```

---

## 📊 SonarQube Dashboard

After a successful pipeline run, analysis results can be viewed at:

```
http://<http://54.216.82.245:9000/dashboard?id=audit_key
```

Metrics include:

* Bugs
* Vulnerabilities
* Code smells
* Coverage
* Security hotspots

---

## ✅ Quality & Best Practices

* ✔ Distributed CI/CD architecture
* ✔ Remote SonarQube integration
* ✔ Automated quality gates
* ✔ Secure credential handling
* ✔ Dockerized application
* ✔ Cloud-ready deployment

---

## 📈 Future Improvements

* Add unit & integration testing
* Deploy to AWS ECS / Kubernetes
* Add Trivy image vulnerability scanning
* Add Slack / Email notifications
* Blue-Green or Canary deployments

---

## 👤 Author

**Joel Addition**
DevOps Engineer | Backend Developer

---

## 🏁 Conclusion

This project demonstrates a **professional CI/CD pipeline** suitable for production environments, showcasing modern DevOps practices using Jenkins, SonarQube, Docker, and AWS.

Feel free to fork, extend, or adapt this pipeline for your own projects 🚀
