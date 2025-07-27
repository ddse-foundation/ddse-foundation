# AI Implementation Guide for TaskFlow TDRs

## Overview

This guide demonstrates how to use the TaskFlow TDR collection as context for AI-assisted development. The TDRs provide comprehensive "decision memory" that enables AI tools to generate implementation that aligns with human architectural decisions.

## Using TDRs with AI Tools

### 1. Provide Decision Context

When working with AI assistants, include relevant TDR content as context:

```
Human: I need to implement the task creation endpoint for TaskFlow.

Context: Here are the relevant TDRs:
[Include content from IDR-001, IDR-002, ADR-001, EDR-002]

Please implement the endpoint following these documented decisions.
```

### 2. Reference Decision Hierarchy

Start with high-level decisions and work down:

1. **MDD-001**: Product strategy and constraints
2. **ADR-001/002**: Architectural choices
3. **EDR-001/002**: Engineering practices
4. **IDR-001/002**: Implementation patterns

### 3. Leverage AI Context Sections

Each TDR includes structured AI context in YAML format:

```yaml
ai_context:
  implementation_priority: |
    Clear guidance on what to prioritize
  framework_guidance: |
    Specific technology recommendations
  validation_requirements: |
    Rules for input validation
```

## Example AI Interaction

### Prompt Template
```
Role: You are implementing the TaskFlow API following documented technical decisions.

Context: TaskFlow is a simple task management API for small teams (2-10 people). 

Key Constraints from MDD-001:
- 2-3 day development timeline
- Single developer implementation
- Zero configuration deployment
- Essential functionality only

Architecture from ADR-001:
- RESTful API with FastAPI
- JSON request/response format
- Automatic OpenAPI documentation

Data Storage from ADR-002:
- SQLite database with SQLAlchemy ORM
- Normalized schema with foreign keys
- Connection pooling for concurrent access

Authentication from EDR-001:
- JWT tokens with 24-hour expiration
- bcrypt password hashing
- Team-based authorization

Task: Implement the task creation endpoint following IDR-001 and IDR-002 specifications.

Required Implementation:
- POST /tasks endpoint
- Pydantic model validation
- Team-based authorization
- Structured error responses per EDR-002

AI Context from IDR-001:
[Include the ai_context section from IDR-001]

AI Context from IDR-002:
[Include the ai_context section from IDR-002]

Please implement the complete endpoint with proper validation, error handling, and documentation.
```

### Expected AI Output Quality

With proper TDR context, AI should generate:

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import date

router = APIRouter(prefix="/tasks", tags=["tasks"])

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    priority: TaskPriority = TaskPriority.MEDIUM
    assigned_to: Optional[int] = None
    due_date: Optional[date] = None
    
    @validator('title')
    def title_must_not_be_whitespace(cls, v):
        if not v.strip():
            raise ValueError('Task title cannot be empty or whitespace only')
        return v.strip()
    
    @validator('due_date')
    def due_date_not_in_past(cls, v):
        if v is not None and v < date.today():
            raise ValueError('Due date cannot be in the past')
        return v

@router.post("/", response_model=TaskResponse, status_code=201)
async def create_task(
    task_data: TaskCreate,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new task for the authenticated user's team.
    
    - **title**: Task title (required, 1-200 characters)
    - **description**: Task description (optional, max 1000 characters)
    - **priority**: Task priority (low, medium, high)
    - **assigned_to**: User ID to assign task to (must be team member)
    - **due_date**: Due date in ISO 8601 format (must be future date)
    """
    
    # Validate assigned user is in same team
    if task_data.assigned_to:
        assigned_user = db.query(User).filter(
            User.id == task_data.assigned_to,
            User.team_id == current_user.team_id
        ).first()
        
        if not assigned_user:
            raise HTTPException(
                status_code=422,
                detail={
                    "error": {
                        "code": "INVALID_ASSIGNMENT",
                        "message": "Cannot assign task to user outside team",
                        "details": {
                            "field": "assigned_to",
                            "user_id": task_data.assigned_to
                        }
                    }
                }
            )
    
    # Create task
    task = Task(
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        assigned_to=task_data.assigned_to,
        due_date=task_data.due_date,
        created_by=current_user.user_id,
        team_id=current_user.team_id,
        status=TaskStatus.TODO
    )
    
    db.add(task)
    db.commit()
    db.refresh(task)
    
    return TaskResponse.from_orm(task)
```

## TDR-Guided Development Process

### Step 1: Review Decision Hierarchy
```
1. Read MDD-001 for product constraints
2. Review ADR-001/002 for architectural patterns
3. Study EDR-001/002 for engineering practices
4. Examine relevant IDRs for implementation details
```

### Step 2: Extract AI Context
```
1. Collect ai_context sections from relevant TDRs
2. Identify implementation patterns and constraints
3. Note validation requirements and error handling
4. Understand performance and security requirements
```

### Step 3: Generate Implementation
```
1. Provide TDR context to AI assistant
2. Request implementation following documented decisions
3. Validate output against TDR specifications
4. Iterate if implementation doesn't match decisions
```

### Step 4: Validate Against TDRs
```
1. Check implementation follows architectural patterns
2. Verify error handling matches EDR-002 format
3. Ensure validation follows IDR-002 specifications
4. Confirm security practices from relevant EDRs
```

## Common AI Prompts for TaskFlow

### Implementing Database Models
```
Context: Implement SQLAlchemy models following ADR-002 data storage strategy.

Key Requirements:
- SQLite with SQLAlchemy ORM
- Normalized schema with foreign keys
- Support for users and tasks tables
- Team-based data isolation

[Include relevant sections from ADR-002]

Task: Generate User and Task model classes with proper relationships and constraints.
```

### Implementing Authentication
```
Context: Implement JWT authentication following EDR-001 and IDR-003.

Key Requirements:
- JWT tokens with 24-hour expiration
- bcrypt password hashing
- FastAPI dependency injection
- Structured error responses

[Include AI context from EDR-001 and IDR-003]

Task: Generate authentication middleware and login endpoint.
```

### Implementing Validation
```
Context: Implement input validation following IDR-002 patterns.

Key Requirements:
- Pydantic model validation
- Custom business rule validators
- Structured error responses per EDR-002
- Security sanitization

[Include AI context from IDR-002]

Task: Generate validation models and custom validators for task management.
```

## Quality Indicators

### Well-Aligned AI Output Should:

1. **Follow Architectural Patterns**
   - Use FastAPI patterns from ADR-001
   - Follow SQLAlchemy patterns from ADR-002
   - Implement JWT authentication from EDR-001

2. **Include Proper Validation**
   - Use Pydantic models with Field constraints
   - Implement custom validators for business rules
   - Return structured error responses

3. **Handle Errors Correctly**
   - Return appropriate HTTP status codes
   - Use structured error format from EDR-002
   - Include actionable error messages

4. **Implement Security Measures**
   - Use bcrypt for password hashing
   - Implement team-based authorization
   - Sanitize user input

5. **Follow Performance Guidelines**
   - Use async/await patterns
   - Implement efficient database queries
   - Include appropriate indexes

## Iterating with AI

### When AI Output Doesn't Match TDRs:

1. **Provide More Specific Context**
   ```
   The implementation doesn't follow IDR-001 endpoint conventions. 
   Please revise to use the exact URL patterns and response formats specified.
   ```

2. **Reference Specific Decisions**
   ```
   According to EDR-002, error responses must include error codes and structured details.
   Please update the error handling to match this format.
   ```

3. **Include Missing Requirements**
   ```
   The validation doesn't implement the business rules from IDR-002.
   Please add validators for status transitions and user assignments.
   ```

## Benefits of TDR-Guided AI Development

### Without TDRs:
- AI generates generic CRUD patterns
- Inconsistent error handling
- Missing business rules
- No architectural alignment

### With TDRs:
- AI generates aligned implementations
- Consistent patterns across components
- Proper error handling and validation
- Security and performance considerations included

## Best Practices

1. **Always Start with MDD**: Understand product constraints first
2. **Include Multiple TDR Levels**: Provide architectural and implementation context
3. **Use Specific AI Context**: Include the structured ai_context sections
4. **Validate Against Decisions**: Check output follows documented patterns
5. **Iterate for Alignment**: Refine prompts when output doesn't match decisions

---

This guide demonstrates how DDSE methodology creates "decision memory" that makes AI-assisted development both faster and better aligned with human intentions.
