# Student Database Application System – Backend

A backend application for managing student records, user authentication, and knowledge-based chatbot interactions. Built with FastAPI, SQLAlchemy, JWT authentication, Google Gemini, LangGraph, ChromaDB, and Docker.

## Features

* **Student Management:** Create, retrieve, update, and delete student records.
* **User Authentication:** User registration and login with password hashing.
* **JWT Authorization:** Protect student and chatbot endpoints.
* **Database Integration:** Store structured student records using SQLAlchemy and SQLite.
* **AI Chatbot:** Answer questions using a knowledge retrieval workflow.
* **Vector Search:** Use ChromaDB for semantic retrieval of relevant knowledge.
* **API Documentation:** Interactive API documentation through Swagger UI.
* **Docker Support:** Build and run the backend in a Docker container.
* **Automated Testing:** Test API functionality using pytest.

## Technology Stack

| Component        | Technology         |
| ---------------- | ------------------ |
| Backend          | Python, FastAPI    |
| Database         | SQLite, SQLAlchemy |
| Authentication   | JWT, PyJWT         |
| Password Hashing | pwdlib, Argon2     |
| AI Model         | Google Gemini      |
| Workflow         | LangGraph          |
| Vector Database  | ChromaDB           |
| Testing          | pytest, HTTPX      |
| Containerization | Docker             |

## Project Structure

```text
student-database-backend/
├── app/
│   ├── core/
│   ├── models/
│   ├── schemas/
│   ├── crud/
│   ├── routes/
│   ├── services/
│   └── main.py
├── tests/
├── Dockerfile
├── .dockerignore
├── .gitignore
├── requirements.txt
└── README.md
```

## Prerequisites

* Python 3.12 or compatible version
* pip
* Git
* Docker (optional)
* A Google Gemini API key for chatbot functionality

## Local Installation

### 1. Clone the repository

```bash
git clone https://github.com/Moddu-Bhanu/student-database-backend.git
cd student-database-backend
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
DATABASE_URL=sqlite:///./students.db
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=your_configured_gemini_model
SECRET_KEY=your_generated_secret_key
```

Use your own valid values. Never commit `.env` or expose your API keys and secret key.

### 5. Run the application

```bash
uvicorn app.main:app --reload
```

The API will be available at:

* API: http://127.0.0.1:8000
* Swagger UI: http://127.0.0.1:8000/docs

## Authentication

Register a user through the registration endpoint, then log in to obtain a JWT access token.

Include the token when calling protected endpoints:

```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

## API Endpoints

| Method | Endpoint                 | Description                                |
| ------ | ------------------------ | ------------------------------------------ |
| POST   | `/auth/register`         | Register a user                            |
| POST   | `/auth/login`            | Log in and obtain a token                  |
| POST   | `/students/`             | Create a student                           |
| GET    | `/students/`             | Retrieve students                          |
| GET    | `/students/{student_id}` | Retrieve a student by ID                   |
| PUT    | `/students/{student_id}` | Update a student                           |
| DELETE | `/students/{student_id}` | Delete a student                           |
| POST   | `/chatbot/chat`          | Ask the knowledge-based chatbot a question |

Use Swagger UI to inspect request schemas and test the endpoints.

## Run with Docker

Build the image:

```bash
docker build -t student-database-backend .
```

Run the container with your environment variables:

```bash
docker run -d --name student-backend -p 8000:8000 --env-file .env student-database-backend
```

Open http://127.0.0.1:8000/docs to access the API.

For persistent Docker storage, use the configured database and ChromaDB paths and mount a host directory to `/app/data`.

## Run Tests

```bash
python -m pytest -v
```

## Security Notes

* Keep API keys and secret keys in environment variables.
* Do not commit `.env`, database files, or generated vector-store data.
* Use password hashing rather than storing plain-text passwords.
* Protect private student records with authentication and authorization.
* Use HTTPS and appropriately managed secrets when deploying to production.

## Future Enhancements

* Role-based access control
* Improved chatbot evaluation and retrieval
* Additional database support
* Cloud deployment
* Expanded automated test coverage

## Author

**Bhanu Vardhan Reddy**

GitHub: [Moddu-Bhanu](https://github.com/Moddu-Bhanu)
