---
type: IDR
id: idr-003
title: User Authentication Flow
status: Accepted
date: 2025-01-15
decision_owner: Feature Owner
reviewers: [Technical Lead, Security Advisor]
related_decisions: [edr-001, edr-002, adr-002]
depends_on: [edr-001]
supersedes: []
superseded_by: []
component: user-management
---

# IDR-003: User Authentication Flow

## Status
**Accepted** - January 15, 2025

## Context

The user management component requires specific implementation of the JWT authentication strategy (EDR-001) for login, logout, and token refresh operations. The authentication flow must:

- Implement secure credential verification
- Generate and validate JWT tokens according to EDR-001 specifications
- Provide clear authentication endpoints following REST conventions
- Handle authentication errors according to EDR-002 error strategy

### Component Scope
This IDR covers the authentication endpoints and flow:
- User login with username/password
- JWT token generation and response
- Token validation for protected endpoints
- Logout and token invalidation (optional)
- Password reset flow (future scope)

### Technical Requirements
- **JWT Implementation**: Follow EDR-001 token structure and expiration
- **Password Security**: Use bcrypt hashing as specified in EDR-001
- **Error Handling**: Return structured errors per EDR-002
- **Performance**: Authentication within 100ms for valid credentials

## Decision

**We will implement a straightforward authentication flow with login endpoint for token generation, token validation middleware for protected endpoints, and logout endpoint for client-side token cleanup.**

### Authentication Flow Specification

#### Login Flow
1. Client sends POST /auth/login with username/password
2. Server validates credentials against bcrypt hash
3. Server generates JWT token with user context
4. Server returns token with expiration information
5. Client stores token for subsequent requests

#### Protected Endpoint Flow
1. Client includes "Authorization: Bearer {token}" header
2. Server validates JWT signature and expiration
3. Server extracts user context from token payload
4. Server proceeds with authorized operation

#### Logout Flow (Client-Side)
1. Client sends POST /auth/logout (optional server notification)
2. Client removes token from local storage
3. Token expires naturally after 24 hours

## Implementation Guidelines

### Login Endpoint Implementation
```python
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext

router = APIRouter(prefix="/auth", tags=["authentication"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=1)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserInfo

@router.post("/login", response_model=TokenResponse)
async def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Authenticate user and return JWT access token.
    
    - **username**: User's username or email
    - **password**: User's password
    
    Returns JWT token with 24-hour expiration.
    """
    
    # Find user by username or email
    user = db.query(User).filter(
        (User.username == credentials.username) | 
        (User.email == credentials.username)
    ).first()
    
    if not user or not pwd_context.verify(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": {
                    "code": "INVALID_CREDENTIALS",
                    "message": "Invalid username or password",
                    "details": {}
                }
            }
        )
    
    # Generate JWT token
    token_data = {
        "user_id": user.id,
        "username": user.username,
        "email": user.email,
        "team_id": user.team_id,
        "role": user.role,
        "exp": datetime.utcnow() + timedelta(hours=24),
        "iat": datetime.utcnow()
    }
    
    access_token = jwt.encode(token_data, SECRET_KEY, algorithm="HS256")
    
    return TokenResponse(
        access_token=access_token,
        expires_in=86400,  # 24 hours in seconds
        user=UserInfo(
            id=user.id,
            username=user.username,
            email=user.email,
            team_id=user.team_id
        )
    )
```

### Token Validation Middleware
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError

security = HTTPBearer()

class CurrentUser(BaseModel):
    user_id: int
    username: str
    email: str
    team_id: int
    role: str

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> CurrentUser:
    """
    Validate JWT token and extract user context.
    
    Used as dependency for protected endpoints.
    """
    token = credentials.credentials
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        
        # Validate required fields
        required_fields = ["user_id", "username", "email", "team_id", "role"]
        for field in required_fields:
            if field not in payload:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail={
                        "error": {
                            "code": "INVALID_TOKEN_PAYLOAD",
                            "message": "Token missing required fields",
                            "details": {"missing_field": field}
                        }
                    }
                )
        
        return CurrentUser(
            user_id=payload["user_id"],
            username=payload["username"],
            email=payload["email"],
            team_id=payload["team_id"],
            role=payload["role"]
        )
        
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": {
                    "code": "TOKEN_EXPIRED",
                    "message": "Authentication token has expired",
                    "details": {"suggestion": "Please log in again"}
                }
            }
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": {
                    "code": "INVALID_TOKEN",
                    "message": "Invalid authentication token",
                    "details": {}
                }
            }
        )
```

### Protected Endpoint Usage
```python
@router.get("/profile", response_model=UserProfile)
async def get_user_profile(
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's profile information."""
    user = db.query(User).filter(User.id == current_user.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserProfile.from_orm(user)

@router.get("/tasks")
async def list_user_tasks(
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List tasks for authenticated user's team."""
    tasks = db.query(Task).filter(
        Task.team_id == current_user.team_id
    ).all()
    
    return [TaskResponse.from_orm(task) for task in tasks]
```

## Authentication Error Scenarios

### Invalid Credentials Response
```json
{
  "error": {
    "code": "INVALID_CREDENTIALS",
    "message": "Invalid username or password",
    "details": {}
  },
  "meta": {
    "timestamp": "2025-01-15T10:30:00Z",
    "request_id": "req-12345",
    "api_version": "1.0"
  }
}
```

### Expired Token Response
```json
{
  "error": {
    "code": "TOKEN_EXPIRED",
    "message": "Authentication token has expired",
    "details": {
      "suggestion": "Please log in again"
    }
  },
  "meta": {
    "timestamp": "2025-01-15T10:30:00Z",
    "request_id": "req-67890",
    "api_version": "1.0"
  }
}
```

### Missing Authorization Header
```json
{
  "error": {
    "code": "AUTHENTICATION_REQUIRED",
    "message": "Authentication credentials required",
    "details": {
      "header": "Authorization: Bearer <token>"
    }
  },
  "meta": {
    "timestamp": "2025-01-15T10:30:00Z",
    "request_id": "req-11111",
    "api_version": "1.0"
  }
}
```

## Security Considerations

### Password Verification
- Use constant-time comparison to prevent timing attacks
- Log failed authentication attempts for monitoring
- Implement rate limiting on login endpoint (future enhancement)
- Never log passwords or password hashes

### Token Security
- Use strong, random secret key for JWT signing
- Include expiration time in all tokens
- Validate token signature and expiration on every request
- Consider token refresh mechanism for longer sessions

### Error Response Security
- Generic error messages for authentication failures
- No indication of whether username exists
- Log authentication failures with request details
- Consistent response times for valid/invalid credentials

## AI Assistant Context

```yaml
ai_context:
  jwt_implementation: |
    Implement JWT authentication using these patterns:
    - Use PyJWT library for token generation and validation
    - Include user_id, username, email, team_id, role in token payload
    - Set expiration to 24 hours from generation time
    - Use HS256 algorithm with strong secret key from environment
    
  password_security: |
    Handle passwords securely:
    - Use passlib CryptContext with bcrypt scheme
    - Verify passwords using context.verify() method
    - Never store or log plaintext passwords
    - Use constant-time comparison for security
    
  fastapi_integration: |
    Integrate with FastAPI authentication:
    - Use HTTPBearer security scheme for automatic OpenAPI documentation
    - Create dependency function for token validation
    - Handle JWT exceptions and convert to appropriate HTTP responses
    - Include security scheme in endpoint documentation
    
  error_handling_integration: |
    Follow error handling strategy:
    - Return 401 for invalid credentials or expired tokens
    - Use structured error responses with specific error codes
    - Provide actionable error messages without security details
    - Include request tracking for debugging
    
  performance_optimization: |
    Optimize authentication performance:
    - Cache JWT secret key (don't read from file repeatedly)
    - Use efficient database queries for user lookup
    - Implement connection pooling for database access
    - Consider token validation caching for high traffic
```

### Environment Configuration
```python
import os
from typing import Optional

class AuthConfig:
    SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_HOURS: int = 24
    
    @classmethod
    def validate_config(cls):
        if cls.SECRET_KEY == "your-secret-key-here":
            raise ValueError("JWT_SECRET_KEY environment variable must be set")
        if len(cls.SECRET_KEY) < 32:
            raise ValueError("JWT_SECRET_KEY must be at least 32 characters")

# Validate configuration on startup
AuthConfig.validate_config()
```

## Testing Guidelines

### Unit Tests for Authentication
```python
import pytest
from fastapi.testclient import TestClient
import jwt
from datetime import datetime, timedelta

def test_login_success(client: TestClient, test_user):
    """Test successful login with valid credentials"""
    response = client.post("/auth/login", json={
        "username": test_user.username,
        "password": "test_password"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["expires_in"] == 86400

def test_login_invalid_credentials(client: TestClient):
    """Test login with invalid credentials"""
    response = client.post("/auth/login", json={
        "username": "invalid",
        "password": "invalid"
    })
    
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "INVALID_CREDENTIALS"

def test_protected_endpoint_without_token(client: TestClient):
    """Test accessing protected endpoint without token"""
    response = client.get("/tasks")
    assert response.status_code == 401

def test_protected_endpoint_with_valid_token(client: TestClient, auth_headers):
    """Test accessing protected endpoint with valid token"""
    response = client.get("/tasks", headers=auth_headers)
    assert response.status_code == 200
```

## Performance Requirements

### Authentication Performance Targets
- **Login Endpoint**: < 100ms for valid credentials
- **Token Validation**: < 10ms per request
- **Password Verification**: < 50ms using bcrypt
- **JWT Generation**: < 5ms per token

### Scalability Considerations
- Support 10+ concurrent authentication requests
- Handle 100+ token validations per minute
- Maintain performance with team size up to 10 users
- Plan for stateless horizontal scaling

## Compliance Rules

### Security Standards
- All authentication endpoints must use HTTPS in production
- Password verification must use bcrypt with minimum 12 rounds
- JWT tokens must include expiration times
- Failed authentication attempts must be logged

### Implementation Standards
- Authentication logic must be centralized and reusable
- Error responses must follow EDR-002 structured format
- Token validation must be consistent across all protected endpoints
- All authentication functions must include comprehensive tests

## References

- **Constraining Decisions**: [EDR-001: Authentication Strategy](../../tdr/system-level/edr-001-authentication-strategy.md), [EDR-002: Error Handling](../../tdr/system-level/edr-002-error-handling-strategy.md)
- **Component**: User Management
- **JWT Library**: https://pyjwt.readthedocs.io/
- **FastAPI Security**: https://fastapi.tiangolo.com/tutorial/security/

---

**Decision Authority**: Feature Owner  
**Implementation Impact**: All authentication and authorization implementations  
**Review Date**: February 1, 2025
