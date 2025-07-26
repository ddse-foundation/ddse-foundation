# DDSE TDR Templates

This directory contains standardized templates for all Technical Decision Record (TDR) types in the Decision-Driven Software Engineering (DDSE) methodology. These templates are designed to be fully compliant with the DDSE specification and compatible with automated validation tools.

## Template Overview

### TDR Type Hierarchy

```
MDD (Major Design Decision)
├── ADR (Architectural Decision Record)
│   ├── EDR (Engineering Decision Record)
│   └── IDR (Implementation Decision Record)
└── TDM (Trade-off Decision Matrix)
```

## Available Templates

| Template | Purpose | Authority Level | Typical Scope |
|----------|---------|----------------|---------------|
| **mdd-template.md** | Strategic/portfolio decisions | CTO, Product Owner | System-wide, multi-year |
| **adr-template.md** | Architecture decisions | Solution Architect | Application/service level |
| **edr-template.md** | Engineering practices | Technical Lead | Team/project level |
| **idr-template.md** | Implementation choices | Feature Owner | Component/feature level |
| **tdm-template.md** | Quantitative analysis | Decision Owner | Supporting analysis |

## Template Features

### Compliance with DDSE Specification

All templates include:

- ✅ **YAML Frontmatter**: Structured metadata for automated parsing
- ✅ **Required Sections**: All mandatory sections per DDSE spec
- ✅ **AI Assistant Context**: Structured AI integration support
- ✅ **Cross-References**: Proper reference management
- ✅ **Type-Specific Sections**: Requirements for each TDR type
- ✅ **Validation Ready**: Compatible with `tdr_validator.py`

### Template Structure

Each template follows this consistent structure:

1. **YAML Frontmatter** - Machine-readable metadata
2. **Title & Metadata** - Human-readable header information
3. **Context** - Background and problem description
4. **Decision** - Clear statement of the decision
5. **Alternatives** - Options that were considered
6. **Rationale** - Why this option was chosen
7. **Consequences** - Implications and impacts
8. **Type-Specific Section** - Required section for each TDR type
9. **AI Assistant Context** - Structured AI integration data
10. **References** - Cross-references to other TDRs

## How to Use Templates

### 1. Choose the Right Template

- **MDD**: For strategic technology decisions (cloud vs on-premise, build vs buy)
- **ADR**: For architectural patterns (microservices, database choices, integration)
- **EDR**: For development practices (CI/CD, testing strategy, code standards)
- **IDR**: For implementation details (algorithms, libraries, specific patterns)
- **TDM**: For quantitative analysis supporting any of the above

### 2. Copy and Customize

```bash
# Copy template to your project
cp mdd-template.md ../your-project/tdr/mdd/mdd-001-cloud-strategy.md
```

### 3. Fill Required Fields

**Essential Fields to Update:**
- Replace `XXX` in `tdr_id` with actual sequence number
- Update all `[Placeholder]` values
- Set proper `status`, `date`, `decision_owner`, and `reviewers`
- Fill all required sections completely

### 4. Validate Before Committing

```bash
# Validate single file
python3 ../tools/tdr_validator.py --file mdd-001-cloud-strategy.md

# Validate entire project
python3 ../tools/tdr_validator.py --project ../your-project
```

## Template Guidelines

### Naming Conventions

Follow this pattern: `{type}-{sequence}-{short-title}.md`

**Examples:**
- `mdd-001-cloud-native-strategy.md`
- `adr-003-microservices-architecture.md`
- `edr-005-cicd-pipeline.md`
- `idr-012-user-authentication.md`
- `tdm-001-database-comparison.md`

### Sequence Management

- **MDD**: Global sequence across organization
- **ADR**: Global sequence within product/application
- **EDR**: Sequence within team/component scope
- **IDR**: Sequence within component/feature scope
- **TDM**: Sequence within analysis scope

### Status Values

Use only these valid status values:
- `Proposed` - Decision under consideration
- `Accepted` - Decision approved and active
- `Superseded` - Replaced by newer decision
- `Deprecated` - No longer recommended

### Cross-Reference Format

Reference other TDRs using their IDs:
```markdown
**Supersedes**: mdd-001, adr-002
**Related**: adr-004, edr-003
**Depends On**: mdd-001
```

## AI Assistant Integration

### Required AI Context Fields

Each template includes an "AI Assistant Context" section with these required fields:

- **Decision Summary**: One-sentence decision summary
- **Key Constraints**: Comma-separated constraints
- **Required Patterns**: Patterns to follow
- **Anti-patterns**: Patterns to avoid
- **Verification Commands**: Automated checks

### Example AI Context

```markdown
## AI Assistant Context

**Decision Summary**: Use microservices architecture with domain-driven design boundaries  
**Key Constraints**: Team size 8 people, 6-month timeline, cloud-native deployment  
**Required Patterns**: Domain boundaries, API-first design, independent deployments  
**Anti-patterns**: Shared databases, synchronous coupling, distributed transactions  
**Verification Commands**: architecture-check, service-boundary-lint, api-compliance  
```

## Integration with Project Management

### Jira/Azure Boards Integration

Link TDRs to user stories and tasks:

```markdown
**Epic**: User Authentication System
**Related TDRs**: 
- [ADR-003: Authentication Architecture](./tdr/adr/adr-003-auth.md)
- [EDR-005: OAuth Implementation](./src/auth/tdr/edr-005-oauth.md)
```

### Pull Request Integration

Reference TDRs in commit messages:
```
feat: implement user authentication (ADR-003, EDR-005)

Implements OAuth2 authentication following architectural 
decisions in ADR-003 and engineering practices in EDR-005.
```

## Validation and Quality

### Automated Validation

The templates are designed to work with `tdr_validator.py`:

```bash
# Check template compliance
python3 ../tools/tdr_validator.py --file your-tdr.md

# Validate cross-references
python3 ../tools/tdr_validator.py --project ./

# JSON output for CI/CD
python3 ../tools/tdr_validator.py --project ./ --output json
```

### Quality Checklist

Before finalizing any TDR:

- [ ] All sections are complete
- [ ] Decision is clearly stated
- [ ] Alternatives are documented
- [ ] AI Context is properly filled
- [ ] Cross-references are valid
- [ ] File naming follows convention
- [ ] YAML frontmatter is valid
- [ ] Template validation passes

## Directory Structure Examples

### Distributed TDR Structure (Recommended)
```
project/
├── tdr/
│   ├── mdd/
│   │   └── mdd-001-cloud-strategy.md
│   └── adr/
│       └── adr-001-microservices.md
└── src/
    └── user-service/
        ├── tdr/
        │   ├── edr-001-testing.md
        │   └── idr-001-validation.md
        └── code/
```

### Centralized TDR Structure
```
project/
├── tdr/
│   ├── mdd/
│   ├── adr/
│   ├── user-service/
│   │   ├── edr/
│   │   └── idr/
│   └── payment-service/
│       ├── edr/
│       └── idr/
└── src/
```

## Support and Updates

### Getting Help

- **Validation Issues**: Check with `tdr_validator.py --help`
- **Template Questions**: See [DDSE Specification](../specification/ddse-spec-v1.0.md)
- **Best Practices**: Review [examples](../examples/) directory

### Template Versioning

Templates follow DDSE specification version:
- **Current Version**: 1.0
- **Compatibility**: Validator checks template compliance
- **Updates**: Templates updated with specification changes

---

**Quick Start:** Copy the appropriate template, fill in the blanks, validate with `tdr_validator.py`, and commit to your project's TDR directory.
