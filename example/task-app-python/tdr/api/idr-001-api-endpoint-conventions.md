// Implementation Decision: API Endpoint Conventions
// Copied from task-app-tdr-only/components/task-management/tdr/idr-001-api-endpoint-conventions.md
// See original for full context and rationale.

---
type: IDR
id: idr-001
title: API Endpoint Conventions
status: Accepted
date: 2025-01-15
decision_owner: Lead Developer
reviewers: [Solution Architect]
related_decisions: [adr-001]
depends_on: [adr-001]
supersedes: []
superseded_by: []
---

# IDR-001: API Endpoint Conventions

## Status
**Accepted** - January 15, 2025

## Context

TaskFlow requires consistent, predictable API endpoint conventions to support RESTful design and ease of use for client developers. This decision defines the naming, structure, and versioning of API endpoints following ADR-001 REST API architecture.

## Decision

**We will use standard RESTful conventions with resource-based URLs, appropriate HTTP verbs, and consistent response patterns across all API endpoints.**

### URL Structure Standards

1. **Resource Naming**
   - Use plural nouns for resource collections (`/tasks`, `/users`, `/teams`)
   - Use lowercase with hyphens for multi-word resources
   - Avoid verbs in URLs (actions expressed through HTTP methods)

2. **Path Parameters**
   - Use curly braces for path variables (`/tasks/{task_id}`)
   - Use descriptive parameter names (`{task_id}` not `{id}`)
   - Numeric IDs for primary resource identifiers

3. **Query Parameters**
   - Use for filtering, pagination, and optional parameters
   - Examples: `?skip=0&limit=100`, `?status=todo`

### HTTP Verb Usage

| Verb   | Purpose | URL Pattern | Response |
|--------|---------|-------------|----------|
| GET    | Retrieve resource(s) | `/tasks`, `/tasks/{id}` | 200 + data |
| POST   | Create new resource | `/tasks` | 201 + created data |
| PUT    | Update existing resource | `/tasks/{id}` | 200 + updated data |
| DELETE | Remove resource | `/tasks/{id}` | 204 (no content) |

### Complete API Endpoint Specification

#### Authentication Endpoints
```
POST /auth/register     - User registration
POST /auth/token        - User login (OAuth2 compatible)
GET  /auth/me          - Current user profile
```

#### Task Management Endpoints
```
GET    /tasks          - List tasks (team-filtered)
POST   /tasks          - Create new task
GET    /tasks/{id}     - Get specific task
PUT    /tasks/{id}     - Update task
DELETE /tasks/{id}     - Delete task
```

#### Team Management Endpoints
```
GET    /teams          - List available teams
POST   /teams          - Create new team
GET    /teams/{id}     - Get team details
POST   /teams/{id}/join - Join existing team
```

#### System Endpoints
```
GET    /health         - Health check
GET    /               - Redirect to /docs
GET    /docs           - OpenAPI documentation
GET    /redoc          - Alternative documentation
```

### Response Format Standards

#### Success Response Structure
```json
{
  "id": 123,
  "field1": "value",
  "field2": "value",
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-15T10:30:00Z"
}
```

#### List Response Structure
```json
[
  {"id": 1, "title": "Task 1"},
  {"id": 2, "title": "Task 2"}
]
```

#### Error Response Structure (per EDR-002)
```json
{
  "detail": "Error description",
  "type": "error_type",
  "path": "/api/path"
}
```

### Pagination Standards

#### Query Parameters
- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum records to return (default: 100, max: 1000)

#### Example Usage
```
GET /tasks?skip=20&limit=10
```

### Filtering and Search

#### Simple Filtering
```
GET /tasks?status=todo
GET /tasks?owner_id=123
```

#### Future Extensions
- Full-text search: `?search=keyword`
- Date ranges: `?created_after=2025-01-01`
- Multiple values: `?status=todo,in_progress`

## Implementation Requirements

### FastAPI Implementation
```python
@router.get("/tasks", response_model=List[schemas.TaskOut])
def read_tasks(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Implementation follows team-based access control
    return db.query(models.Task)\
        .filter(models.Task.team_id == current_user.team_id)\
        .offset(skip)\
        .limit(limit)\
        .all()
```

### Path Parameter Validation
- All path parameters must be validated
- Numeric IDs must be positive integers
- Return 404 for non-existent resources
- Return 403 for access denied scenarios

### Query Parameter Validation
- Validate `skip` >= 0
- Validate `limit` between 1 and 1000
- Ignore unknown query parameters
- Return 422 for invalid parameter values

## Security Considerations

### Authentication Requirements
- All endpoints except `/health` and `/docs` require authentication
- Use JWT Bearer token authentication
- Return 401 for missing/invalid tokens

### Authorization Patterns
- Team-based access control for all data endpoints
- Users can only access resources within their team
- Public endpoints: `/teams` (list), `/health`, `/docs`

### Rate Limiting (Future)
- Consider rate limiting by user/IP
- Protect authentication endpoints especially
- Different limits for different endpoint types

## Documentation Requirements

### OpenAPI Specification
- All endpoints must have complete OpenAPI documentation
- Include request/response schemas
- Document all possible HTTP status codes
- Provide example requests and responses

### Endpoint Documentation Template
```python
@router.post("/tasks", response_model=schemas.TaskOut, status_code=201)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Create a new task.
    
    - **title**: Task title (required, 1-128 chars)
    - **description**: Task description (optional)
    - **status**: Task status (default: 'todo')
    
    Returns the created task with assigned ID and timestamps.
    Requires team membership to create tasks.
    """
```

## Testing Requirements

### Endpoint Testing
- Test all HTTP methods for each endpoint
- Verify correct status codes
- Test authentication/authorization
- Test input validation
- Test error scenarios

### Integration Testing
- Test complete user workflows
- Test team-based access control
- Test pagination functionality
- Test error handling consistency

## Monitoring and Analytics

### Endpoint Metrics
- Request count by endpoint
- Response time by endpoint
- Error rate by endpoint
- Most frequently used endpoints

### Usage Patterns
- Popular query parameters
- Pagination usage patterns
- Authentication success rates
- Team access patterns

## Consequences

### Positive
- **Predictable API**: Consistent patterns across all endpoints
- **Developer Experience**: Easy to learn and use
- **Tool Compatibility**: Works with standard REST tools
- **Documentation**: Auto-generated OpenAPI documentation
- **Testing**: Consistent patterns simplify testing

### Negative
- **Rigidity**: Must follow conventions even when suboptimal
- **Verbosity**: Some operations require multiple API calls
- **Over-fetching**: May return more data than needed

## Future Considerations

### API Versioning
- Consider URL-based versioning (`/v1/tasks`) if breaking changes needed
- Header-based versioning as alternative
- Maintain backward compatibility when possible

### Performance Optimizations
- Add caching headers for appropriate endpoints
- Consider response compression
- Implement field selection (`?fields=id,title`)

### Advanced Features
- Bulk operations for efficiency
- Webhook support for real-time updates
- GraphQL endpoint as alternative to REST

## Compliance Checklist
- [ ] All endpoints follow RESTful conventions
- [ ] Consistent error handling across endpoints
- [ ] Complete OpenAPI documentation
- [ ] Authentication/authorization implemented
- [ ] Input validation on all endpoints
- [ ] Team-based access control enforced
- [ ] Comprehensive test coverage
- [ ] Performance monitoring in place
