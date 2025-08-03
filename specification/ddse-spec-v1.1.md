# Decision-Driven Software Engineering (DDSE) Specification v1.1

**Document Status**: Final  
**Version**: 1.1  
**Date**: August 3, 2025  
**Maintainer**: DDSE Foundation  
**License**: MIT  

## Version 1.1 Changes

This version introduces critical enhancements for **Greenfield Architecture Pattern** and contract-driven development:

### New Features
- **Contract Decision Records (CDRs)**: New TDR type for API and integration contracts
- **Greenfield Architecture Pattern**: Systematic approach for new project initialization
- **Decision-to-Implementation Traceability**: Standards for linking decisions to code
- **Enhanced AI Context**: Improved AI integration for contract-driven development

### Breaking Changes
- CDR template addition requires updated validation rules
- Traceability annotations become REQUIRED for new implementations
- Contract-first development workflow integration

---

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
11. [Greenfield Architecture Pattern](#greenfield-architecture-pattern) ⭐ *New in v1.1*
12. [Contract-Driven Development](#contract-driven-development) ⭐ *New in v1.1*
13. [Decision-to-Implementation Traceability](#decision-to-implementation-traceability) ⭐ *New in v1.1*

## 1. Introduction

### 1.1 Purpose

This specification defines the standards, practices, and organizational structures for implementing Decision-Driven Software Engineering (DDSE) methodology in software projects. DDSE establishes Technical Decision Records (TDRs) as first-class artifacts in the software development lifecycle, ensuring technical decisions are captured, maintained, and enforced throughout the development process.

**Version 1.1 Focus**: This version emphasizes **contract-driven greenfield development**, providing systematic approaches for new projects to establish comprehensive decision governance from day one while enabling AI-assisted implementation.

### 1.2 Scope

This specification covers:
- TDR taxonomy and classification (expanded with CDRs)
- Organizational structure within codebases
- Integration with project management tools (Jira, Azure Boards, GitHub Issues)
- Template standards for automated parsing (including contract specifications)
- AI-assisted development integration (enhanced with contract context)
- Compliance and governance requirements
- **Greenfield Architecture Pattern** for new project initialization
- **Contract Decision Records** for API and service specifications
- **Decision-to-Implementation Traceability** standards

### 1.3 Normative Requirements

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in RFC 2119.

## 2. Core Principles

### 2.1 Decision-First Development

Every codebase implementing DDSE:
- **MUST** maintain TDRs as primary governance artifacts
- **MUST** link all user stories and tasks to relevant TDRs
- **SHOULD** create TDRs before implementation begins
- **MUST** update TDRs when decisions change

### 2.2 Contract-Driven Implementation ⭐ *New in v1.1*

For greenfield projects and service interfaces:
- **MUST** define CDRs for all service boundaries
- **SHOULD** create API contracts before parallel development begins
- **MUST** validate implementations against contract specifications
- **SHOULD** enable parallel frontend/backend development through contracts

### 2.3 AI-Human Collaboration

DDSE facilitates effective AI-assisted development by:
- **MUST** provide structured AI context in all TDRs
- **SHOULD** use TDR content to guide AI code generation
- **MUST** validate AI-generated code against documented decisions
- **SHOULD** continuously improve AI context based on implementation feedback

### 2.4 Traceability and Governance ⭐ *Enhanced in v1.1*

All implementations:
- **MUST** include decision references in code annotations
- **SHOULD** maintain clear links between TDRs and implementation
- **MUST** validate decision compliance in CI/CD pipelines
- **SHOULD** track decision-to-code impact for maintenance

## 3. Technical Decision Records (TDR) Framework

### 3.1 TDR Taxonomy

DDSE defines six types of Technical Decision Records:

#### 3.1.1 Major Design Decision (MDD)
- **Scope**: Strategic product and system-level decisions
- **Authority**: Product/Engineering leadership
- **Impact**: Affects multiple systems or long-term strategy
- **Examples**: Technology stack, architectural style, buy-vs-build

#### 3.1.2 Architectural Decision Record (ADR)
- **Scope**: System architecture and design decisions
- **Authority**: Technical architects and senior engineers
- **Impact**: Affects system structure and component relationships
- **Examples**: Service boundaries, data flow, integration patterns

#### 3.1.3 Contract Decision Record (CDR) ⭐ *New in v1.1*
- **Scope**: API contracts, service interfaces, and integration specifications
- **Authority**: API architects and service owners
- **Impact**: Defines implementable contracts for service boundaries
- **Examples**: REST API specifications, message schemas, service interfaces

#### 3.1.4 Engineering Decision Record (EDR)
- **Scope**: Development practices, tools, and processes
- **Authority**: Engineering teams and tech leads
- **Impact**: Affects development workflow and team practices
- **Examples**: Testing strategy, deployment process, code standards

#### 3.1.5 Implementation Decision Record (IDR)
- **Scope**: Component-level and code implementation decisions
- **Authority**: Individual developers and feature teams
- **Impact**: Affects specific components or features
- **Examples**: Algorithm choice, library usage, configuration

#### 3.1.6 Technical Decision Memo (TDM)
- **Scope**: Lightweight decisions and temporary choices  
- **Authority**: Any team member
- **Impact**: Limited scope with clear expiration or review date
- **Examples**: Experiment parameters, temporary workarounds

### 3.2 TDR Relationships and Dependencies

#### 3.2.1 Hierarchical Relationships
```
MDD (Strategic Level)
├── ADR (Architectural Level)
│   ├── CDR (Contract Level) ⭐ New in v1.1
│   ├── EDR (Engineering Level)
│   └── IDR (Implementation Level)
└── TDM (Memo Level)
```

#### 3.2.2 Cross-Reference Requirements
- **MUST** reference parent decisions when creating child TDRs
- **SHOULD** reference related decisions that influence current decision
- **MUST** update dependent decisions when parent decisions change

#### 3.2.3 Contract Dependencies ⭐ *New in v1.1*
- CDRs **MUST** reference the ADRs that define their architectural context
- IDRs **SHOULD** reference CDRs when implementing service interfaces
- Contract changes **MUST** trigger review of dependent implementations

## 4. TDR Organization and Structure

### 4.1 Directory Structure

#### 4.1.1 Standard Organization
```
tdr/
├── mdd/          # Major Design Decisions
├── adr/          # Architectural Decision Records  
├── cdr/          # Contract Decision Records ⭐ New in v1.1
├── edr/          # Engineering Decision Records
├── idr/          # Implementation Decision Records
├── tdm/          # Technical Decision Memos
├── archived/     # Superseded decisions
└── index.md      # Decision registry and cross-references
```

#### 4.1.2 Alternative Organizations
For smaller projects, a flat structure **MAY** be used:
```
decisions/
├── mdd-001-product-strategy.md
├── adr-001-microservices-architecture.md
├── cdr-001-user-api-contract.md ⭐ New in v1.1
├── edr-001-testing-strategy.md
└── index.md
```

### 4.2 File Naming Conventions

#### 4.2.1 Standard Format
`{type}-{number}-{kebab-case-title}.md`

Examples:
- `mdd-001-technology-stack-selection.md`
- `adr-003-database-architecture.md`
- `cdr-001-authentication-api-contract.md` ⭐ *New in v1.1*
- `edr-002-deployment-pipeline.md`
- `idr-005-error-handling-patterns.md`

#### 4.2.2 Numbering Requirements
- Numbers **MUST** be sequential within each TDR type
- Numbers **MUST** be zero-padded to three digits (001, 002, etc.)
- Numbers **MUST NOT** be reused even after archiving

### 4.3 Version Control Integration

#### 4.3.1 Git Workflow
- TDRs **MUST** be version controlled alongside code
- TDR changes **SHOULD** use pull request workflow
- TDR updates **MUST** include rationale for changes

#### 4.3.2 Branch Strategy
- TDR changes **MAY** use feature branches for complex decisions
- TDR merges **SHOULD** be reviewed by relevant stakeholders
- TDR conflicts **MUST** be resolved before implementation proceeds

## 5. Integration with Development Workflows

### 5.1 Agile Integration

#### 5.1.1 Sprint Planning
- User stories **SHOULD** reference relevant TDRs
- New features **MUST** identify TDR requirements during planning
- Sprint backlog **SHOULD** include TDR creation tasks when needed

#### 5.1.2 Definition of Done
Projects **SHOULD** include in Definition of Done:
- Relevant TDRs are updated or created
- Implementation aligns with documented decisions
- Decision compliance is validated (for v1.1+ projects)

### 5.2 Issue Tracking Integration

#### 5.2.1 Required Metadata
Issues **SHOULD** include:
- `tdr_impact`: List of TDRs affected by the issue
- `decision_required`: Boolean indicating if new TDRs are needed
- `architectural_review`: Boolean for issues requiring architecture review

#### 5.2.2 Workflow States
- **Decision Required**: Issue identifies need for new TDR
- **Decision In Progress**: TDR is being drafted
- **Decision Approved**: TDR is approved and implementation can proceed
- **Implementation**: Code is being written according to TDRs

### 5.3 CI/CD Integration

#### 5.3.1 Validation Requirements
CI/CD pipelines **SHOULD** include:
- TDR format validation using DDSE validator
- Decision compliance checking (for v1.1+ projects)
- Contract validation against CDR specifications ⭐ *New in v1.1*

#### 5.3.2 Automated Checks
- YAML frontmatter validation
- Cross-reference integrity checking
- AI context section completeness
- Implementation traceability validation ⭐ *New in v1.1*

## 6. Template Standards

### 6.1 Required Template Elements

#### 6.1.1 YAML Frontmatter
All TDRs **MUST** include standardized YAML frontmatter:

```yaml
---
id: "{TYPE}-{NUMBER}"
title: "Decision Title"
status: "proposed|accepted|superseded|deprecated"
date: "YYYY-MM-DD"
authors: ["email@domain.com"]
reviewers: ["email@domain.com"]
category: "category-name"
related_decisions:
  - "TDR-ID: Related decision title"
ai_context:
  # Type-specific AI context
---
```

#### 6.1.2 Standard Sections
All TDRs **MUST** include these sections:
- **Summary**: Brief decision overview
- **Context**: Background and problem statement
- **Decision**: The chosen solution
- **Consequences**: Impact and trade-offs
- **Implementation**: Guidance for implementation (v1.1+)

#### 6.1.3 Contract-Specific Sections ⭐ *New in v1.1*
CDRs **MUST** additionally include:
- **Contract Specification**: Complete API or interface specification
- **Data Schemas**: Detailed schema definitions
- **Evolution Strategy**: Contract versioning and backward compatibility
- **Testing Requirements**: Contract validation and testing approach

### 6.2 AI Context Requirements

#### 6.2.1 Mandatory Fields
All TDRs **MUST** include in `ai_context`:
- `implementation_priorities`: List of key implementation guidance
- `framework_hints`: Technology-specific guidance
- `validation_rules`: Criteria for validating implementation

#### 6.2.2 Type-Specific Context

**CDR AI Context** ⭐ *New in v1.1*:
```yaml
ai_context:
  contract_type: "REST API|GraphQL|gRPC|Message Queue"
  implementation_priorities:
    - "OpenAPI specification compliance"
    - "Backward compatibility requirements"
  validation_rules:
    - "All endpoints must return proper HTTP status codes"
    - "Request/response schemas must be validated"
  framework_hints:
    backend: "Framework and libraries to use"
    frontend: "Client integration patterns"
    testing: "Contract testing approach"
```

### 6.3 Cross-Reference Standards

#### 6.3.1 Reference Format
References **MUST** use the format:
- Internal: `[TDR-ID](relative/path/to/file.md)`
- External: `[External System](https://example.com/path)`

#### 6.3.2 Impact Tracking ⭐ *Enhanced in v1.1*
TDRs **SHOULD** maintain:
- `affects`: List of components/services impacted by the decision
- `implementation_refs`: Links to code implementing the decision
- `test_refs`: Links to tests validating the decision

## 7. Automation and Tooling Requirements

### 7.1 TDR Validator Requirements

#### 7.1.1 Core Validation
The TDR validator **MUST** validate:
- YAML frontmatter syntax and required fields
- Markdown structure and required sections  
- Cross-reference integrity
- ID uniqueness and format compliance

#### 7.1.2 Contract Validation ⭐ *New in v1.1*
For CDRs, the validator **MUST** additionally validate:
- OpenAPI specification syntax (for REST APIs)
- Schema definition completeness
- Contract evolution compatibility
- Implementation traceability references

### 7.2 IDE Integration

#### 7.2.1 Template Support
IDE plugins **SHOULD** provide:
- TDR template scaffolding
- Auto-completion for TDR references
- Real-time validation feedback
- Decision impact visualization

#### 7.2.2 Code Integration ⭐ *New in v1.1*
IDE plugins **SHOULD** support:
- Decision annotation auto-completion
- TDR context display in code editors
- Contract compliance checking
- Implementation traceability navigation

### 7.3 AI Tool Integration

#### 7.3.1 Context Injection
AI coding assistants **SHOULD**:
- Automatically inject relevant TDR context
- Validate generated code against decisions
- Suggest appropriate decision references
- Maintain contract compliance in generated code ⭐ *New in v1.1*

#### 7.3.2 Decision Support
AI tools **MAY** assist with:
- TDR drafting and template completion
- Impact analysis for decision changes
- Alternative solution exploration
- Contract specification generation ⭐ *New in v1.1*

## 8. Compliance and Governance

### 8.1 Organizational Roles

#### 8.1.1 Decision Steward
Each TDR type **SHOULD** have designated stewards:
- **MDD Steward**: Product/Engineering leadership
- **ADR Steward**: Principal/Staff architects
- **CDR Steward**: API architects and service owners ⭐ *New in v1.1*
- **EDR Steward**: Engineering managers/tech leads
- **IDR Steward**: Senior engineers
- **TDM Steward**: Any team member

#### 8.1.2 Review Requirements
- MDDs **MUST** be reviewed by engineering leadership
- ADRs **MUST** be reviewed by architecture team
- CDRs **MUST** be reviewed by API governance committee ⭐ *New in v1.1*
- EDRs **SHOULD** be reviewed by engineering team
- IDRs **MAY** be reviewed by feature team
- TDMs **MAY** be self-approved with notification

### 8.2 Compliance Metrics

#### 8.2.1 Decision Coverage
Projects **SHOULD** track:
- Percentage of user stories with TDR references
- Percentage of architectural decisions documented
- Percentage of APIs with CDR specifications ⭐ *New in v1.1*

#### 8.2.2 Implementation Alignment ⭐ *New in v1.1*
Projects **SHOULD** measure:
- Code coverage with decision annotations
- Contract compliance in API implementations
- Decision-to-code traceability completeness

### 8.3 Audit Requirements

#### 8.3.1 Regular Reviews
- TDRs **SHOULD** be reviewed quarterly for relevance
- Superseded decisions **MUST** be moved to archived/ directory
- Decision impact **SHOULD** be assessed during retrospectives

#### 8.3.2 Change Management
- Decision changes **MUST** trigger impact analysis
- Affected teams **MUST** be notified of decision updates
- Implementation changes **MUST** be validated against updated decisions

## 9. Implementation Guidelines

### 9.1 Adoption Strategy

#### 9.1.1 Gradual Implementation
Organizations **MAY** adopt DDSE incrementally:
1. Start with ADRs for architectural decisions
2. Add EDRs for development practices
3. Introduce IDRs for implementation details
4. Implement CDRs for service boundaries ⭐ *New in v1.1*
5. Establish full traceability framework ⭐ *New in v1.1*

#### 9.1.2 Tool Integration
- Choose tools that integrate with existing workflows
- Prioritize automated validation and compliance checking
- Ensure seamless IDE and CI/CD integration

### 9.2 Team Training

#### 9.2.1 Required Knowledge
Team members **SHOULD** understand:
- DDSE principles and TDR taxonomy
- Template structure and requirements
- Decision review and approval processes
- Contract-driven development workflows ⭐ *New in v1.1*

#### 9.2.2 Role-Specific Training
- **Architects**: Focus on ADR and CDR creation ⭐ *Updated in v1.1*
- **Developers**: Emphasize IDR usage and traceability ⭐ *Updated in v1.1*
- **Product Managers**: Concentrate on MDD and business alignment
- **DevOps Engineers**: Focus on automation and compliance checking

## 10. Version Management

### 10.1 TDR Versioning

#### 10.1.1 Version Control
- TDRs **MUST** be versioned with the codebase
- Major decision changes **SHOULD** create new TDR versions
- Old versions **MUST** be archived with clear supersession links

#### 10.1.2 Backward Compatibility
- TDR format changes **MUST** be backward compatible
- Template updates **SHOULD** not break existing TDRs
- Validation tools **MUST** support legacy formats during transition

### 10.2 Specification Evolution

#### 10.2.1 Version Numbering
- Major versions (1.0, 2.0) for breaking changes
- Minor versions (1.1, 1.2) for new features
- Patch versions (1.1.1) for bug fixes and clarifications

#### 10.2.2 Migration Support
- Each version **MUST** include migration guidance
- Breaking changes **MUST** be clearly documented
- Migration tools **SHOULD** be provided when feasible

## 11. Greenfield Architecture Pattern ⭐ *New in v1.1*

### 11.1 Pattern Overview

The Greenfield Architecture Pattern provides a systematic approach for establishing comprehensive decision governance in new projects from day one.

#### 11.1.1 Objectives
- Establish complete decision foundation before implementation
- Enable parallel development through contract specifications
- Provide rich context for AI-assisted development
- Ensure architectural integrity from project inception

#### 11.1.2 Implementation Phases
1. **Decision Foundation**: Establish MDDs, ADRs, and EDRs
2. **Contract Definition**: Create CDRs and detailed IDRs
3. **Parallel Development**: Enable simultaneous frontend/backend development

### 11.2 Required Deliverables

#### 11.2.1 Phase 1: Decision Foundation
- **MUST** create complete MDD hierarchy for product strategy
- **MUST** define system ADRs for architecture style and major components
- **MUST** establish EDRs for development workflow and practices

#### 11.2.2 Phase 2: Contract Definition
- **MUST** create CDRs for all service boundaries and APIs
- **MUST** define data schemas and integration contracts
- **SHOULD** create IDRs for implementation patterns and frameworks

#### 11.2.3 Phase 3: Implementation Enablement
- **MUST** provide mock implementations based on CDR specifications
- **MUST** establish contract testing and validation frameworks
- **SHOULD** enable parallel team development with minimal dependencies

### 11.3 Success Metrics

#### 11.3.1 Decision Quality
- 100% of architectural concerns addressed in decision hierarchy
- Complete API contract coverage for service boundaries
- Full traceability from business requirements to implementation decisions

#### 11.3.2 Development Velocity  
- Reduced time to first working implementation
- High parallel development efficiency with minimal team blocking
- Significant rework reduction compared to ad-hoc decision making

## 12. Contract-Driven Development ⭐ *New in v1.1*

### 12.1 CDR Specifications

#### 12.1.1 Required Elements
CDRs **MUST** include:
- Complete API specification (OpenAPI, GraphQL schema, etc.)
- Data schema definitions with validation rules
- Authentication and authorization requirements
- Error handling and status code specifications
- Rate limiting and performance requirements

#### 12.1.2 Contract Evolution
- **MUST** define versioning strategy and backward compatibility approach
- **MUST** specify breaking change notification and migration process
- **SHOULD** include deprecation timeline and sunset procedures

### 12.2 Implementation Requirements

#### 12.2.1 Mock Services
- **SHOULD** provide mock implementations for all CDR contracts
- **MUST** validate mock responses against contract specifications
- **SHOULD** enable frontend development without backend dependencies

#### 12.2.2 Contract Testing
- **MUST** implement consumer-driven contract testing
- **MUST** validate implementation compliance with CDR specifications
- **SHOULD** include automated contract regression testing

### 12.3 AI Integration

#### 12.3.1 Contract-Informed Generation
- AI tools **SHOULD** use CDR specifications to generate implementation code
- Generated code **MUST** comply with contract specifications
- AI context **SHOULD** include contract validation rules and constraints

#### 12.3.2 Contract Validation
- AI assistants **SHOULD** validate generated code against CDR specifications
- **MUST** flag contract violations during code generation
- **SHOULD** suggest contract-compliant alternatives for invalid code

## 13. Decision-to-Implementation Traceability ⭐ *New in v1.1*

### 13.1 Traceability Requirements

#### 13.1.1 Code Annotations
All implementation code **MUST** include decision references:
```typescript
/**
 * @implements ADR-003: JWT Authentication Strategy
 * @contract GET /api/v1/auth/validate
 * @see tdr/adr/adr-003-jwt-authentication.md
 */
```

#### 13.1.2 Required Annotations
- `@implements`: Reference to specific TDR being implemented
- `@contract`: Reference to CDR contract being fulfilled (when applicable)
- `@see`: Link to relevant TDR documentation

### 13.2 Validation and Compliance

#### 13.2.1 Automated Checking
CI/CD pipelines **MUST** include:
- Validation of TDR reference accuracy
- Verification of contract compliance in implementations  
- Detection of orphaned code without decision references

#### 13.2.2 Coverage Metrics
Projects **SHOULD** maintain:
- Percentage of code with decision references
- Percentage of TDRs with implementation coverage
- Contract compliance rate for service implementations

### 13.3 Maintenance and Evolution

#### 13.3.1 Impact Analysis
- Decision changes **MUST** trigger analysis of affected implementations
- **MUST** identify code requiring updates when TDRs change
- **SHOULD** provide automated refactoring suggestions when possible

#### 13.3.2 Continuous Alignment
- **SHOULD** regularly validate decision-code alignment
- **MUST** update traceability references when code is refactored
- **SHOULD** deprecate decision references when functionality is removed

## Conclusion

DDSE Specification v1.1 establishes a comprehensive framework for decision-driven software engineering with particular emphasis on greenfield project success and contract-driven development. The introduction of Contract Decision Records (CDRs) and systematic traceability requirements enables teams to bridge the gap between architectural decisions and implementable code while maintaining clear governance and AI integration capabilities.

Organizations implementing DDSE v1.1 gain:
- **Systematic approach** to new project architecture establishment
- **Clear contracts** enabling parallel development and reduced coordination overhead
- **Rich AI context** for enhanced code generation and validation
- **Comprehensive traceability** ensuring long-term architectural integrity

This specification serves as the foundation for tools, templates, and practices that enable effective decision-driven development in modern software engineering environments.

---

**Document Metadata**:
- **Author**: DDSE Foundation
- **Contributors**: Open source community
- **License**: MIT
- **Source**: https://github.com/ddse-foundation/ddse-foundation
- **Issues**: https://github.com/ddse-foundation/ddse-foundation/issues

**Change Log**:
- v1.1 (2025-08-03): Added CDRs, Greenfield Architecture Pattern, traceability requirements
- v1.0 (2025-07-26): Initial specification release
