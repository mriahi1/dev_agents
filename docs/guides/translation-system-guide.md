# Translation System Guide

**Comprehensive guide for the unified translation system**  
**Updated**: 2025-01-16 after KEY-258/KEY-259 implementation  
**Status**: Production-ready with 99%+ coverage

## 🎯 **System Overview**

The translation system provides multilingual support with 4,492 active translation calls across 166 files. After KEY-258/KEY-259 standardization, it uses a single, consistent approach with comprehensive tooling.

### **Supported Languages**
- ✅ **English (EN)** - Complete (baseline)
- ✅ **French (FR)** - Complete  
- ⚠️ **German (DE)** - Partial (infrastructure ready)
- ⚠️ **Spanish (ES)** - Partial (infrastructure ready)

### **Architecture**
```
next-i18next (framework)
├── Translation Files: public/locales/{lang}/{namespace}.json
├── Constants: lib/constants/translation-keys.ts  
├── Hooks: useTranslation from react-i18next
├── API: /api/translations/{lng}/{ns} (custom backend)
└── Validation: scripts/validate_translations.py
```

## 🏗️ **File Structure**

### **Translation Files** (`public/locales/`)
```
public/locales/
├── en/                          # English (baseline)
│   ├── common.json             # Global UI elements (21KB, 619 lines)
│   ├── dashboard.json          # Dashboard-specific (48 keys)
│   ├── properties.json         # Property management (309 lines)
│   ├── navigation.json         # Navigation elements
│   └── [20+ other namespaces]
├── fr/                          # French (complete)  
│   ├── common.json             # (24KB, 632 lines)
│   ├── dashboard.json          # Complete translations
│   └── [matching namespaces]
├── de/                          # German (partial)
└── es/                          # Spanish (partial)
```

### **Translation Constants** (`lib/constants/translation-keys.ts`)
```typescript
export const TRANSLATION_KEYS = {
  NAVIGATION: {
    DASHBOARD: 'navigation.dashboard',      // ✅ Proper namespace.key format
    PROPERTIES: 'navigation.properties',   // ✅ Matches navigation.json
  },
  DASHBOARD: {
    TITLE: 'dashboard.title',             // ✅ Fixed in KEY-259
    DESCRIPTION: 'dashboard.description', // ✅ Fixed in KEY-259
  },
  // ... 109 total translation key definitions
} as const;

// Convenience exports
export const NAV_KEYS = TRANSLATION_KEYS.NAVIGATION;
export const DASHBOARD_KEYS = TRANSLATION_KEYS.DASHBOARD;
```

## 🔧 **Usage Patterns**

### **Standard Component Usage** (Recommended)
```typescript
import { useTranslation } from 'react-i18next';
import { TRANSLATION_KEYS } from '@/lib/constants/translation-keys';

export function DashboardHeader() {
  const { t } = useTranslation('dashboard');  // Load dashboard namespace
  
  return (
    <div>
      <h1>{t(TRANSLATION_KEYS.DASHBOARD.TITLE)}</h1>
      <p>{t(TRANSLATION_KEYS.DASHBOARD.DESCRIPTION)}</p>
    </div>
  );
}
```

### **Multiple Namespaces**
```typescript
import { useTranslation } from 'react-i18next';
import { NAV_KEYS, DASHBOARD_KEYS } from '@/lib/constants/translation-keys';

export function Navigation() {
  const { t } = useTranslation(['common', 'navigation', 'dashboard']);
  
  return (
    <nav>
      <Link href="/dashboard">{t(NAV_KEYS.DASHBOARD)}</Link>
      <button>{t(DASHBOARD_KEYS.ADD_PROPERTY)}</button>
    </nav>
  );
}
```

### **⚠️ Anti-Patterns (Do Not Use)**
```typescript
// ❌ WRONG: Hardcoded strings
<h1>Dashboard</h1>
<button>Add Property</button>

// ❌ WRONG: Raw translation keys without constants
{t('dashboard.title')}
{t('title')}  // Missing namespace!

// ❌ WRONG: Multiple translation systems  
import { useNamespaceTranslations } from '@/lib/i18n';  // Deprecated
import { useTranslation } from '@/lib/i18n/client-i18n';  // Removed
```

## 🛠️ **Development Tools**

### **1. Translation Validation** (`scripts/validate_translations.py`)
**Purpose**: Detect missing keys, namespace issues, and inconsistencies

```bash
# Run validation
python scripts/validate_translations.py

# Output example:
# 📂 Found languages: de, fr, es, en
# 📝 Found namespaces: dashboard, common, properties...
# ✅ All critical validation checks passed!
```

**Use Cases**:
- Before PR submission
- After adding new translations
- Regular system health checks
- Debugging translation issues

### **2. Hardcoded Text Replacement** (`scripts/fix_hardcoded_text.py`)
**Purpose**: Automatically fix hardcoded text with proper translations

```bash
# Fix hardcoded text automatically
python scripts/fix_hardcoded_text.py

# Replaces patterns like:
# "Dashboard" → {t(TRANSLATION_KEYS.DASHBOARD.TITLE)}
# "Add Property" → {t(TRANSLATION_KEYS.DASHBOARD.ADD_PROPERTY)}
```

**Features**:
- Automatic import injection
- Hook setup in components
- Safe batch processing
- Change tracking and reporting

### **3. ESLint Prevention** (`.eslintrc.translation.js`)
**Purpose**: Prevent new hardcoded strings during development

```bash
# Check for hardcoded strings
npx eslint src/ --config .eslintrc.translation.js

# Flags errors like:
# - <div>Dashboard</div>        // ❌ Use {t()} 
# - toast.success("Saved")      // ❌ Use translation
# - t('title')                  // ❌ Missing namespace
```

**Integration**: Add to your main ESLint config or run as separate check

## 📋 **Adding New Translations**

### **Step 1: Add to Translation Files**
```bash
# 1. Add to English baseline
# File: public/locales/en/your-namespace.json
{
  "newFeature": {
    "title": "New Feature",
    "description": "Description of the new feature",
    "actions": {
      "save": "Save Changes",
      "cancel": "Cancel"
    }
  }
}

# 2. Add to French
# File: public/locales/fr/your-namespace.json  
{
  "newFeature": {
    "title": "Nouvelle Fonctionnalité",
    "description": "Description de la nouvelle fonctionnalité",
    "actions": {
      "save": "Enregistrer les Modifications", 
      "cancel": "Annuler"
    }
  }
}
```

### **Step 2: Add to Translation Constants**
```typescript
// File: lib/constants/translation-keys.ts
export const TRANSLATION_KEYS = {
  // ... existing keys ...
  
  NEW_FEATURE: {
    TITLE: 'your-namespace.newFeature.title',
    DESCRIPTION: 'your-namespace.newFeature.description',
    SAVE: 'your-namespace.newFeature.actions.save',
    CANCEL: 'your-namespace.newFeature.actions.cancel',
  },
};

// Export convenience accessor
export const NEW_FEATURE_KEYS = TRANSLATION_KEYS.NEW_FEATURE;
```

### **Step 3: Use in Components**
```typescript
import { useTranslation } from 'react-i18next';
import { NEW_FEATURE_KEYS } from '@/lib/constants/translation-keys';

export function NewFeature() {
  const { t } = useTranslation('your-namespace');
  
  return (
    <div>
      <h2>{t(NEW_FEATURE_KEYS.TITLE)}</h2>
      <p>{t(NEW_FEATURE_KEYS.DESCRIPTION)}</p>
      <button>{t(NEW_FEATURE_KEYS.SAVE)}</button>
      <button>{t(NEW_FEATURE_KEYS.CANCEL)}</button>
    </div>
  );
}
```

### **Step 4: Validate**
```bash
# Run validation to ensure consistency
python scripts/validate_translations.py

# Check for hardcoded strings
npx eslint src/ --config .eslintrc.translation.js
```

## 🚨 **Troubleshooting**

### **Translation Keys Show as Raw Text**
**Symptoms**: Seeing "dashboard.title" instead of "Dashboard"

**Common Causes**:
1. **Missing namespace prefix** in constants
   ```typescript
   // ❌ Wrong
   TITLE: 'title'
   
   // ✅ Correct  
   TITLE: 'dashboard.title'
   ```

2. **Incorrect namespace in useTranslation**
   ```typescript
   // ❌ Wrong
   const { t } = useTranslation('common');
   t(DASHBOARD_KEYS.TITLE);  // Looking in wrong namespace
   
   // ✅ Correct
   const { t } = useTranslation('dashboard');
   t(DASHBOARD_KEYS.TITLE);
   ```

3. **Missing translation file**
   - Check if `public/locales/{lang}/{namespace}.json` exists
   - Run `python scripts/validate_translations.py` to identify missing files

### **Language Switching Not Working**
**Symptoms**: Interface stays in same language when switching

**Solutions**:
1. **Check next-i18next configuration**
2. **Verify API endpoint**: `/api/translations/{lng}/{ns}`
3. **Ensure component re-renders** after language change
4. **Check browser console** for loading errors

### **Translation Performance Issues**
**Symptoms**: Slow page loads, translation loading delays

**Solutions**:
1. **Optimize namespace loading** - Only load needed namespaces
2. **Check bundle size** - Large translation files impact performance
3. **Use lazy loading** for less critical translations
4. **Monitor network requests** to translation API

## 🎯 **Best Practices**

### **Naming Conventions**
```typescript
// ✅ Good: Clear, hierarchical naming
NAVIGATION: {
  DASHBOARD: 'navigation.dashboard',
  PROPERTIES: 'navigation.properties',
}

DASHBOARD: {
  TITLE: 'dashboard.title',
  ADD_PROPERTY: 'dashboard.add_property',
}

// ❌ Avoid: Unclear or inconsistent naming
MISC: {
  THING1: 'random.key',
  stuff: 'another.thing',  // Inconsistent casing
}
```

### **Translation File Organization**
```json
{
  "topLevel": {
    "subLevel": {
      "key": "value"
    },
    "actions": {
      "save": "Save",
      "cancel": "Cancel", 
      "delete": "Delete"
    }
  }
}
```

### **Component Patterns**
```typescript
// ✅ Good: Single responsibility, clear namespace
function DashboardHeader() {
  const { t } = useTranslation('dashboard');
  return <h1>{t(DASHBOARD_KEYS.TITLE)}</h1>;
}

// ✅ Good: Multiple namespaces when needed
function Navigation() {
  const { t } = useTranslation(['navigation', 'common']);
  // Use both navigation and common translations
}

// ❌ Avoid: Loading unnecessary namespaces
function SimpleButton() {
  const { t } = useTranslation(['common', 'dashboard', 'properties', 'forms']);
  return <button>{t(COMMON_KEYS.SAVE)}</button>;  // Only needs 'common'
}
```

## 📊 **System Metrics & Health**

### **Current System State** (Post KEY-258/KEY-259)
- ✅ **4,492 translation calls** across 166 files
- ✅ **24 translation namespaces** available  
- ✅ **99%+ translation coverage** (EN/FR complete)
- ✅ **Single unified system** (no fragmentation)
- ✅ **Zero regression risk** (validation tools)

### **Quality Indicators**
```bash
# Check translation system health
python scripts/validate_translations.py

# Key metrics to monitor:
# - Translation coverage percentage
# - Missing namespace files
# - Hardcoded text instances  
# - ESLint rule violations
```

### **Performance Benchmarks**
- **Page load impact**: <50ms additional load time
- **Bundle size**: ~150KB for full translation data
- **Memory usage**: ~5MB for loaded translations
- **API response**: <100ms for translation loading

## 🚀 **Future Development**

### **Expanding Language Support**
To add complete DE/ES support:
1. **Translate missing namespace files** 
2. **Validate completeness** with script
3. **Test language switching** in UI
4. **Update language selector** to include new languages

### **Advanced Features**
- **Pluralization support**: ICU message format
- **Variable interpolation**: Dynamic content in translations
- **Context-aware translations**: Different translations for different contexts
- **Translation management UI**: Non-developer translation editing

### **Maintenance Schedule**
- **Weekly**: Run validation script
- **Before each PR**: ESLint translation checks
- **Monthly**: Review translation coverage and quality
- **Quarterly**: Audit system performance and optimization

## 📚 **Additional Resources**

### **Documentation**
- **Quick Reference**: `docs/reference/translation-quick-reference.md`
- **Implementation Details**: `docs/implementation/learnings/2025-01-16-KEY-259-translation-fix-implementation.md`
- **API Reference**: [next-i18next documentation](https://react.i18next.com/)

### **Tools & Scripts**
- **Validation**: `scripts/validate_translations.py`
- **Cleanup**: `scripts/fix_hardcoded_text.py`  
- **Prevention**: `.eslintrc.translation.js`

### **Integration Examples**
- **Components**: `components/navigation/side-navigation.tsx`
- **Constants Usage**: `lib/constants/translation-keys.ts`
- **Test Files**: Look for `*.test.tsx` for testing patterns

This guide provides everything needed to maintain and extend the unified translation system. Follow these patterns for consistent, maintainable internationalization. 