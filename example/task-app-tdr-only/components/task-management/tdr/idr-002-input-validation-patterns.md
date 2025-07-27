---
type: IDR
id: idr-002
title: Input Validation Patterns
status: Accepted
date: 2025-01-15
decision_owner: Feature Owner
reviewers: [Technical Lead, Security Advisor]
related_decisions: [adr-002, edr-002, idr-001]
depends_on: [adr-002, edr-002]
supersedes: []
superseded_by: []
component: task-management
---

# IDR-002: Input Validation Patterns

## Status
**Accepted** - January 15, 2025

## Context

The task management component requires comprehensive input validation that ensures data integrity while following the error handling strategy (EDR-002) and data storage patterns (ADR-002). Validation must:

- Prevent invalid data from entering the SQLite database
- Provide clear, actionable error messages to API consumers
- Maintain performance requirements for small team usage
- Support business rules specific to task management

### Validation Scope
This IDR covers validation for:
- Task creation and update operations
- Query parameter validation for filtering
- Business rule enforcement (status transitions, assignments)
- Data type and format validation

### Requirements
- **Data Integrity**: Ensure all data meets business requirements before storage
- **User Experience**: Provide clear validation feedback with specific field errors
- **Security**: Prevent injection attacks and malformed data processing
- **Performance**: Validation must complete within response time requirements

## Decision

**We will implement multi-layered validation using Pydantic models for type/format validation, custom validators for business rules, and database constraints for data integrity enforcement.**

### Validation Architecture

1. **Pydantic Model Validation**
   - Type checking and format validation
   - Field length and range constraints
   - Automatic error message generation

2. **Custom Business Validators**
   - Status transition validation
   - User assignment verification
   - Due date business rules

3. **Database Constraints**
   - Foreign key integrity
   - Enum value enforcement
   - NOT NULL constraints

## Validation Rules Specification

### Task Creation Validation

#### Required Fields
- **title**: 1-200 characters, cannot be empty or whitespace only
- **created_by**: Must be valid user ID (automatically set from JWT token)

#### Optional Fields with Constraints
- **description**: Maximum 1000 characters, HTML tags stripped
- **priority**: Must be 'low', 'medium', or 'high' (default: 'medium')
- **assigned_to**: Must be valid user ID in same team, or null
- **due_date**: Must be today or future date, ISO 8601 format

#### Default Values
- **status**: 'todo' for new tasks
- **priority**: 'medium' if not specified
- **created_at/updated_at**: Current timestamp

### Task Update Validation

#### Status Transition Rules
```
todo → in_progress ✓
todo → completed ✓
in_progress → completed ✓
in_progress → todo ✓
completed → todo ✓ (reopen task)
completed → in_progress ✓ (reopen task)
```

#### Field Update Constraints
- **title**: Same rules as creation (1-200 characters)
- **assigned_to**: Must be team member or null
- **due_date**: Cannot set past dates
- **status**: Must follow valid transition rules

### Query Parameter Validation

#### Filtering Parameters
- **status**: Must be valid status enum values
- **assigned_to**: Must be integer user ID
- **priority**: Must be valid priority enum values
- **limit**: Integer between 1-100 (default: 20)
- **offset**: Non-negative integer (default: 0)

## Alternatives Considered

### Alternative 1: Database-Only Validation
- **Pros**: Single validation layer, guaranteed data integrity
- **Cons**: Poor user experience, generic error messages, late failure detection
- **Rejection Reason**: Conflicts with user experience requirements from MDD-001

### Alternative 2: Frontend-Only Validation
- **Pros**: Immediate user feedback, rich UI validation
- **Cons**: No API protection, security vulnerabilities, data integrity risks
- **Rejection Reason**: Violates API-first architecture and security requirements

### Alternative 3: Manual Validation Functions
- **Pros**: Complete control, custom error messages, flexible validation logic
- **Cons**: Code duplication, maintenance overhead, inconsistent error formats
- **Rejection Reason**: Conflicts with rapid development timeline and maintainability

## Implementation Guidelines

### Pydantic Model Validation
```python
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import date, datetime
from enum import Enum

class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class TaskCreate(BaseModel):
    title: str = Field(
        ..., 
        min_length=1, 
        max_length=200,
        regex=r'^(?!\s*$).+',  # Not empty or whitespace only
        description="Task title (required, 1-200 characters)"
    )
    description: Optional[str] = Field(
        None, 
        max_length=1000,
        description="Task description (optional, max 1000 characters)"
    )
    priority: TaskPriority = Field(
        TaskPriority.MEDIUM,
        description="Task priority: low, medium, or high"
    )
    assigned_to: Optional[int] = Field(
        None,
        description="User ID to assign task to (must be team member)"
    )
    due_date: Optional[date] = Field(
        None,
        description="Due date (must be today or future)"
    )
    
    @validator('title')
    def title_must_not_be_whitespace(cls, v):
        if not v.strip():
            raise ValueError('Task title cannot be empty or whitespace only')
        return v.strip()
    
    @validator('description')
    def sanitize_description(cls, v):
        if v is None:
            return v
        # Strip HTML tags for security
        import re
        v = re.sub(r'<[^>]+>', '', v)
        return v.strip() if v.strip() else None
    
    @validator('due_date')
    def due_date_not_in_past(cls, v):
        if v is not None and v < date.today():
            raise ValueError('Due date cannot be in the past')
        return v
```

### Custom Business Validators
```python
from sqlalchemy.orm import Session
from fastapi import HTTPException

def validate_user_assignment(assigned_to: int, team_id: int, db: Session):
    """Validate that assigned user is in the same team"""
    if assigned_to is None:
        return None
    
    user = db.query(User).filter(
        User.id == assigned_to,
        User.team_id == team_id
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=422,
            detail={
                "error": {
                    "code": "INVALID_ASSIGNMENT",
                    "message": "Cannot assign task to user outside team",
                    "details": {
                        "field": "assigned_to",
                        "user_id": assigned_to,
                        "team_id": team_id
                    }
                }
            }
        )
    return assigned_to

def validate_status_transition(current_status: str, new_status: str):
    """Validate task status transitions"""
    # All transitions are valid in TaskFlow for simplicity
    # This validator exists for future business rule enforcement
    valid_transitions = {
        'todo': ['in_progress', 'completed'],
        'in_progress': ['todo', 'completed'],
        'completed': ['todo', 'in_progress']
    }
    
    if new_status not in valid_transitions.get(current_status, []):
        raise HTTPException(
            status_code=422,
            detail={
                "error": {
                    "code": "INVALID_STATUS_TRANSITION",
                    "message": f"Cannot transition from {current_status} to {new_status}",
                    "details": {
                        "current_status": current_status,
                        "requested_status": new_status,
                        "valid_transitions": valid_transitions[current_status]
                    }
                }
            }
        )
```

### Validation Integration in Endpoints
```python
@router.post("/tasks", response_model=TaskResponse, status_code=201)
async def create_task(
    task_data: TaskCreate,  # Automatic Pydantic validation
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Additional business validation
    if task_data.assigned_to:
        validate_user_assignment(task_data.assigned_to, current_user.team_id, db)
    
    task = Task(
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        assigned_to=task_data.assigned_to,
        due_date=task_data.due_date,
        created_by=current_user.id,
        team_id=current_user.team_id,
        status=TaskStatus.TODO
    )
    
    try:
        db.add(task)
        db.commit()
        db.refresh(task)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=422,
            detail={
                "error": {
                    "code": "DATABASE_CONSTRAINT_VIOLATION",
                    "message": "Data violates database constraints",
                    "details": {"constraint": str(e)}
                }
            }
        )
    
    return TaskResponse.from_orm(task)
```

## Error Response Examples

### Validation Error Response
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data provided",
    "details": {
      "errors": [
        {
          "field": "title",
          "message": "Task title cannot be empty or whitespace only",
          "type": "value_error.title.empty"
        },
        {
          "field": "due_date",
          "message": "Due date cannot be in the past",
          "type": "value_error.date.past"
        }
      ]
    }
  },
  "meta": {
    "timestamp": "2025-01-15T10:30:00Z",
    "request_id": "req-12345",
    "api_version": "1.0"
  }
}
```

### Business Rule Violation
```json
{
  "error": {
    "code": "INVALID_ASSIGNMENT",
    "message": "Cannot assign task to user outside team",
    "details": {
      "field": "assigned_to",
      "user_id": 456,
      "team_id": 123
    }
  },
  "meta": {
    "timestamp": "2025-01-15T10:30:00Z",
    "request_id": "req-67890",
    "api_version": "1.0"
  }
}
```

## AI Assistant Context

```yaml
ai_context:
  validation_implementation: |
    Implement validation using these patterns:
    - Use Pydantic Field() with descriptive constraints
    - Create custom validators for business rules
    - Handle database constraint violations gracefully
    - Return structured error responses following EDR-002
    
  pydantic_patterns: |
    Follow these Pydantic best practices:
    - Use Field() for validation rules and documentation
    - Implement custom validators with @validator decorator
    - Use Enum classes for controlled vocabulary
    - Set appropriate default values
    
  business_rule_validation: |
    Implement business rules consistently:
    - Validate user assignments against team membership
    - Check status transitions against business logic
    - Verify date constraints (future dates only)
    - Sanitize user input to prevent injection attacks
    
  error_handling_integration: |
    Integrate with error handling strategy:
    - Use HTTPException for business rule violations
    - Include specific error codes for different failure types
    - Provide actionable error messages
    - Include field-level error details
    
  performance_considerations: |
    Optimize validation performance:
    - Cache user team membership lookups
    - Use database constraints as final safety net
    - Minimize database queries in validation functions
    - Validate early to fail fast
```

### Database Constraint Integration
```sql
-- Ensure enum values are constrained at database level
ALTER TABLE tasks ADD CONSTRAINT check_status 
CHECK (status IN ('todo', 'in_progress', 'completed'));

ALTER TABLE tasks ADD CONSTRAINT check_priority 
CHECK (priority IN ('low', 'medium', 'high'));

-- Ensure referential integrity
ALTER TABLE tasks ADD CONSTRAINT fk_assigned_to 
FOREIGN KEY (assigned_to) REFERENCES users(id);

ALTER TABLE tasks ADD CONSTRAINT fk_created_by 
FOREIGN KEY (created_by) REFERENCES users(id);

-- Ensure logical constraints
ALTER TABLE tasks ADD CONSTRAINT check_title_not_empty 
CHECK (LENGTH(TRIM(title)) > 0);
```

## Performance Requirements

### Validation Performance Targets
- **Pydantic Validation**: < 5ms per request
- **Business Rule Validation**: < 10ms per validation check
- **Database Constraint Validation**: < 15ms for constraint violations
- **Total Validation Overhead**: < 20ms per request

### Validation Caching
- Cache team membership lookups for user assignment validation
- Cache enum value validation results
- Use database connection pooling for validation queries

## Compliance Rules

### Validation Standards
- All user input must be validated before database insertion
- Business rules must be enforced consistently across all endpoints
- Error messages must be clear and actionable
- Validation logic must be testable and well-documented

### Security Requirements
- All text input must be sanitized to prevent injection attacks
- User IDs must be validated against team membership
- File uploads (future) must include content type validation
- Rate limiting must be applied to validation-heavy endpoints

## References

- **Constraining Decisions**: [ADR-002: Data Storage](../../tdr/adr/adr-002-data-storage-strategy.md), [EDR-002: Error Handling](../../tdr/system-level/edr-002-error-handling-strategy.md)
- **Related Decisions**: [IDR-001: API Endpoint Conventions](./idr-001-api-endpoint-conventions.md)
- **Component**: Task Management
- **Pydantic Documentation**: https://pydantic-docs.helpmanual.io/usage/validators/

---

**Decision Authority**: Feature Owner  
**Implementation Impact**: All task management input validation and business rules  
**Review Date**: February 1, 2025
