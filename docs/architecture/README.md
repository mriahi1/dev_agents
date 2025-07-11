# Architecture Documentation

⚠️ **Note**: Most documents in this directory are from the original "Autonomous PR System" vision. They are kept for historical reference but do not reflect the current Cursor DevOps Toolkit architecture.

For the current architecture, see:
- [Toolkit Transformation](../implementation/toolkit-transformation.md) - How we evolved to the current approach
- [Source Code README](../../src/README.md) - Current implementation structure

## Historical Documents

The following documents describe the original autonomous system design:
- `original-system-plan.md` - The original autonomous vision
- `langgraph-architecture.md` - LangGraph-based autonomous design
- `cognitive-loops.md` - Three-loop cognitive model
- `state-management.md` - Complex state management for autonomous operation
- `safety-design.md` - Safety mechanisms for autonomous code generation

## Current Architecture

The Cursor DevOps Toolkit follows a much simpler architecture:

```
User → Cursor → CLI Commands → External APIs → Results → Cursor → User
```

- **No autonomous operation** - Human + Cursor collaboration
- **Simple CLI tools** - Each tool does one thing
- **No complex state** - Stateless operations
- **Direct API integration** - Linear and GitHub clients 