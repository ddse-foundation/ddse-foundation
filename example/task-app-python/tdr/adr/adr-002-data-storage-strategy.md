// Architectural Decision: Data Storage Strategy
// Copied from task-app-tdr-only/tdr/adr/adr-002-data-storage-strategy.md
// See original for full context and rationale.

---
type: ADR
id: adr-002
title: Data Storage Strategy
status: Accepted
date: 2025-01-15
decision_owner: Solution Architect
reviewers: [Technical Lead, Senior Developer]
related_decisions: [mdd-001, adr-001]
depends_on: [mdd-001]
supersedes: []
superseded_by: []
---

# ADR-002: Data Storage Strategy

## Status
**Accepted** - January 15, 2025

## Context

TaskFlow requires a data storage solution that aligns with the product strategy (MDD-001) and REST API architecture (ADR-001). The storage strategy must support:

- Rapid development and deployment (2-3 day constraint)
- Zero configuration setup for development and deployment
- Support for 10 concurrent users initially
- Simple backup and maintenance procedures
- Standard SQL patterns for data integrity

### Data Requirements
- **User Management**: User accounts, authentication, team membership
- **Task Management**: Task CRUD operations, assignments, status tracking
- **Relationship Management**: User-task assignments, team relationships
- **Data Volume**: Estimated 1,000 tasks maximum per team initially

### Operational Constraints
- **Infrastructure**: Standard web hosting environment
- **Maintenance**: Minimal database administration overhead
- **Backup**: Simple file-based backup strategy
- **Scaling**: Plan for growth beyond initial 10-user limit

## Decision

**We will use SQLite as the primary database with SQLAlchemy ORM for data access, providing a simple normalized schema that supports all TaskFlow functionality.**

### Technology Stack Choices

1. **SQLite Database**
   - File-based storage requiring no separate server
   - ACID compliance for data integrity
   - Zero configuration deployment
   - Built into Python standard library

2. **SQLAlchemy ORM**
   - Database-agnostic abstraction layer
   - Automatic migration support
   - Type safety and validation
   - Familiar patterns for Python developers

3. **Database Schema Design**
   - Normalized relational design
   - Foreign key constraints for referential integrity
   - Indexed fields for performance
   - Timestamps for audit trails

### Alternatives Considered

1. **PostgreSQL**
   - **Pros**: Advanced features, better concurrency, production-ready
   - **Cons**: Requires separate server, configuration overhead, deployment complexity
   - **Rejected**: Violates zero-configuration requirement from MDD-001

2. **NoSQL (MongoDB, DynamoDB)**
   - **Pros**: Schema flexibility, horizontal scaling
   - **Cons**: Learning curve, deployment complexity, over-engineering for simple use case
   - **Rejected**: Unnecessary complexity for structured data

3. **In-Memory Storage**
   - **Pros**: Maximum performance, simple implementation
   - **Cons**: Data loss on restart, no persistence
   - **Rejected**: Data persistence is essential requirement

## Database Schema

### Tables and Relationships
```sql
-- Users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(32) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    team_id INTEGER REFERENCES teams(id),
    is_active BOOLEAN DEFAULT TRUE
);

-- Teams table
CREATE TABLE teams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(32) UNIQUE NOT NULL
);

-- Tasks table
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(128) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'todo',
    owner_id INTEGER NOT NULL REFERENCES users(id),
    team_id INTEGER NOT NULL REFERENCES teams(id),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Indexes for Performance
```sql
CREATE INDEX idx_tasks_team_id ON tasks(team_id);
CREATE INDEX idx_tasks_owner_id ON tasks(owner_id);
CREATE INDEX idx_users_team_id ON users(team_id);
CREATE INDEX idx_users_username ON users(username);
```

## Migration Strategy

### Initial Setup
- SQLAlchemy will auto-create tables on first run
- No manual migration scripts needed for MVP
- Database file created automatically in project directory

### Future Migrations
- Use Alembic for schema evolution when needed
- Version control migration scripts
- Support for production database upgrades

## Backup and Recovery

### Backup Strategy
- **Development**: Copy SQLite file
- **Production**: Automated file-based backups
- **Frequency**: Daily backups with 7-day retention
- **Testing**: Regular backup restoration tests

### Recovery Procedures
- Simple file replacement for restoration
- Point-in-time recovery through backup files
- Data export capabilities for migration

## Performance Considerations

### Optimization Techniques
- Proper indexing on foreign keys and search fields
- Connection pooling through SQLAlchemy
- Query optimization through ORM best practices
- Pagination for large result sets

### Scaling Limitations
- **Concurrent Users**: ~10 users with SQLite WAL mode
- **Data Volume**: Efficient up to ~1M records
- **Read Performance**: Excellent for small datasets
- **Write Performance**: Limited by SQLite transaction model

## Consequences

### Positive
- **Zero Configuration**: No database server setup required
- **Simple Deployment**: Single file database, easy to backup/restore
- **Development Speed**: Familiar SQL patterns, ORM abstraction
- **Data Integrity**: ACID compliance, foreign key constraints
- **Cost Effective**: No database licensing or hosting costs

### Negative
- **Concurrency Limits**: Not suitable for high-concurrency applications
- **Scaling Constraints**: Difficult to scale beyond single server
- **Limited Features**: Missing advanced database features
- **Backup Simplicity**: File-based backups may not suit all scenarios

### Risks
- **Data Loss**: Single file vulnerability (mitigated by backups)
- **Performance Degradation**: May slow with large datasets
- **Migration Complexity**: Future database changes may require data migration

## Implementation Guidelines

### Development Standards
- Use SQLAlchemy models for all database access
- Implement proper foreign key relationships
- Add appropriate indexes for query performance
- Include timestamps on all entities

### Security Considerations
- Encrypt sensitive data at application layer
- Use parameterized queries (automatic with ORM)
- Implement proper access controls
- Regular security updates for dependencies

### Monitoring and Maintenance
- Monitor database file size growth
- Track query performance metrics
- Implement automated backup verification
- Plan migration path for scaling needs

## Success Metrics
- **Deployment Time**: Database setup in under 1 minute
- **Query Performance**: 95% of queries under 50ms
- **Data Integrity**: Zero data corruption incidents
- **Backup Reliability**: 100% successful backup restoration tests

## Future Considerations
- Migration to PostgreSQL when user count exceeds 50
- Implementation of read replicas for performance
- Advanced backup strategies for production use
- Database monitoring and alerting systems
