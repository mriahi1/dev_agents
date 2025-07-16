# Translation System Quick Reference

**Fast reference for developers using the unified translation system**

## 🚀 **Quick Start**

### **Basic Component Setup**
```typescript
import { useTranslation } from 'react-i18next';
import { TRANSLATION_KEYS } from '@/lib/constants/translation-keys';

function MyComponent() {
  const { t } = useTranslation('namespace');
  return <h1>{t(TRANSLATION_KEYS.SECTION.KEY)}</h1>;
}
```

### **Available Namespaces**
```typescript
// Most commonly used:
useTranslation('common')       // Global UI elements
useTranslation('navigation')   // Menu and navigation
useTranslation('dashboard')    // Dashboard-specific
useTranslation('properties')   // Property management
useTranslation('forms')        // Form elements and validation

// Full list: 24 namespaces available
// See: public/locales/en/ for complete list
```

## 🎯 **Translation Constants**

### **Navigation**
```typescript
import { NAV_KEYS } from '@/lib/constants/translation-keys';

NAV_KEYS.DASHBOARD      // 'navigation.dashboard'
NAV_KEYS.PROPERTIES     // 'navigation.properties'  
NAV_KEYS.TENANTS        // 'navigation.tenants'
NAV_KEYS.SETTINGS       // 'navigation.settings'
```

### **Dashboard**
```typescript
import { DASHBOARD_KEYS } from '@/lib/constants/translation-keys';

DASHBOARD_KEYS.TITLE           // 'dashboard.title'
DASHBOARD_KEYS.DESCRIPTION     // 'dashboard.description'
DASHBOARD_KEYS.ADD_PROPERTY    // 'dashboard.add_property'
```

### **Common Actions**
```typescript
import { ACTION_KEYS } from '@/lib/constants/translation-keys';

ACTION_KEYS.SAVE        // 'actions.save'
ACTION_KEYS.CANCEL      // 'actions.cancel'
ACTION_KEYS.DELETE      // 'actions.delete'
ACTION_KEYS.EDIT        // 'actions.edit'
```

### **UI Elements**
```typescript
import { UI_KEYS } from '@/lib/constants/translation-keys';

UI_KEYS.LOADING         // 'status.loading'
UI_KEYS.ERROR          // 'status.error'
UI_KEYS.NO_DATA        // 'status.empty'
UI_KEYS.SUCCESS        // 'status.success'
```

## 🔧 **Common Patterns**

### **Single Namespace**
```typescript
function DashboardPage() {
  const { t } = useTranslation('dashboard');
  
  return (
    <div>
      <h1>{t(DASHBOARD_KEYS.TITLE)}</h1>
      <p>{t(DASHBOARD_KEYS.DESCRIPTION)}</p>
    </div>
  );
}
```

### **Multiple Namespaces**
```typescript
function ComplexComponent() {
  const { t } = useTranslation(['common', 'dashboard', 'navigation']);
  
  return (
    <div>
      <nav>{t(NAV_KEYS.DASHBOARD)}</nav>
      <h1>{t(DASHBOARD_KEYS.TITLE)}</h1>
      <button>{t(ACTION_KEYS.SAVE)}</button>
    </div>
  );
}
```

### **With Variables**
```typescript
// Translation file: { "welcome": "Welcome back, {{name}}!" }
const { t } = useTranslation('common');
<span>{t('welcome', { name: user.name })}</span>
```

## 🛠️ **Development Tools**

### **Validation**
```bash
# Check translation system health
python scripts/validate_translations.py

# Quick check for missing namespaces or keys
```

### **Fix Hardcoded Text**
```bash
# Automatically replace hardcoded strings
python scripts/fix_hardcoded_text.py

# Replaces: "Dashboard" → {t(TRANSLATION_KEYS.DASHBOARD.TITLE)}
```

### **ESLint Prevention**
```bash
# Check for hardcoded strings
npx eslint src/ --config .eslintrc.translation.js

# Catches: <div>Dashboard</div>, toast.success("Saved")
```

## ❌ **Common Mistakes**

### **Missing Namespace Prefix**
```typescript
// ❌ Wrong (missing namespace)
TITLE: 'title'

// ✅ Correct (includes namespace)
TITLE: 'dashboard.title'
```

### **Wrong Namespace in Hook**
```typescript
// ❌ Wrong (looking in wrong namespace)
const { t } = useTranslation('common');
{t(DASHBOARD_KEYS.TITLE)}  // dashboard.title not in common.json

// ✅ Correct (matching namespace)
const { t } = useTranslation('dashboard');
{t(DASHBOARD_KEYS.TITLE)}
```

### **Hardcoded Strings**
```typescript
// ❌ Wrong (hardcoded)
<h1>Dashboard</h1>
<button>Save</button>

// ✅ Correct (translated)
<h1>{t(DASHBOARD_KEYS.TITLE)}</h1>
<button>{t(ACTION_KEYS.SAVE)}</button>
```

### **Raw Translation Keys**
```typescript
// ❌ Discouraged (raw keys)
{t('dashboard.title')}

// ✅ Preferred (constants)
{t(DASHBOARD_KEYS.TITLE)}
```

## 🚨 **Troubleshooting**

### **Seeing Raw Keys Instead of Text**
**Problem**: "dashboard.title" displays instead of "Dashboard"

**Solutions**:
1. Check namespace prefix in constants
2. Verify useTranslation namespace matches
3. Ensure translation file exists

### **Translation Not Loading**
**Problem**: Text doesn't change when switching languages

**Solutions**:
1. Check next-i18next configuration
2. Verify translation files exist for target language
3. Check browser console for errors

### **ESLint Errors**
**Problem**: ESLint flagging translation usage

**Solutions**:
1. Use TRANSLATION_KEYS constants instead of raw strings
2. Add required imports (useTranslation, TRANSLATION_KEYS)
3. Check for typos in translation keys

## 📁 **File Locations**

### **Translation Files**
```
public/locales/
├── en/dashboard.json          # English dashboard translations
├── fr/dashboard.json          # French dashboard translations
└── [lang]/[namespace].json    # Pattern for all translations
```

### **Constants**
```
lib/constants/translation-keys.ts    # All translation key constants
```

### **Tools**
```
scripts/validate_translations.py     # Validation tool
scripts/fix_hardcoded_text.py       # Cleanup tool
.eslintrc.translation.js            # Prevention rules
```

## 📊 **System Status**

**Current State** (Post KEY-258/KEY-259):
- ✅ **4,492 active translation calls**
- ✅ **24 translation namespaces**
- ✅ **99%+ coverage** (EN/FR complete)
- ✅ **Single unified system**
- ✅ **Zero regression risk**

**Supported Languages**:
- ✅ **English (EN)** - Complete
- ✅ **French (FR)** - Complete  
- ⚠️ **German (DE)** - Partial
- ⚠️ **Spanish (ES)** - Partial

## 🔗 **Need More Help?**

- **Full Guide**: `docs/guides/translation-system-guide.md`
- **Implementation Details**: `docs/implementation/learnings/2025-01-16-KEY-259-translation-fix-implementation.md`
- **Linear Tasks**: KEY-258 (standardization), KEY-259 (regression fix)
- **Example Usage**: `components/navigation/side-navigation.tsx` 