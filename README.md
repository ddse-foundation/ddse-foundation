# Decision-Driven Software Engineering (DDSE) Foundation

> **Where Human Intelligence and Artificial Intelligence Collaborate in Software Development**

[![DDSE Version](https://img.shields.io/badge/DDSE-v1.0-blue.svg)](https://github.com/ddse-org/ddse-foundation)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Community](https://img.shields.io/badge/community-join-orange.svg)](CONTRIBUTING.md)

## Overview

Decision-Driven Software Engineering (DDSE) is a modern software development methodology that makes technical decisions first-class artifacts in the development lifecycle. DDSE bridges the gap between agile development practices and architectural governance, especially in the era of AI-assisted coding.

## Why DDSE Now?

> **The foundational principle:** *"In the AI era, human value lies not in being the exclusive generator of solutions, but in being the authoritative decision-maker who guides generation toward human-aligned outcomes."*

**AI can generate code faster than humans—but it can't make intelligent decisions about what should be built or why.** Without decision governance, AI-assisted development creates a dangerous gap: rapid implementation without human authority over architectural direction.

**The Critical Problems:**
- AI generates code without understanding your architectural decisions and constraints
- Teams lose decision context as AI accelerates development cycles  
- Technical debt compounds as AI suggestions conflict with undocumented design principles
- Human decision authority gets eroded by the speed of AI implementation

**The DDSE Solution:**
DDSE preserves human decision authority while unleashing AI implementation power. By making technical decisions explicit and structured, you create "decision memory" that:

✅ **Guides AI tools** with your authorized architectural constraints  
✅ **Preserves human authority** over system evolution and direction  
✅ **Accelerates AI effectiveness** through rich decision context  
✅ **Prevents architectural drift** caused by uninformed AI suggestions  

**The bottom line:** Teams using AI without decision governance are building fast toward chaos. DDSE ensures you harness AI's speed while maintaining human-directed, intentional architecture.

*Make your decisions AI-ready before AI makes decisions for you.*

## Quick Start

- **New to DDSE?** Start with the [DDSE Manifesto](manifesto/ddse-manifesto.md) and [Core Principles](principle.md)
- **Academic Context?** Read our [Research Preprint](PREPRINT.md) for theoretical foundation
- **Want to adopt DDSE?** Follow the [Implementation Guide](adoption/implementation-guide.md)
- **Looking for templates?** Explore [TDR Templates](tdr-templates/) with AI context support
- **Integrating with Agile?** See our [Agile Integration Guide](integration/agile-integration.md)
- **Need validation tools?** Use our [TDR Validator](tools/tdr_validator.py) and [ANTLR Grammar](tools/TDRGrammar.g4)

## Repository Structure

```text
ddse-foundation/
├── manifesto/                  # Core philosophy and principles
│   ├── ddse-manifesto.md      # Main manifesto document
│   └── author-bio.md          # Founding researcher biography
├── principle.md               # Philosophical foundation document
├── PREPRINT.md               # Academic research preprint
├── ddse-spec-v1.0.md         # Complete DDSE specification
├── tdr-templates/            # Standard TDR templates with AI context
│   ├── mdd-template.md       # Major Design Decision template
│   ├── adr-template.md       # Architectural Decision Record template
│   ├── edr-template.md       # Engineering Decision Record template
│   ├── idr-template.md       # Implementation Decision Record template
│   ├── tdm-template.md       # Technical Decision Memo template
│   └── README.md             # Template usage guide
├── adoption/                 # Implementation guidance
│   └── implementation-guide.md # Flexible adoption strategies
├── integration/              # Framework integration guides
│   ├── agile-integration.md  # Natural Agile enhancement patterns
│   └── README.md             # Integration overview
├── tools/                    # Validation and development tools
│   ├── TDRGrammar.g4        # ANTLR4 grammar for TDR parsing
│   ├── tdr_validator.py     # Python TDR compliance validator
│   └── README.md            # Tool usage documentation
├── community/               # Community governance and participation
│   ├── governance.md        # Foundation governance structure
│   └── README.md           # Community hub navigation
└── images/                 # Documentation assets and diagrams
```

## Core Concepts

DDSE introduces **Technical Decision Records (TDRs)** as structured artifacts that capture technical choices with AI-ready context:

- **MDD (Major Design Decision)**: Strategic architectural and technology choices
- **ADR (Architectural Decision Record)**: System architecture and design decisions  
- **EDR (Engineering Decision Record)**: Development practices and tool decisions
- **IDR (Implementation Decision Record)**: Component and code-level decisions
- **TDM (Technical Decision Memo)**: Lightweight decision documentation

All TDR templates include:
- **YAML frontmatter** for structured metadata
- **AI context sections** for intelligent tool integration
- **Cross-reference support** for decision traceability
- **Validation-ready structure** for automated compliance checking

## Key Benefits

- 🎯 **Reduced Architectural Drift**: Explicit decisions prevent uncontrolled system evolution
- 🤖 **AI-Enhanced Development**: AI tools work intelligently within documented decision context
- 📚 **Preserved Decision Knowledge**: Rationale and trade-offs are captured for future reference
- 🔍 **Enhanced Traceability**: Clear links between decisions, implementation, and outcomes
- ⚡ **Faster Team Onboarding**: New members understand system evolution and constraints
- 🔧 **Automated Validation**: Tools ensure decision documentation compliance and quality
- 🧠 **Human-AI Collaboration**: Preserve human decision authority while leveraging AI capabilities

## Getting Started

1. **Understand the Philosophy**: Read the [Core Principles](principle.md) and [Manifesto](manifesto/ddse-manifesto.md)
2. **Explore the Specification**: Review the [DDSE Specification](ddse-spec-v1.0.md) for complete methodology
3. **Try the Templates**: Use our [TDR Templates](tdr-templates/) for your first decisions
4. **Validate Your Work**: Run the [TDR Validator](tools/tdr_validator.py) to ensure compliance
5. **Integrate Naturally**: Follow our [Agile Integration Guide](integration/agile-integration.md) for seamless adoption
6. **Join the Community**: Connect through our [Community Hub](community/README.md)

## Tools & Validation

DDSE includes comprehensive tooling for automated validation and compliance:

- **[TDR Validator](tools/tdr_validator.py)**: Python-based validation engine
  - Validates YAML frontmatter and required sections
  - Checks cross-references and AI context sections
  - Supports all TDR types with type-specific rules
  - CLI interface with text and JSON output formats

- **[ANTLR4 Grammar](tools/TDRGrammar.g4)**: Complete grammar specification
  - Defines TDR markdown structure for parsing
  - Enables language-agnostic validator implementations
  - Supports frontmatter, sections, and cross-references

**Usage Examples:**

```bash
# Validate a single TDR file
python tools/tdr_validator.py tdr-templates/adr-template.md

# Validate entire directory with strict mode
python tools/tdr_validator.py tdr-templates/ --strict

# Generate JSON validation report
python tools/tdr_validator.py tdr-templates/ --output json
```

## Community & Governance

The DDSE Foundation operates through collaborative governance with multiple ways to participate:

**Leadership Structure:**
### Leadership

- **Founding Chair**: Mahmudur Rahman Manna - Convener, Researcher, and Principal Architect
- **Community Stewards**: Open positions - apply through governance process
- **Executive Committee**: Technical Director, Community Manager, Industry Liaison *(positions open)*
- **Advisory Board**: Academic Advisor, AI Ethics Advisor, Enterprise Architect *(positions open)*
- **Working Groups**: Specification, Tooling, and Education leads *(positions open)*

**Get Involved:**
- **Review our [Governance Structure](community/governance.md)** for leadership opportunities
- **Join Community Discussions** through our communication channels
- **Contribute to Tools and Documentation** via GitHub
- **Share Your DDSE Experience** through case studies and feedback

**Contact:**
- **Foundation Repository**: [GitHub](https://github.com/ddse-foundation/ddse-foundation)
- **Community Hub**: [Community README](community/README.md)
- **Founding Chair**: Mahmudur Rahman Manna (mahmudur.r.manna@gmail.com)
- **Leadership Contact**: [Full governance information](community/governance.md)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Citation

If you use DDSE in your research or practice, please cite our foundational work:

```bibtex
@misc{ddse2025,
  title={Decision-Driven Software Engineering (DDSE): Preserving Human Agency in AI-Assisted Development},
  author={DDSE Foundation},
  year={2025},
  howpublished={\url{https://github.com/ddse-foundation/ddse-foundation}},
  note={Academic preprint available at PREPRINT.md}
}
```

For academic contexts, also reference our research preprint: [PREPRINT.md](PREPRINT.md)

---

**Join the DDSE Foundation** • [Community Hub](community/README.md) • [Governance](community/governance.md) • [Academic Research](PREPRINT.md)
