# Deployment Guide

## Prerequisites

- Docker and Docker Compose installed
- Ports 8000 (API) and 8501 (Streamlit) open

## Steps

1. Navigate to the `docker` directory:

   ```bash
   cd medical_ai/docker
   ```
2. Build and run the Docker containers:
   ```bash
   docker-compose up --build
   ```
3. Access the API at `http://localhost:8000`
4. Access the Streamlit UI at `http://localhost:8501`

## Environment Variables
 - `ENCRYPTION_KEY`: The encryption key for PHI data
 - `DATABASE_URL`: The database URL for MLflow tracking