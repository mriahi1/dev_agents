# 📚 Autonomous PR System Documentation

## 🎯 Documentation Philosophy

This documentation follows our core engineering principles:

- **Small, focused files** - Each doc has a single purpose
- **Grouped by directories** - Logical organization with `__init__.py` patterns
- **Durable** - Survives team changes and scale
- **Observable** - Every decision is documented and traceable
- **Composable** - Easy to understand individual components
- **Testable** - Examples and specifications you can validate
- **Low blast radius** - Mistakes in one area don't cascade
- **Expandable** - Grows cleanly with new capabilities

## 📂 Documentation Structure

```
docs/
├── architecture/          # System design & cognitive model
│   ├── README.md         # Architecture overview
│   ├── cognitive-loops.md # The three loops explained
│   ├── state-management.md # LangGraph state design
│   └── safety-design.md   # Safety-first architecture
│
├── implementation/        # Build guides
│   ├── README.md         # Implementation overview
│   ├── quick-start.md    # 5-minute setup
│   ├── day-by-day/       # Detailed build schedule
│   │   ├── day-1-setup.md
│   │   ├── day-2-agents.md
│   │   ├── day-3-loops.md
│   │   ├── day-4-safety.md
│   │   └── day-5-production.md
│   └── testing-strategy.md
│
├── integrations/         # External service guides
│   ├── README.md
│   ├── linear/
│   │   ├── setup.md
│   │   ├── workflow.md
│   │   └── api-reference.md
│   ├── github/
│   │   ├── setup.md
│   │   └── pr-automation.md
│   └── monitoring/
│       ├── langsmith.md
│       ├── sentry.md
│       └── dashboards.md
│
├── guides/              # How-to guides
│   ├── README.md
│   ├── creating-agents.md
│   ├── adding-safety-checks.md
│   ├── debugging.md
│   └── deployment.md
│
└── reference/          # Specifications & examples
    ├── README.md
    ├── api/
    ├── examples/
    └── glossary.md
```

## 🚀 Where to Start

1. **New to the system?** → Start with [implementation/quick-start.md](implementation/quick-start.md)
2. **Understanding the design?** → Read [architecture/README.md](architecture/README.md)
3. **Ready to build?** → Follow [implementation/day-by-day/](implementation/day-by-day/)
4. **Integrating services?** → Check [integrations/](integrations/)
5. **Contributing?** → See [guides/creating-agents.md](guides/creating-agents.md)

## 📋 Documentation Standards

### File Size Guidelines
- **Maximum file size**: 500 lines (prefer 200-300)
- **Single purpose**: Each file addresses ONE topic
- **Clear sections**: Use headers to break up content
- **Code examples**: Keep examples focused and minimal

### Directory Organization
- Each directory has a `README.md` explaining its purpose
- Related files are grouped together
- Deep nesting is avoided (max 3 levels)
- Cross-references use relative links

### Writing Style
- **Clear**: Assume intelligent readers, but don't assume context
- **Concise**: Get to the point quickly
- **Practical**: Include runnable examples
- **Visual**: Use diagrams where helpful

## 🔄 Keeping Docs Current

Documentation is code. It should be:
- **Version controlled** - Changes tracked in git
- **Reviewed** - PRs include doc updates
- **Tested** - Examples are executable
- **Refactored** - Consolidated when patterns emerge 