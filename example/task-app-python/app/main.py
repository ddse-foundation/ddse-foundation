from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app import models, schemas, database, auth, crud, teams, exceptions

# Initialize FastAPI app with enhanced metadata per ADR-001
app = FastAPI(
    title="TaskFlow API",
    description="DDSE-compliant Task Management API implementing TDR-driven architecture",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware per deployment requirements
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register global exception handlers per EDR-002
app.add_exception_handler(Exception, exceptions.global_exception_handler)
app.add_exception_handler(exceptions.TaskFlowException, exceptions.taskflow_exception_handler)
app.add_exception_handler(StarletteHTTPException, exceptions.http_exception_handler)
app.add_exception_handler(RequestValidationError, exceptions.validation_exception_handler)

# Initialize database
database.init_db()

@app.get("/", include_in_schema=False)
def root():
    """Redirect to API documentation"""
    return RedirectResponse(url="/docs")

@app.get("/health")
def health_check():
    """Health check endpoint for deployment monitoring"""
    return {"status": "healthy", "version": "1.0.0"}

# Include routers following IDR-001 API conventions
app.include_router(auth.router)
app.include_router(crud.router)
app.include_router(teams.router)
