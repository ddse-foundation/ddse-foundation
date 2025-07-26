# Decision-Driven Software Engineering (DDSE) Specification v1.0

**Document Status**: Final  
**Version**: 1.0  
**Date**: July 26, 2025  
**Maintainer**: DDSE Foundation  
**License**: MIT  

## Table of Contents

1. [Introduction](#introduction)
2. [Core Principles](#core-principles)
3. [Technical Decision Records (TDR) Framework](#technical-decision-records-tdr-framework)
4. [TDR Organization and Structure](#tdr-organization-and-structure)
5. [Integration with Development Workflows](#integration-with-development-workflows)
6. [Template Standards](#template-standards)
7. [Automation and Tooling Requirements](#automation-and-tooling-requirements)
8. [Compliance and Governance](#compliance-and-governance)
9. [Implementation Guidelines](#implementation-guidelines)
10. [Version Management](#version-management)

## 1. Introduction

### 1.1 Purpose

This specification defines the standards, practices, and organizational structures for implementing Decision-Driven Software Engineering (DDSE) methodology in software projects. DDSE establishes Technical Decision Records (TDRs) as first-class artifacts in the software development lifecycle, ensuring technical decisions are captured, maintained, and enforced throughout the development process.

### 1.2 Scope

This specification covers:
- TDR taxonomy and classification
- Organizational structure within codebases
- Integration with project management tools (Jira, Azure Boards, GitHub Issues)
- Template standards for automated parsing
- AI-assisted development integration
- Compliance and governance requirements

### 1.3 Normative Requirements

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in RFC 2119.

## 2. Core Principles

### 2.1 Decision-First Development

Every codebase implementing DDSE:
- **MUST** maintain TDRs as primary governance artifacts
- **MUST** link all user stories and tasks to relevant TDRs
- **SHOULD** create TDRs before implementation begins
- **MUST** update TDRs when decisions change

### 2.2 Single Source of Truth

- TDRs **MUST** reside within the codebase repository
- External tools (Jira, boards) **MUST** reference TDRs via links
- Narrative discussions **MAY** occur in external tools but **MUST** be preserved in structured TDR format

### 2.3 AI and Human Readable

- All TDRs **MUST** use Markdown format (.md extension)
- Templates **MUST** support automated parsing by AI tools
- Content **MUST** be structured for both human comprehension and machine processing

## 3. Technical Decision Records (TDR) Framework

### 3.1 TDR Hierarchy

The DDSE framework defines five types of Technical Decision Records, organized hierarchically:

```
MDD (Major Design Decision)
├── ADR (Architectural Decision Record)
│   ├── EDR (Engineering Decision Record)
│   └── IDR (Implementation Decision Record)
└── TDM (Trade-off Decision Matrix)
```

### 3.2 TDR Type Definitions

#### 3.2.1 Major Design Decision (MDD)
- **Scope**: System-wide strategic decisions
- **Level**: Portfolio/Product level
- **Examples**: Cloud vs On-premise, Buy vs Build, Technology stack selection
- **Authority**: Product owners, CTOs, Enterprise architects
- **Lifecycle**: Long-term (years)

#### 3.2.2 Architectural Decision Record (ADR)
- **Scope**: System architecture and cross-cutting concerns
- **Level**: Application/Service level
- **Examples**: Microservices vs Monolith, Database selection, Integration patterns
- **Authority**: Solution architects, Technical leads
- **Lifecycle**: Medium-term (months to years)

#### 3.2.3 Engineering Decision Record (EDR)
- **Scope**: Development practices and tooling
- **Level**: Team/Project level
- **Examples**: CI/CD pipeline, Testing strategy, Code standards
- **Authority**: Technical leads, Senior engineers
- **Lifecycle**: Medium-term (sprints to months)

#### 3.2.4 Implementation Decision Record (IDR)
- **Scope**: Component-specific implementation choices
- **Level**: Component/Feature level
- **Examples**: Algorithm selection, Library choices, Design patterns
- **Authority**: Feature owners, Developers
- **Lifecycle**: Short-term (sprints to months)

#### 3.2.5 Trade-off Decision Matrix (TDM)
- **Scope**: Supporting analysis for any TDR type
- **Level**: Any level
- **Examples**: Framework comparison, Performance analysis, Cost-benefit analysis
- **Authority**: Decision owner or designated analyst
- **Lifecycle**: Point-in-time analysis

### 3.3 Decision Hierarchy Rules

1. **MDD and ADR Placement**: 
   - **MUST** be placed at the highest package level
   - **SHOULD** cover multiple components or the entire system

2. **EDR and IDR Requirements**:
   - Stories and tasks **MUST** have associated EDRs or IDRs
   - **MAY** reference higher-level ADRs or MDDs
   - **MUST** be placed close to the code they govern

3. **Cross-Reference Requirements**:
   - Lower-level TDRs **MUST** reference higher-level decisions
   - TDRs **SHOULD** link to related decisions at the same level
   - Superseding relationships **MUST** be documented

## 4. TDR Organization and Structure

### 4.1 Directory Structure Options

#### 4.1.1 Recommended: Distributed TDR Structure
```
project-root/
├── tdr/
│   ├── mdd/
│   │   └── mdd-001-cloud-deployment.md
│   └── adr/
│       └── adr-001-microservices-architecture.md
├── src/
│   ├── user-service/
│   │   ├── tdr/
│   │   │   ├── edr-001-user-auth-strategy.md
│   │   │   └── idr-001-password-hashing.md
│   │   └── code/
│   └── payment-service/
│       ├── tdr/
│       │   ├── edr-001-payment-gateway.md
│       │   └── idr-001-transaction-logging.md
│       └── code/
```

#### 4.1.2 Alternative: Centralized TDR Structure
```
project-root/
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
    ├── user-service/
    └── payment-service/
```

### 4.2 Naming Conventions

#### 4.2.1 File Naming Standard
- **Format**: `{type}-{sequence}-{title}.md`
- **Examples**: 
  - `mdd-001-cloud-deployment.md`
  - `adr-005-event-driven-architecture.md`
  - `edr-003-ci-cd-pipeline.md`
  - `idr-012-user-validation.md`

#### 4.2.2 Sequence Management
- **MDD**: Global sequence across entire organization
- **ADR**: Global sequence within product/application
- **EDR**: Sequence within team/component scope
- **IDR**: Sequence within component/feature scope

### 4.3 Directory Structure Requirements

1. **TDR Directory Presence**:
   - Every package with significant decisions **MUST** have a `tdr/` directory
   - Empty `tdr/` directories **SHOULD** be avoided

2. **Mirror Principle**:
   - Centralized structure **MUST** mirror the package structure
   - Distributed structure **MUST** place TDRs adjacent to relevant code

3. **Cross-Reference Accessibility**:
   - TDRs **MUST** be easily discoverable from code
   - Related TDRs **SHOULD** be co-located when possible

## 5. Integration with Development Workflows

### 5.1 Project Management Integration

#### 5.1.1 Story and Task Association
- **User Stories** (Epic level and above):
  - **MUST** reference at least one MDD or ADR
  - **SHOULD** create new ADRs for architectural implications
  
- **Tasks and Sub-tasks**:
  - **MUST** reference at least one EDR or IDR
  - **MUST** create new EDRs/IDRs for significant implementation decisions

#### 5.1.2 External Tool Integration
```markdown
## Example Jira Story
**Story**: As a user, I want to authenticate securely
**TDR References**: 
- ADR-003: Authentication Architecture
- EDR-005: OAuth2 Implementation Strategy

**TDR Links**:
- [ADR-003](./tdr/adr/adr-003-authentication-architecture.md)
- [EDR-005](./src/auth-service/tdr/edr-005-oauth2-implementation.md)
```

#### 5.1.3 Senior Developer Narrative Input
- Seniors **MAY** write narrative-style decision discussions in project management tools
- All narrative decisions **MUST** be formalized into structured TDR format
- Template compliance **MUST** be maintained for automated parsing

### 5.2 Code Review Integration

#### 5.2.1 Pull Request Requirements
- Code changes **MUST** reference related TDRs in commit messages
- New architectural patterns **MUST** have accompanying ADR updates
- Implementation decisions **SHOULD** be documented in IDRs

#### 5.2.2 Review Checklist
```markdown
## DDSE Review Checklist
- [ ] Are all new architectural decisions documented in ADRs?
- [ ] Do implementation choices have appropriate IDRs?
- [ ] Are TDR references included in commit messages?
- [ ] Do changes comply with existing TDR guidelines?
- [ ] Are superseded TDRs properly updated?
```

## 6. Template Standards

### 6.1 Common Template Structure

All TDR types **MUST** include the following sections for automated parsing:

```yaml
metadata:
  status: [Proposed|Accepted|Superseded|Deprecated]
  date: YYYY-MM-DD
  type: [MDD|ADR|EDR|IDR|TDM]
  decision_owner: string
  reviewers: [list]
  
content:
  title: string
  context: structured_text
  decision: structured_text
  alternatives: [list]
  rationale: structured_text
  consequences: structured_text
  
automation:
  ai_context: structured_summary
  compliance_rules: [list]
  verification_methods: [list]
  
references:
  supersedes: [tdr_ids]
  superseded_by: [tdr_ids]
  related: [tdr_ids]
  depends_on: [tdr_ids]
```

### 6.2 AI Assistant Integration

#### 6.2.1 Required AI Context Section
Every TDR **MUST** include an AI Assistant Context section:

```markdown
## AI Assistant Context
**Decision Summary**: [One sentence decision summary]
**Key Constraints**: [Comma-separated constraints]
**Required Patterns**: [Patterns to follow]
**Anti-patterns**: [Patterns to avoid]
**Verification Commands**: [Automated checks]
```

#### 6.2.2 Automated Parsing Requirements
- Templates **MUST** use consistent header hierarchy
- Key information **MUST** be extractable via regex patterns
- Structured data **SHOULD** be in YAML frontmatter when possible

### 6.3 Template Compliance

#### 6.3.1 Mandatory Sections
All TDRs **MUST** include:
- Status and metadata
- Title and context
- Decision statement
- Rationale
- AI Assistant Context

#### 6.3.2 Type-Specific Requirements
- **MDD**: Business impact assessment
- **ADR**: Quality attribute analysis
- **EDR**: Process integration details
- **IDR**: Implementation guidelines
- **TDM**: Quantitative analysis matrix

## 7. Automation and Tooling Requirements

### 7.1 Automated Parsing

#### 7.1.1 Parser Requirements
DDSE-compliant tools **MUST**:
- Parse TDR metadata from frontmatter
- Extract decision summaries for AI context
- Validate template compliance
- Generate cross-reference maps
- Detect orphaned or conflicting decisions

#### 7.1.2 Integration APIs
```yaml
# Example TDR API Response
tdr_summary:
  id: "adr-003"
  type: "ADR"
  title: "Authentication Architecture"
  status: "Accepted"
  decision_summary: "Use OAuth2 with JWT tokens for authentication"
  constraints: ["GDPR compliance", "Multi-tenant support"]
  patterns: ["Token-based auth", "Stateless sessions"]
  anti_patterns: ["Session storage", "Basic auth"]
```

### 7.2 CI/CD Integration

#### 7.2.1 Automated Checks
Continuous integration pipelines **MUST** include:
- TDR template validation
- Cross-reference integrity checks
- Compliance rule verification
- Automated TDR generation for significant changes

#### 7.2.2 AI-Assisted Reviews
```yaml
# CI Pipeline TDR Check
stages:
  - tdr_validation:
      script: ddse-validator --check-templates
  - decision_compliance:
      script: ddse-compliance --verify-implementation
  - ai_review:
      script: ddse-ai-reviewer --check-alignment
```

### 7.3 IDE Integration

#### 7.3.1 Developer Support
IDEs **SHOULD** provide:
- TDR template generation
- Related TDR discovery
- Compliance checking
- AI context integration for code completion

## 8. Compliance and Governance

### 8.1 Decision Authority Matrix

| TDR Type | Decision Authority | Approval Required | Review Frequency |
|----------|-------------------|-------------------|-------------------|
| MDD | CTO, Product Owner | Architecture Board | Quarterly |
| ADR | Solution Architect | Tech Lead | Monthly |
| EDR | Tech Lead | Senior Developer | Sprint |
| IDR | Feature Owner | Peer Review | As Needed |

### 8.2 Compliance Monitoring

#### 8.2.1 Automated Compliance
- Implementation **MUST** follow TDR guidelines
- Deviations **MUST** be flagged in CI/CD
- AI agents **SHOULD** monitor architectural drift

#### 8.2.2 Review Processes
- TDRs **MUST** be reviewed during sprint planning
- Outdated TDRs **MUST** be updated or deprecated
- Compliance metrics **SHOULD** be tracked and reported

### 8.3 Exception Handling

#### 8.3.1 Emergency Decisions
- Critical fixes **MAY** be implemented before TDR creation
- TDR documentation **MUST** follow within 24 hours
- Emergency decisions **MUST** be reviewed in next sprint

#### 8.3.2 Technical Debt
- TDR violations **MUST** be tracked as technical debt
- Remediation plans **MUST** be documented
- Debt impact **SHOULD** be quantified

## 9. Implementation Guidelines

### 9.1 Adoption Strategy

#### 9.1.1 Incremental Rollout
1. **Phase 1**: Implement ADRs for major architectural decisions
2. **Phase 2**: Add EDRs for engineering practices
3. **Phase 3**: Introduce IDRs for implementation decisions
4. **Phase 4**: Full automation and AI integration

#### 9.1.2 Team Training
- All developers **MUST** be trained on TDR creation
- Architects **MUST** be trained on governance processes
- Tool usage **SHOULD** be demonstrated through examples

### 9.2 Migration from Existing Documentation

#### 9.2.1 Legacy Document Conversion
- Existing architectural docs **SHOULD** be converted to ADRs
- Design decisions in wikis **SHOULD** become TDRs
- Meeting notes **MAY** be mined for historical decisions

#### 9.2.2 Knowledge Preservation
- Tribal knowledge **MUST** be captured in TDRs
- Decision history **SHOULD** be reconstructed where possible
- Context **MUST** be preserved during migration

### 9.3 Quality Assurance

#### 9.3.1 TDR Quality Metrics
- Completeness score (all sections filled)
- Clarity score (readability analysis)
- Currency score (recency of updates)
- Usage score (reference frequency)

#### 9.3.2 Continuous Improvement
- TDR effectiveness **SHOULD** be measured
- Templates **MAY** be updated based on feedback
- Process refinements **SHOULD** be documented

## 10. Version Management

### 10.1 Specification Versioning

- **Major versions**: Breaking changes to template structure
- **Minor versions**: New features or recommendations
- **Patch versions**: Clarifications and corrections

### 10.2 TDR Lifecycle Management

#### 10.2.1 Status Transitions
```
Proposed → Accepted → [Superseded|Deprecated]
```

#### 10.2.2 Historical Preservation
- Superseded TDRs **MUST** be preserved
- Decision evolution **MUST** be traceable
- Archive policies **SHOULD** be defined

### 10.3 Tool Compatibility

#### 10.3.1 Version Support
- Tools **MUST** support current specification version
- Backward compatibility **SHOULD** be maintained for one major version
- Migration tools **SHOULD** be provided for version upgrades

---

## Appendices

### Appendix A: Example File Organization

```
fintech-app/
├── tdr/
│   ├── mdd/
│   │   ├── mdd-001-cloud-native-architecture.md
│   │   └── mdd-002-microservices-adoption.md
│   └── adr/
│       ├── adr-001-event-driven-architecture.md
│       ├── adr-002-database-per-service.md
│       └── adr-003-api-gateway-pattern.md
├── services/
│   ├── user-service/
│   │   ├── tdr/
│   │   │   ├── edr-001-user-authentication.md
│   │   │   ├── edr-002-data-validation.md
│   │   │   ├── idr-001-password-hashing.md
│   │   │   └── idr-002-jwt-token-structure.md
│   │   └── src/
│   ├── payment-service/
│   │   ├── tdr/
│   │   │   ├── edr-001-payment-gateway-integration.md
│   │   │   ├── idr-001-transaction-logging.md
│   │   │   └── idr-002-encryption-algorithms.md
│   │   └── src/
│   └── notification-service/
│       ├── tdr/
│       │   ├── edr-001-message-queuing.md
│       │   └── idr-001-email-templates.md
│       └── src/
└── infrastructure/
    └── tdr/
        ├── edr-001-cicd-pipeline.md
        ├── edr-002-monitoring-strategy.md
        └── edr-003-deployment-automation.md
```

### Appendix B: Integration Examples

#### B.1 Jira Integration
```markdown
## Epic: User Authentication System
**Description**: Implement secure user authentication
**TDR References**: 
- [MDD-001: Cloud Native Architecture](./tdr/mdd/mdd-001-cloud-native-architecture.md)
- [ADR-003: API Gateway Pattern](./tdr/adr/adr-003-api-gateway-pattern.md)

## Story: OAuth2 Implementation
**TDR References**:
- [EDR-001: User Authentication](./services/user-service/tdr/edr-001-user-authentication.md)
- [IDR-001: Password Hashing](./services/user-service/tdr/idr-001-password-hashing.md)
```

#### B.2 GitHub Issue Integration
```markdown
## Feature Request: Payment Processing
**Labels**: enhancement, backend
**TDR Impact**: Will require new EDR for payment gateway integration

**Related TDRs**:
- [ADR-002: Database per Service](./tdr/adr/adr-002-database-per-service.md)
- [EDR-001: Payment Gateway Integration](./services/payment-service/tdr/edr-001-payment-gateway-integration.md)
```

### Appendix C: AI Integration Examples

#### C.1 AI Context Format
```markdown
## AI Assistant Context
**Decision Summary**: Use OAuth2 with JWT tokens for stateless authentication
**Key Constraints**: GDPR compliance, Multi-tenant support, 99.9% uptime
**Required Patterns**: Token validation middleware, Refresh token rotation
**Anti-patterns**: Session storage, Plaintext tokens, Long-lived tokens
**Verification Commands**: `npm test auth`, `security-scan jwt-config`
```

#### C.2 Automated Compliance Check
```bash
# Example CI script
#!/bin/bash
ddse-validator --check-templates ./tdr/
ddse-compliance --verify-implementation --tdr-path ./tdr/
ddse-ai-reviewer --check-code-alignment --service user-service
```

---

**Document History**
- v1.0 (2025-07-26): Initial specification release
- Future versions will be tracked in this section

**Contributors**
- DDSE Foundation
- Industry Advisory Board
- Community Contributors

**References**
- [DDSE Foundation GitHub](https://github.com/ddse-foundation)
- [Template Repository](https://github.com/ddse-foundation/templates)
- [Tool Ecosystem](https://github.com/ddse-foundation/tools)
