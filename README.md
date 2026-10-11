# Stethoscope Sound Analyzer

A full-stack research and decision-support web application for recording stethoscope audio, classifying heart vs lung sounds, and suggesting possible pathologies.

## Overview

This project includes:
- Frontend: React + Vite web app
- Backend: FastAPI service with JWT authentication
- Database: PostgreSQL via SQLAlchemy
- Audio pipeline: microphone capture, waveform preview, and sound analysis
- Model layer: prototype classifier with a real-model hook for clinical-grade replacement

## Stack

- Frontend: React, Vite, CSS
- Backend: Python, FastAPI, SQLAlchemy, Alembic-ready models
- Database: PostgreSQL
- Auth: JWT with password hashing
- Containerization: Docker + Docker Compose

## Features

- User registration and login
- Audio upload or real-time microphone capture
- Sound classification: heart or lung sound
- Pathology suggestion engine
- Saved analysis history in the database
- Docker-ready deployment

## Project structure

```text
backend/
  app/
    __init__.py
    auth.py
    config.py
    db.py
    main.py
    models.py
    schemas.py
    services/
      audio_service.py
      model_service.py
  Dockerfile
  requirements.txt
frontend/
  package.json
  vite.config.js
  index.html
  src/
    App.jsx
    api.js
    main.jsx
    index.css

docker-compose.yml
.env.example
.gitignore
README.md
```

## Local development

### 1. Copy environment file

```bash
cp .env.example .env
```

### 2. Start services

```bash
docker compose up --build
```

Then open:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000/docs
- PostgreSQL: localhost:5432

### 3. Create an account

Use the frontend to register a new user, then upload or record sound.

## Important safety notice

This application is intended for research and decision support only. It is not a replacement for medical diagnosis by a qualified clinician. The model layer is a prototype and requires validation against clinically curated datasets before any diagnostic use.

## Model integration note

The backend exposes a model service placeholder. To replace the prototype classifier with a real pretrained audio model, update `backend/app/services/model_service.py` and point it to your trained model artifacts stored in `backend/models/`.

## License

MIT
