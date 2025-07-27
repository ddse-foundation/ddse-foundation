---
type: IDR
id: idr-001
title: API Endpoint Conventions
status: Accepted
date: 2025-01-15
decision_owner: Feature Owner
reviewers: [Technical Lead, Senior Developer]
related_decisions: [adr-001, edr-002]
depends_on: [adr-001]
supersedes: []
superseded_by: []
component: task-management
---

# IDR-001: API Endpoint Conventions

## Status
**Accepted** - January 15, 2025

## Context

The task management component requires specific API endpoint implementations that follow the REST architecture (ADR-001) and error handling strategy (EDR-002). These endpoints form the core functionality of TaskFlow and must be:

- Consistent with RESTful design principles
- Easy to understand and use
- Aligned with the simplicity goals from MDD-001
- Compatible with multiple client types

### Component Scope
This IDR specifically addresses the task management endpoints:
- Task creation, retrieval, updating, and deletion
- Task filtering and querying
- Task assignment and status management
- Bulk operations for efficiency

### Technical Context
- **Framework**: FastAPI with automatic OpenAPI generation
- **Data Model**: SQLAlchemy Task model with SQLite backend
- **Authentication**: JWT token-based (from EDR-001)
- **Authorization**: Team-based access control

## Decision

**We will implement task management endpoints using standard RESTful patterns with consistent URL structure, query parameter conventions, and response formats that align with the established API architecture.**

### Endpoint Specifications

#### Core CRUD Operations
```
GET    /tasks              # List tasks with optional filtering
POST   /tasks              # Create new task
GET    /tasks/{task_id}    # Retrieve specific task
PUT    /tasks/{task_id}    # Update entire task
PATCH  /tasks/{task_id}    # Partial task update
DELETE /tasks/{task_id}    # Delete task
```

#### Query Parameters for Filtering
```
GET /tasks?status=todo,in_progress&assigned_to=123&priority=high&limit=20&offset=0
```

### URL Design Patterns

1. **Resource Collection**: `/tasks` for task collection operations
2. **Resource Instance**: `/tasks/{task_id}` for specific task operations
3. **Query Parameters**: Use query strings for filtering, pagination, and sorting
4. **Path Parameters**: Use path segments only for resource identification

## Alternatives Considered

### Alternative 1: Nested Resource URLs
- **Example**: `/users/{user_id}/tasks` for user-specific tasks
- **Pros**: Clear ownership relationship, intuitive for user-centric views
- **Cons**: Complex URL management, harder to implement team-based filtering
- **Rejection Reason**: Conflicts with team-based access model and adds URL complexity

### Alternative 2: Action-Based URLs
- **Example**: `/tasks/complete/{task_id}`, `/tasks/assign/{task_id}`
- **Pros**: Explicit action naming, clear intent
- **Cons**: Non-RESTful design, proliferation of endpoints, harder to document
- **Rejection Reason**: Violates REST principles from ADR-001

### Alternative 3: GraphQL-Style Single Endpoint
- **Example**: `/graphql` with query language
- **Pros**: Flexible querying, efficient data fetching
- **Cons**: Higher complexity, different from established REST pattern
- **Rejection Reason**: Conflicts with REST API architecture decision

## Rationale

Standard RESTful endpoints provide:

1. **Consistency**: Predictable URL patterns reduce learning curve
2. **Tooling Compatibility**: Works with standard HTTP tools and libraries
3. **Documentation**: Automatic OpenAPI generation with clear endpoint structure
4. **Client Simplicity**: Standard HTTP methods with intuitive semantics
5. **Caching**: GET requests can be cached by HTTP infrastructure

### Implementation Benefits
- **Fast Development**: Leverage FastAPI's automatic CRUD generation patterns
- **Testing**: Standard HTTP testing tools work without modification
- **Documentation**: OpenAPI specification clearly documents all endpoints
- **Client Libraries**: Standard REST clients can consume the API easily

## Implementation Guidelines

### Task List Endpoint
```python
@router.get("/tasks", response_model=List[TaskResponse])
async def list_tasks(
    status: Optional[List[TaskStatus]] = Query(None),
    assigned_to: Optional[int] = Query(None),
    priority: Optional[List[TaskPriority]] = Query(None),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve list of tasks with optional filtering.
    
    - **status**: Filter by task status (comma-separated)
    - **assigned_to**: Filter by assigned user ID
    - **priority**: Filter by priority level (comma-separated)
    - **limit**: Maximum number of tasks to return (1-100)
    - **offset**: Number of tasks to skip for pagination
    """
    query = db.query(Task).filter(Task.team_id == current_user.team_id)
    
    if status:
        query = query.filter(Task.status.in_(status))
    if assigned_to:
        query = query.filter(Task.assigned_to == assigned_to)
    if priority:
        query = query.filter(Task.priority.in_(priority))
    
    tasks = query.offset(offset).limit(limit).all()
    return [TaskResponse.from_orm(task) for task in tasks]
```

### Task Creation Endpoint
```python
@router.post("/tasks", response_model=TaskResponse, status_code=201)
async def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new task.
    
    - **title**: Task title (required, 1-200 characters)
    - **description**: Task description (optional, max 1000 characters)
    - **priority**: Task priority (low, medium, high)
    - **assigned_to**: User ID to assign task to (optional)
    - **due_date**: Due date in ISO 8601 format (optional)
    """
    task = Task(
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        assigned_to=task_data.assigned_to,
        due_date=task_data.due_date,
        created_by=current_user.id,
        team_id=current_user.team_id
    )
    
    db.add(task)
    db.commit()
    db.refresh(task)
    
    return TaskResponse.from_orm(task)
```

### Task Update Endpoint
```python
@router.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update an existing task (full replacement).
    
    - **task_id**: ID of the task to update
    - All fields in request body will replace existing values
    """
    task = get_task_or_404(db, task_id, current_user.team_id)
    
    for field, value in task_data.dict(exclude_unset=True).items():
        setattr(task, field, value)
    
    db.commit()
    db.refresh(task)
    
    return TaskResponse.from_orm(task)
```

## Query Parameter Conventions

### Filtering Parameters
- **Single Value**: `?status=todo` (exact match)
- **Multiple Values**: `?status=todo,in_progress` (comma-separated OR logic)
- **Range Values**: `?created_after=2025-01-01&created_before=2025-01-31`

### Pagination Parameters
- **limit**: Maximum number of results (default: 20, max: 100)
- **offset**: Number of results to skip (default: 0)

### Sorting Parameters
- **sort**: Field name for sorting (default: created_at)
- **order**: Sort direction (asc/desc, default: desc)

### Example Complex Query
```
GET /tasks?status=todo,in_progress&assigned_to=123&priority=high&sort=due_date&order=asc&limit=10&offset=0
```

## Response Format Standards

### Success Response Structure
```json
{
  "id": 123,
  "title": "Complete API documentation",
  "description": "Write comprehensive API documentation for TaskFlow",
  "status": "in_progress",
  "priority": "high",
  "assigned_to": 456,
  "created_by": 789,
  "due_date": "2025-01-20",
  "created_at": "2025-01-15T10:00:00Z",
  "updated_at": "2025-01-15T14:30:00Z"
}
```

### List Response with Metadata
```json
{
  "data": [
    {
      "id": 123,
      "title": "Task 1",
      // ... task fields
    }
  ],
  "meta": {
    "total": 45,
    "limit": 20,
    "offset": 0,
    "has_more": true
  }
}
```

## AI Assistant Context

```yaml
ai_context:
  endpoint_implementation: |
    Implement task management endpoints using these patterns:
    - Use FastAPI router for endpoint organization
    - Implement proper dependency injection for auth and database
    - Use Pydantic models for request/response validation
    - Include comprehensive docstrings for OpenAPI documentation
    
  query_parameter_handling: |
    Handle query parameters consistently:
    - Use Optional[] types for optional parameters
    - Set reasonable defaults and limits for pagination
    - Implement comma-separated lists for multiple values
    - Validate query parameter combinations
    
  authorization_patterns: |
    Implement team-based authorization:
    - Filter all queries by current_user.team_id
    - Verify task ownership before updates/deletes
    - Check assigned_to user is in same team
    - Return 404 for unauthorized access (don't reveal existence)
    
  error_handling_integration: |
    Follow error handling strategy from EDR-002:
    - Use appropriate HTTP status codes
    - Return structured error responses
    - Validate input using Pydantic models
    - Handle business logic errors gracefully
    
  performance_considerations: |
    Optimize for small team usage:
    - Add database indexes on frequently filtered fields
    - Limit result set sizes to prevent abuse
    - Use efficient query patterns with SQLAlchemy
    - Implement pagination for large result sets
```

### Pydantic Model Examples
```python
from pydantic import BaseModel, Field
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
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    priority: TaskPriority = TaskPriority.MEDIUM
    assigned_to: Optional[int] = None
    due_date: Optional[date] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assigned_to: Optional[int] = None
    due_date: Optional[date] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    priority: TaskPriority
    assigned_to: Optional[int]
    created_by: int
    due_date: Optional[date]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True
```

## Performance Requirements

### Response Time Targets
- **List Tasks**: < 100ms for typical queries (20 results)
- **Create Task**: < 50ms for successful creation
- **Update Task**: < 50ms for simple updates
- **Delete Task**: < 25ms for successful deletion

### Throughput Expectations
- **Read Operations**: Support 50+ requests per minute
- **Write Operations**: Support 10+ requests per minute
- **Concurrent Users**: Handle 5+ simultaneous API consumers

## Compliance Rules

### URL Design Standards
- All task endpoints must use `/tasks` base path
- Resource IDs must be integers in path parameters
- Query parameters must follow documented naming conventions
- HTTP methods must align with REST semantics

### Response Standards
- All responses must include appropriate HTTP status codes
- Success responses must use documented JSON structure
- Error responses must follow EDR-002 error format
- List endpoints must include pagination metadata

## References

- **Constraining Decisions**: [ADR-001: REST API Architecture](../../tdr/adr/adr-001-rest-api-architecture.md), [EDR-002: Error Handling](../../tdr/system-level/edr-002-error-handling-strategy.md)
- **Component**: Task Management
- **FastAPI Router Documentation**: https://fastapi.tiangolo.com/tutorial/bigger-applications/
- **OpenAPI Documentation**: Generated automatically by FastAPI

---

**Decision Authority**: Feature Owner  
**Implementation Impact**: All task management API endpoints  
**Review Date**: February 1, 2025
