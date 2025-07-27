// Architectural Decision: REST API Architecture
// Copied from task-app-tdr-only/tdr/adr/adr-001-rest-api-architecture.md
// See original for full context and rationale.

---
type: ADR
id: adr-001
title: REST API Architecture
status: Accepted
date: 2025-01-15
decision_owner: Solution Architect
reviewers: [Technical Lead, Senior Developer]
related_decisions: [mdd-001]
depends_on: [mdd-001]
supersedes: []
superseded_by: []
---

# ADR-001: REST API Architecture

## Status
**Accepted** - January 15, 2025

## Context

TaskFlow requires an API architecture that supports the product strategy defined in MDD-001. The architecture must enable:

- Multiple client types (web, mobile, CLI)
- Rapid development within 2-3 day constraint
- Simple deployment and maintenance
- Clear, self-documenting interface

### Technical Context
- **Development Team**: Single developer with standard web development skills
- **Infrastructure Constraint**: Standard web hosting environment
- **Client Requirements**: Support for future web and mobile applications
- **Timeline Pressure**: Architecture choice must not delay implementation

### Integration Requirements
- **Frontend Flexibility**: Multiple client implementations over time
- **API Documentation**: Self-generating documentation for developer onboarding
- **Testing Strategy**: Automated testing of API endpoints
- **Development Tools**: Standard tooling compatibility

## Decision

**We will implement TaskFlow using RESTful API architecture with JSON request/response format and automatic OpenAPI documentation generation.**

### Architectural Choices

1. **RESTful Design Principles**
   - Resource-based URL structure (`/tasks`, `/users`, `/teams`)
   - HTTP verbs for operations (GET, POST, PUT, DELETE)
   - Stateless communication with JWT tokens
   - Standard HTTP status codes for responses

2. **Technology Stack**
   - **Framework**: FastAPI for Python (automatic OpenAPI generation)
   - **Data Format**: JSON for all request/response payloads
   - **Authentication**: JWT Bearer tokens
   - **Documentation**: Automatic Swagger UI and ReDoc generation

3. **API Design Standards**
   - Consistent error response format across all endpoints
   - Pagination support for list endpoints
   - Version tolerance (design for future API versioning)
   - Content negotiation support

### Alternatives Considered

1. **GraphQL API**
   - **Pros**: Flexible queries, reduced over-fetching
   - **Cons**: Increased complexity, learning curve, tooling overhead
   - **Rejected**: Violates simplicity constraint from MDD-001

2. **RPC-Style API**
   - **Pros**: Simple function-like calls
   - **Cons**: Not web-standard, poor caching, limited tooling
   - **Rejected**: Poor integration with web ecosystem

3. **SOAP/XML**
   - **Pros**: Enterprise standards, strong typing
   - **Cons**: Verbose, complex tooling, heavy overhead
   - **Rejected**: Conflicts with simplicity and speed goals

## Implementation Details

### URL Structure
```
/auth/register          POST   - User registration
/auth/token            POST   - User login
/auth/me               GET    - Current user info
/tasks                 GET    - List tasks
/tasks                 POST   - Create task
/tasks/{id}            GET    - Get task
/tasks/{id}            PUT    - Update task
/tasks/{id}            DELETE - Delete task
/teams                 GET    - List teams
/teams                 POST   - Create team
/teams/{id}            GET    - Get team
/teams/{id}/join       POST   - Join team
/health                GET    - Health check
```

### Response Format Standard
```json
{
  "id": 123,
  "title": "Task title",
  "description": "Task description",
  "status": "todo",
  "created_at": "2025-01-15T10:30:00Z"
}
```

### Error Response Format
```json
{
  "detail": "Error description",
  "type": "error_type",
  "path": "/api/path"
}
```

## Consequences

### Positive
- **Developer Familiarity**: REST is widely understood
- **Tooling Ecosystem**: Extensive tool support for REST APIs
- **Automatic Documentation**: FastAPI generates OpenAPI specs
- **Testing**: Easy to test with standard HTTP tools
- **Caching**: HTTP caching strategies work naturally
- **Scaling**: Stateless design supports horizontal scaling

### Negative
- **Over-fetching**: May retrieve more data than needed
- **Multiple Requests**: Related data requires separate API calls
- **Version Management**: Future versioning may require breaking changes

### Risks
- **API Evolution**: Changes may break existing clients
- **Performance**: N+1 query problems possible
- **Security**: Standard REST security considerations apply

## Compliance Requirements

### Development
- All endpoints must follow RESTful conventions
- Consistent error handling across all endpoints
- OpenAPI documentation must be complete and accurate
- All endpoints must have appropriate test coverage

### Operations
- API must support health checks for monitoring
- Response times must meet performance requirements (200ms)
- Error rates must be tracked and alerted on

## Success Metrics
- API documentation completeness (100% endpoint coverage)
- Response time compliance (95% under 200ms)
- Client integration success (time to first working integration)
- Developer feedback on API usability

## Implementation Notes
- Use FastAPI's automatic validation and serialization
- Implement consistent pagination for list endpoints
- Follow HTTP status code conventions strictly
- Ensure all responses include appropriate headers
