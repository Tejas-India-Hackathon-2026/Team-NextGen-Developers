# 🚀 Platform Deployment & Production Guide

This guide provides instructions for deploying the **Student Resource Sharing Platform** to various cloud and container environments.

---

## 1. Streamlit Community Cloud (Recommended for Hackathons)

1. Fork or push the repository to GitHub.
2. Visit [share.streamlit.io](https://share.streamlit.io) and log in with GitHub.
3. Click **New app** and select your repository `Tejas-India-Hackathon-2026/Team-NextGen-Developers`.
4. Set:
   - **Main file path**: `app.py`
   - **Python version**: `3.10` or higher
5. Click **Deploy!**

---

## 2. Docker Container Deployment

### Build the Image
```bash
docker build -t student-resource-platform:latest .
```

### Run Container Locally
```bash
docker run -d -p 8501:8501 --name campus-portal student-resource-platform:latest
```

### Docker Compose
```bash
docker-compose up -d --build
```
Access the application at `http://localhost:8501`.

---

## 3. Environment Variables
Optional configuration via `.env`:
```env
PORT=8501
STREAMLIT_SERVER_HEADLESS=true
MAX_UPLOAD_SIZE_MB=50
```
