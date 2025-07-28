# Contributing to DDSE Foundation

Thank you for your interest in contributing to the Decision-Driven Software Engineering (DDSE) Foundation! This project provides a methodology and tools for capturing architectural decisions in machine-readable TDRs (Technical Decision Records).

## Quick Start

1. **Fork** the repository
2. **Clone** your fork: `git clone https://github.com/your-username/ddse-foundation.git`
3. **Create** a branch: `git checkout -b feature/your-contribution`
4. **Make** your changes
5. **Submit** a pull request

## Contribution Types

### Domain Starter Packs
Create complete TDR collections for specific domains (AI/ML, E-commerce, Fintech, etc.)

**Location**: `example/your-domain-app-tdr-only/`

**Requirements**:
- Complete TDR set (MDD, ADR, EDR, IDR)
- Working generator script
- Comprehensive README
- Validation passing

### TDR Templates
Contribute reusable decision templates for common architectural patterns.

**Location**: `templates/`

### Tools & Validation
Improve generator scripts, validation tools, or CI/CD integrations.

**Location**: `tools/`, `.github/workflows/`

### Documentation
Enhance specifications, guides, or examples.

## Standards

### TDR Format
- Follow [TDR Specification](docs/tdr-specification.md)
- Include required YAML front matter
- Add rich `ai_context` blocks
- Pass ANTLR validation

### Code Quality
- Include tests for generator scripts
- Follow existing code style
- Document public functions
- Ensure cross-platform compatibility

### Commit Messages
```
type(scope): description

- feat: new feature
- fix: bug fix
- docs: documentation
- test: add tests
```

## Testing

```bash
# Run TDR validation
python tools/validate_tdrs.py

# Test generator
cd example/task-app-tdr-only
python generate.py

# Run all tests
pytest tests/
```

## Review Process

1. **Automated checks** run on all PRs
2. **Community review** for technical accuracy
3. **Maintainer approval** before merge
4. **Integration testing** with existing packs

## Getting Help

- Review existing [examples](example/)
- Check [TDR specification](docs/tdr-specification.md)
- Open an issue for questions

## License

Contributions are licensed under [MIT License](LICENSE).

---

**Ready to start?** Check out the [task-app example](example/task-app-tdr-only/) or explore [open issues](https://github.com/ddse-foundation/ddse-foundation/issues).
