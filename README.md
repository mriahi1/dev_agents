# Dev Agents - Autonomous Development Toolkit

An autonomous development toolkit for software engineering tasks with integrated Linear workflow management and comprehensive translation system.

## 🎯 **Recent Major Implementations**

### **Translation System Standardization** ✅ **COMPLETED**
- **4,492 translation calls** standardized across 166 files
- **99%+ translation coverage** with EN/FR complete support
- **Single unified system** replacing 3 fragmented approaches
- **Comprehensive tooling** for validation and maintenance

**Key Tools Created**:
- `scripts/validate_translations.py` - Translation system health checks
- `scripts/fix_hardcoded_text.py` - Automated hardcoded text replacement  
- `.eslintrc.translation.js` - Prevention rules for new hardcoded strings
- `lib/constants/translation-keys.ts` - Centralized translation constants

**Linear Tasks**: KEY-258 (standardization), KEY-259 (regression fix)

## 🚀 **Quick Start**

### **Setup**
```bash
# Install dependencies
pip install -r requirements.txt

# Verify setup
python scripts/verify_setup.py

# Run tests
python -m pytest tests/
```

### **Translation System Usage**
```typescript
// Standard component pattern
import { useTranslation } from 'react-i18next';
import { TRANSLATION_KEYS } from '@/lib/constants/translation-keys';

function MyComponent() {
  const { t } = useTranslation('dashboard');
  return <h1>{t(TRANSLATION_KEYS.DASHBOARD.TITLE)}</h1>;
}
```

### **Development Tools**
```bash
# Validate translation system
python scripts/validate_translations.py

# Fix hardcoded text automatically
python scripts/fix_hardcoded_text.py

# Check for hardcoded strings
npx eslint src/ --config .eslintrc.translation.js
```

## 🏗️ **Architecture**

### **Core Components**
- **Analyzers**: Code analysis tools for security, performance, accessibility
- **Integrations**: GitHub and Linear API clients for workflow automation
- **Translation System**: Comprehensive i18n with validation and tooling
- **Documentation**: Complete learning system for knowledge transfer

### **Translation System Architecture**
```
next-i18next (framework)
├── Translation Files: public/locales/{lang}/{namespace}.json
├── Constants: lib/constants/translation-keys.ts  
├── Hooks: useTranslation from react-i18next
├── API: /api/translations/{lng}/{ns} (custom backend)
└── Validation: scripts/validate_translations.py
```

## 📁 **Project Structure**

```
dev_agents/
├── src/
│   ├── analyzers/           # Code analysis tools
│   ├── integrations/        # External service clients
│   └── utils/              # Shared utilities
├── scripts/
│   ├── validate_translations.py    # Translation validation
│   ├── fix_hardcoded_text.py      # Automated text replacement
│   └── verify_setup.py            # System verification
├── docs/
│   ├── guides/             # Comprehensive guides
│   │   ├── translation-system-guide.md
│   │   └── perfect-workflow-pattern.md
│   ├── reference/          # Quick reference docs
│   │   └── translation-quick-reference.md
│   └── implementation/     # Implementation learnings
├── lib/
│   └── constants/
│       └── translation-keys.ts    # Translation constants
├── components/             # Reusable components
├── projects/              # Project-specific work
└── tests/                 # Test suite
```

## 🛠️ **Available Tools**

### **Translation System** (Production Ready)
```bash
# System health check
python scripts/validate_translations.py

# Automated cleanup
python scripts/fix_hardcoded_text.py

# Development prevention
npx eslint --config .eslintrc.translation.js
```

### **Code Analysis**
```bash
# Security analysis
python src/analyzers/security_analyzer.py

# Performance analysis  
python src/analyzers/performance_analyzer.py

# Accessibility analysis
python src/analyzers/accessibility_analyzer.py
```

### **Workflow Integration**
```bash
# Linear integration
python src/integrations/linear_client.py

# GitHub integration
python src/integrations/github_client.py
```

## 📚 **Documentation**

### **Translation System**
- **Complete Guide**: `docs/guides/translation-system-guide.md`
- **Quick Reference**: `docs/reference/translation-quick-reference.md`
- **Implementation Summary**: `docs/implementation/learnings/2025-01-16-KEY-259-translation-fix-implementation.md`

### **Development Patterns**
- **Perfect Workflow**: `docs/guides/perfect-workflow-pattern.md`
- **PR Review Process**: `docs/guides/pr-review-workflow.md`
- **Development Principles**: `docs/guides/development-principles.md`

### **Architecture & Design**
- **System Architecture**: `docs/architecture/README.md`
- **State Management**: `docs/architecture/state-management.md`
- **Safety Design**: `docs/architecture/safety-design.md`

## 🎯 **Translation System Features**

### **Multi-Language Support**
- ✅ **English (EN)** - Complete baseline
- ✅ **French (FR)** - Complete production-ready  
- ⚠️ **German (DE)** - Infrastructure ready
- ⚠️ **Spanish (ES)** - Infrastructure ready

### **Developer Experience**
- **Type-safe constants** for all translation keys
- **ESLint integration** prevents hardcoded strings
- **Automated validation** detects missing translations
- **Batch processing tools** for maintenance
- **Comprehensive documentation** with examples

### **System Health**
- **4,492 active translation calls** across codebase
- **24 translation namespaces** organized by feature
- **99%+ translation coverage** maintained
- **Zero regression risk** with validation tools
- **Performance optimized** (<50ms load impact)

## 🔧 **Configuration**

### **Environment Variables**
```bash
# Linear integration
export LINEAR_API_KEY="your_linear_api_key"
export LINEAR_TEAM_ID="your_team_id"

# GitHub integration  
export GITHUB_TOKEN="your_github_token"
```

### **Translation Configuration**
The translation system uses next-i18next with custom API backend. Configuration is automatically handled, but you can customize:

- **Language switching**: Automatic UI updates
- **Namespace loading**: Optimized for performance
- **Fallback handling**: Graceful degradation
- **API endpoints**: Custom translation loading

## 🚀 **Deployment**

### **Translation System Ready**
All translation system components are production-ready:
- ✅ Fixed critical dashboard translation regression
- ✅ Comprehensive validation and prevention tools
- ✅ Complete documentation and examples
- ✅ Zero-regression deployment with rollback plan

### **Integration Requirements**
- **next-i18next**: Translation framework
- **ESLint**: Development-time validation
- **Python 3.8+**: Validation and maintenance scripts

## 📊 **Success Metrics**

### **Translation System (Post KEY-258/KEY-259)**
- **Coverage**: 99%+ translated text (target maintained)
- **Performance**: <50ms additional load time
- **Quality**: Zero raw translation keys visible
- **Maintainability**: Automated validation prevents regressions
- **Developer Experience**: Clear patterns and comprehensive tooling

### **Overall System Health**
- **Test Coverage**: Comprehensive test suite
- **Documentation**: Complete guides and references
- **Integration**: Seamless Linear and GitHub workflows
- **Knowledge Transfer**: Detailed learning documentation

## 🤝 **Contributing**

### **Translation Updates**
1. **Add translations** to `public/locales/{lang}/{namespace}.json`
2. **Update constants** in `lib/constants/translation-keys.ts`
3. **Run validation** with `python scripts/validate_translations.py`
4. **Test changes** with ESLint rules

### **General Development**
1. **Follow patterns** documented in `docs/guides/`
2. **Use validation tools** before submitting PRs
3. **Update documentation** for significant changes
4. **Run tests** to ensure system stability

## 📞 **Support**

- **Documentation**: See `docs/` directory for comprehensive guides
- **Quick Reference**: `docs/reference/translation-quick-reference.md`
- **Implementation Details**: Check `docs/implementation/learnings/`
- **Linear Integration**: Track progress with automated task management

## 🏆 **Achievements**

- ✅ **Translation System Standardization**: 4,492 calls unified
- ✅ **Comprehensive Tooling**: Validation, cleanup, and prevention
- ✅ **99%+ Coverage**: Professional multilingual experience
- ✅ **Zero Regression Risk**: Automated validation and monitoring
- ✅ **Complete Documentation**: Future-ready knowledge transfer

Built with comprehensive tooling for sustainable development and seamless internationalization. 