# Video Upload and Streaming Utility App

This is a simple web application built with **FastAPI** and **Supabase** that allows users to upload, store, and stream videos with ease. The application provides a way to handle video uploads, while leveraging Supabase for storage and streaming functionality.

<br>

## Tech Stack

- **FastAPI**: A modern, fast web framework for building APIs with Python.
- **Supabase**: Open-source alternative to Firebase, providing database, authentication, and file storage services.
- **Uvicorn**: ASGI server to run the FastAPI app.

<br>

## Installation

To get started with the project, follow these steps:

### 1. Clone the Repository

```bash
https://github.com/anishhguptaa/video-app.git
cd video-app
```

### 2. Set up a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```


### 3. Install the Dependencies
Install the required dependencies from `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Set up Supabase

- Sign up for a Supabase account at supabase.io.
- Create a new project and configure the Storage service to handle video files.
- Obtain the following credentials:
    - Supabase URL
    - Supabase API key
- Rename the `.env.example` file to `.env` and add your credentials.

### 5. Run the Application

```bash
uvicorn main:app --reload
```

This will launch the app on `http://127.0.0.1:8000`.
