---
type: IDR
id: idr-004
title: Password Security Implementation
status: Accepted
date: 2025-01-15
decision_owner: Feature Owner
reviewers: [Technical Lead, Security Advisor]
related_decisions: [edr-001, idr-003, adr-002]
depends_on: [edr-001]
supersedes: []
superseded_by: []
component: user-management
---

# IDR-004: Password Security Implementation

## Status
**Accepted** - January 15, 2025

## Context

The user management component requires secure password handling that implements the authentication strategy (EDR-001) with proper password hashing, validation, and storage. Password security must:

- Protect user credentials from database compromise
- Enforce password complexity requirements for user security
- Support secure password verification during authentication
- Enable future password reset functionality

### Security Requirements
- **Hash Storage**: Never store plaintext passwords
- **Salt Generation**: Unique salt per password for rainbow table protection
- **Verification**: Secure password verification during login
- **Complexity**: Enforce minimum password requirements

### Implementation Context
- **Hashing Algorithm**: bcrypt as specified in EDR-001
- **Database Storage**: Password hashes in users table (ADR-002)
- **Authentication Integration**: Support IDR-003 login flow
- **Performance**: Password operations within acceptable response times

## Decision

**We will implement password security using bcrypt hashing with 12 rounds, minimum complexity requirements, and secure verification patterns that protect against timing attacks and common security vulnerabilities.**

### Password Security Specifications

#### Password Requirements
- **Minimum Length**: 8 characters
- **Character Requirements**: At least one letter and one number
- **Prohibited Patterns**: No dictionary words, common passwords, or sequential patterns
- **Case Sensitivity**: Passwords are case-sensitive

#### Bcrypt Configuration
- **Rounds**: 12 (balance of security and performance)
- **Salt**: Automatically generated unique salt per password
- **Algorithm**: bcrypt (Blowfish-based)
- **Hash Length**: 60-character hash string

## Implementation Guidelines

### Password Hashing Service
```python
from passlib.context import CryptContext
import re
from typing import List, Optional

class PasswordService:
    """Service for secure password handling"""
    
    def __init__(self):
        self.pwd_context = CryptContext(
            schemes=["bcrypt"],
            deprecated="auto",
            bcrypt__rounds=12
        )
    
    def hash_password(self, password: str) -> str:
        """
        Hash a password using bcrypt with automatic salt generation.
        
        Args:
            password: Plaintext password to hash
            
        Returns:
            Bcrypt hash string (60 characters)
        """
        return self.pwd_context.hash(password)
    
    def verify_password(self, password: str, hash_string: str) -> bool:
        """
        Verify a password against its hash using constant-time comparison.
        
        Args:
            password: Plaintext password to verify
            hash_string: Stored bcrypt hash
            
        Returns:
            True if password matches, False otherwise
        """
        return self.pwd_context.verify(password, hash_string)
    
    def validate_password_strength(self, password: str) -> List[str]:
        """
        Validate password meets complexity requirements.
        
        Args:
            password: Plaintext password to validate
            
        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []
        
        if len(password) < 8:
            errors.append("Password must be at least 8 characters long")
        
        if not re.search(r'[a-zA-Z]', password):
            errors.append("Password must contain at least one letter")
        
        if not re.search(r'[0-9]', password):
            errors.append("Password must contain at least one number")
        
        # Check for common weak passwords
        weak_passwords = {
            'password', 'password123', '12345678', 'qwerty123',
            'admin123', 'welcome123', 'letmein123'
        }
        if password.lower() in weak_passwords:
            errors.append("Password is too common and easily guessed")
        
        # Check for sequential patterns
        if self._has_sequential_pattern(password):
            errors.append("Password cannot contain sequential patterns")
        
        return errors
    
    def _has_sequential_pattern(self, password: str) -> bool:
        """Check for sequential character patterns"""
        sequential_patterns = ['123', 'abc', 'qwe', '789']
        password_lower = password.lower()
        
        for pattern in sequential_patterns:
            if pattern in password_lower:
                return True
        
        return False

# Global password service instance
password_service = PasswordService()
```

### User Registration with Password Security
```python
from pydantic import BaseModel, Field, validator
from sqlalchemy.orm import Session

class UserRegistration(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., regex=r'^[^@]+@[^@]+\.[^@]+$')
    password: str = Field(..., min_length=8)
    
    @validator('password')
    def validate_password_strength(cls, v):
        errors = password_service.validate_password_strength(v)
        if errors:
            raise ValueError('; '.join(errors))
        return v
    
    @validator('username')
    def validate_username(cls, v):
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('Username can only contain letters, numbers, and underscores')
        return v

@router.post("/register", response_model=UserResponse, status_code=201)
async def register_user(
    user_data: UserRegistration,
    db: Session = Depends(get_db)
):
    """
    Register a new user with secure password handling.
    
    - **username**: Unique username (3-50 characters, alphanumeric + underscore)
    - **email**: Valid email address
    - **password**: Strong password (min 8 chars, letter + number)
    """
    
    # Check if username or email already exists
    existing_user = db.query(User).filter(
        (User.username == user_data.username) | 
        (User.email == user_data.email)
    ).first()
    
    if existing_user:
        if existing_user.username == user_data.username:
            raise HTTPException(
                status_code=422,
                detail={
                    "error": {
                        "code": "USERNAME_TAKEN",
                        "message": "Username is already taken",
                        "details": {"field": "username"}
                    }
                }
            )
        else:
            raise HTTPException(
                status_code=422,
                detail={
                    "error": {
                        "code": "EMAIL_TAKEN",
                        "message": "Email address is already registered",
                        "details": {"field": "email"}
                    }
                }
            )
    
    # Hash password before storage
    password_hash = password_service.hash_password(user_data.password)
    
    # Create new user
    user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=password_hash,
        team_id=1,  # Default team for MVP
        role='user'
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return UserResponse.from_orm(user)
```

### Secure Login Implementation
```python
@router.post("/login", response_model=TokenResponse)
async def login_user(
    credentials: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Authenticate user with secure password verification.
    
    Uses constant-time comparison to prevent timing attacks.
    """
    
    # Find user by username or email
    user = db.query(User).filter(
        (User.username == credentials.username) | 
        (User.email == credentials.username)
    ).first()
    
    # Use constant-time verification even if user not found
    # This prevents timing attacks that could reveal valid usernames
    if user:
        password_valid = password_service.verify_password(
            credentials.password, 
            user.password_hash
        )
    else:
        # Perform dummy hash verification to maintain constant time
        password_service.verify_password(
            credentials.password,
            "$2b$12$dummy.hash.to.prevent.timing.attacks.here"
        )
        password_valid = False
    
    if not user or not password_valid:
        # Generic error message to prevent username enumeration
        raise HTTPException(
            status_code=401,
            detail={
                "error": {
                    "code": "INVALID_CREDENTIALS",
                    "message": "Invalid username or password",
                    "details": {}
                }
            }
        )
    
    # Generate and return JWT token (implementation from IDR-003)
    return generate_token_response(user)
```

### Password Change Functionality
```python
class PasswordChangeRequest(BaseModel):
    current_password: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=8)
    
    @validator('new_password')
    def validate_new_password_strength(cls, v):
        errors = password_service.validate_password_strength(v)
        if errors:
            raise ValueError('; '.join(errors))
        return v

@router.put("/profile/password")
async def change_password(
    password_data: PasswordChangeRequest,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Change user's password with current password verification.
    """
    
    user = db.query(User).filter(User.id == current_user.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify current password
    if not password_service.verify_password(
        password_data.current_password, 
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail={
                "error": {
                    "code": "INVALID_CURRENT_PASSWORD",
                    "message": "Current password is incorrect",
                    "details": {"field": "current_password"}
                }
            }
        )
    
    # Check new password is different
    if password_service.verify_password(
        password_data.new_password, 
        user.password_hash
    ):
        raise HTTPException(
            status_code=422,
            detail={
                "error": {
                    "code": "PASSWORD_UNCHANGED",
                    "message": "New password must be different from current password",
                    "details": {"field": "new_password"}
                }
            }
        )
    
    # Update password
    user.password_hash = password_service.hash_password(password_data.new_password)
    user.updated_at = datetime.utcnow()
    
    db.commit()
    
    return {"message": "Password updated successfully"}
```

## Security Best Practices

### Protection Against Common Attacks

#### Timing Attack Prevention
- Use constant-time password verification
- Perform dummy operations when user not found
- Consistent response times for valid/invalid credentials

#### Rainbow Table Protection
- Unique salt generated automatically by bcrypt
- High iteration count (12 rounds) increases computation cost
- Modern bcrypt implementation with adaptive cost

#### Brute Force Protection
- Rate limiting on authentication endpoints (future enhancement)
- Account lockout after repeated failures (future enhancement)
- Password complexity requirements

### Secure Storage Patterns
```python
# Example user model with secure password storage
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)  # bcrypt hash
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    def set_password(self, password: str):
        """Set user password with secure hashing"""
        self.password_hash = password_service.hash_password(password)
    
    def verify_password(self, password: str) -> bool:
        """Verify password against stored hash"""
        return password_service.verify_password(password, self.password_hash)
```

## Error Handling Examples

### Password Validation Errors
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Password does not meet security requirements",
    "details": {
      "errors": [
        {
          "field": "password",
          "message": "Password must be at least 8 characters long",
          "type": "value_error.password.length"
        },
        {
          "field": "password",
          "message": "Password must contain at least one number",
          "type": "value_error.password.complexity"
        }
      ]
    }
  }
}
```

### Username Already Taken
```json
{
  "error": {
    "code": "USERNAME_TAKEN",
    "message": "Username is already taken",
    "details": {
      "field": "username",
      "suggestion": "Try a different username"
    }
  }
}
```

## AI Assistant Context

```yaml
ai_context:
  password_hashing: |
    Implement password security using these patterns:
    - Use passlib CryptContext with bcrypt scheme and 12 rounds
    - Always hash passwords before database storage
    - Use verify() method for password checking (constant-time)
    - Never store or log plaintext passwords
    
  validation_patterns: |
    Implement password validation consistently:
    - Check minimum length (8 characters)
    - Require at least one letter and one number
    - Reject common weak passwords
    - Validate against sequential patterns
    
  security_considerations: |
    Follow security best practices:
    - Use constant-time comparison to prevent timing attacks
    - Perform dummy operations when user not found
    - Implement generic error messages for authentication
    - Log authentication attempts without sensitive data
    
  pydantic_integration: |
    Integrate password validation with Pydantic:
    - Use Field() constraints for basic validation
    - Implement custom validators for complexity rules
    - Return descriptive error messages
    - Validate on both registration and password change
    
  database_patterns: |
    Handle password data in database:
    - Store hashes in password_hash column (255 chars)
    - Use proper column types for bcrypt output
    - Never query or log password_hash values
    - Implement secure password update patterns
```

### Environment Security Configuration
```python
import os
import secrets

class SecurityConfig:
    # Minimum bcrypt rounds for password hashing
    BCRYPT_ROUNDS: int = int(os.getenv("BCRYPT_ROUNDS", "12"))
    
    # Password complexity settings
    MIN_PASSWORD_LENGTH: int = 8
    REQUIRE_LETTER: bool = True
    REQUIRE_NUMBER: bool = True
    
    # Rate limiting settings (future implementation)
    MAX_LOGIN_ATTEMPTS: int = 5
    LOCKOUT_DURATION_MINUTES: int = 15
    
    @classmethod
    def validate_config(cls):
        if cls.BCRYPT_ROUNDS < 10:
            raise ValueError("BCRYPT_ROUNDS must be at least 10 for security")
        if cls.MIN_PASSWORD_LENGTH < 8:
            raise ValueError("MIN_PASSWORD_LENGTH must be at least 8")

# Validate security configuration on startup
SecurityConfig.validate_config()
```

## Performance Considerations

### Bcrypt Performance
- **12 rounds**: ~100-200ms per hash operation
- **Verification**: ~50-100ms per password check
- **Memory usage**: Minimal impact on application memory
- **CPU usage**: Intentionally CPU-intensive for security

### Optimization Strategies
- Use async/await for password operations
- Consider background processing for bulk operations
- Monitor password operation performance
- Plan for rate limiting to prevent abuse

## Testing Guidelines

### Password Security Tests
```python
def test_password_hashing():
    """Test password hashing generates different hashes"""
    password = "test_password123"
    hash1 = password_service.hash_password(password)
    hash2 = password_service.hash_password(password)
    
    assert hash1 != hash2  # Different salts
    assert password_service.verify_password(password, hash1)
    assert password_service.verify_password(password, hash2)

def test_password_validation():
    """Test password complexity requirements"""
    weak_passwords = [
        "short",           # Too short
        "onlyletters",     # No numbers
        "12345678",        # No letters
        "password123"      # Common password
    ]
    
    for weak_password in weak_passwords:
        errors = password_service.validate_password_strength(weak_password)
        assert len(errors) > 0

def test_timing_attack_resistance():
    """Test login timing is consistent for valid/invalid users"""
    import time
    
    # Time login attempts for existing and non-existing users
    start_time = time.time()
    # Login with valid username, invalid password
    valid_user_time = time.time() - start_time
    
    start_time = time.time()
    # Login with invalid username
    invalid_user_time = time.time() - start_time
    
    # Times should be similar (within reasonable margin)
    time_difference = abs(valid_user_time - invalid_user_time)
    assert time_difference < 0.1  # Less than 100ms difference
```

## Compliance Rules

### Security Standards
- All passwords must be hashed using bcrypt with minimum 12 rounds
- Password complexity requirements must be enforced at validation
- Timing attack protection must be implemented in authentication
- Password hashes must never be logged or exposed in responses

### Code Standards
- Password handling must be centralized in PasswordService
- All password operations must use the password service
- Raw password strings must not be stored in variables longer than necessary
- Database queries must not include password_hash in SELECT statements

## References

- **Constraining Decisions**: [EDR-001: Authentication Strategy](../../tdr/system-level/edr-001-authentication-strategy.md)
- **Related Decisions**: [IDR-003: User Authentication Flow](./idr-003-user-authentication-flow.md), [ADR-002: Data Storage](../../tdr/adr/adr-002-data-storage-strategy.md)
- **Component**: User Management
- **Passlib Documentation**: https://passlib.readthedocs.io/
- **bcrypt Information**: https://en.wikipedia.org/wiki/Bcrypt

---

**Decision Authority**: Feature Owner  
**Implementation Impact**: All password handling and user registration implementations  
**Review Date**: February 1, 2025
