# TaskFlow Python Example: DDSE-First Implementation

This project implements the TaskFlow task management API in Python, following the DDSE methodology and the decision memory from `task-app-tdr-only`.

## Project Structure

```
task-app-python/
├── README.md
├── tdr/
│   ├── mdd/
│   │   └── mdd-001-product-strategy.md
│   ├── adr/
│   │   ├── adr-001-rest-api-architecture.md
│   │   └── adr-002-data-storage-strategy.md
│   ├── system-level/
│   │   ├── edr-001-authentication-strategy.md
│   │   └── edr-002-error-handling-strategy.md
│   └── ...
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── auth.py
│   └── crud.py
├── tests/
│   └── test_api.py
├── requirements.txt
└── openapi.yaml
```

## Key Features
- RESTful API for tasks and users
- JWT authentication, bcrypt password hashing
- SQLite database (SQLAlchemy ORM)
- OpenAPI auto-documentation
- Automated tests
- All major decisions documented as TDRs (see `tdr/`)

## How to Run

1. Install dependencies: `pip install -r requirements.txt`
2. Start the app: `uvicorn app.main:app --reload`
3. Access docs: `http://localhost:8000/docs`

---

This project is a reference implementation for DDSE-compliant, decision-driven, AI-ready software engineering.

