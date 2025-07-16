# KEY-259: Translation Keys Regression Audit

**Date**: 2025-01-16  
**Type**: Bug Fix / Translation  
**Priority**: HIGH  
**Reporter**: Staging Issue - dashboard.title & dashboard.description not translating

## 🚨 **Critical Issue Identified**

**Problem**: Dashboard translations not working on staging (https://staging.keysy.co/dashboard)
- `dashboard.title` showing as raw key instead of "Dashboard" / "Tableau de bord"
- `dashboard.description` showing as raw key instead of "Welcome to your property management dashboard"

## 🔍 **Root Cause Analysis**

### **Primary Issue: Incorrect Translation Constants**

**File**: `lib/constants/translation-keys.ts` (Lines 95-103)

```typescript
// ❌ INCORRECT - Missing namespace prefix
DASHBOARD: {
  TITLE: 'title',                       // Should be 'dashboard.title' 
  DESCRIPTION: 'description',           // Should be 'dashboard.description'
  ADD_PROPERTY: 'add_property',         // Should be 'dashboard.add_property'
  PREMIUM_VIEW: 'premium_view',         // Should be 'dashboard.premium_view'
  SETTINGS: 'settings',                 // Should be 'dashboard.settings'
},
```

**Impact**: When components use `t(TRANSLATION_KEYS.DASHBOARD.TITLE)`, they're calling `t('title')` instead of `t('dashboard.title')`, causing translation lookup to fail.

### **Translation Files Are Correct**

✅ **English** (`./projects/keysy3/public/locales/en/dashboard.json`):
```json
{
  "title": "Dashboard",
  "description": "Welcome to your property management dashboard",
  "add_property": "Add Property",
  "premium_view": "Premium",
  ...
}
```

✅ **French** (`./projects/keysy3/public/locales/fr/dashboard.json`):
```json
{
  "title": "Tableau de bord", 
  "description": "Bienvenue dans votre plateforme de gestion immobilière",
  "add_property": "Ajouter une propriété",
  "premium_view": "Premium",
  ...
}
```

## 📊 **System State Assessment**

### **Translation Infrastructure Status**
- ✅ **24 translation namespaces** available in English
- ✅ **Complete FR translations** (dashboard.json has 48 keys)
- ✅ **Proper file structure** (public/locales/en/, public/locales/fr/)
- ✅ **next-i18next** configuration working
- ❌ **Translation constants** have namespace errors

### **Components Affected**
Based on KEY-258 audit findings:
- **4,492 translation calls** across 166 files (mature system)
- **Dashboard components** specifically broken due to constant errors
- **Navigation working** (uses correct `'navigation.dashboard'` format)

## 🎯 **Required Fixes**

### **Immediate Fix (Critical)**

**File**: `lib/constants/translation-keys.ts`

```typescript
// ✅ CORRECT - Add namespace prefix
DASHBOARD: {
  TITLE: 'dashboard.title',             // ✅ Fixed
  DESCRIPTION: 'dashboard.description', // ✅ Fixed  
  ADD_PROPERTY: 'dashboard.add_property',
  PREMIUM_VIEW: 'dashboard.premium_view',
  SETTINGS: 'dashboard.settings',
},
```

### **Secondary Issues to Address**

1. **Similar Namespace Errors**: Audit other sections for missing prefixes
2. **Hardcoded Text**: Continue KEY-258 cleanup work  
3. **Missing Translations**: Add validation to prevent future regressions

## 🔍 **Extended Audit Findings**

### **Other Potential Issues**
From `translation-keys.ts` analysis:

```typescript
// ❌ Potential issue - Check if these need namespace prefixes
AI_MARKETING: {
  TITLE: 'ai.title',                    // ✅ Correct format
  DESCRIPTION: 'ai.description',        // ✅ Correct format
},

SETTINGS: {
  TITLE: 'settings.title',              // ✅ Correct format
},

// ❌ SUSPICIOUS - Need to verify these
PROPERTY: {
  ADD_PROPERTY: 'addProperty.header',   // Mixed casing concern
},
```

### **Files with Hardcoded Text** (From search results)
- `./projects/keysy3/app/ai-marketing/page.tsx`
- `./projects/keysy3/app/settings/access/page.tsx`  
- `./projects/keysy3/app/settings/financial/components/invoicing-tab.tsx`
- Multiple settings pages with likely hardcoded "Settings", "Dashboard", "Properties"

## 📋 **Implementation Plan**

### **Phase 1: Emergency Fix** (Today)
- [ ] Fix dashboard translation constants 
- [ ] Test dashboard translations on staging
- [ ] Verify English/French switching works

### **Phase 2: Validation** (Week 1)
- [ ] Audit all translation constants for namespace errors
- [ ] Create validation script to detect missing prefixes
- [ ] Add TypeScript types for translation key validation

### **Phase 3: Hardcoded Text Cleanup** (Week 2)
- [ ] Complete remaining KEY-258 cleanup tasks
- [ ] Focus on high-visibility components (settings, dashboard)
- [ ] Add ESLint rules to prevent new hardcoded strings

## 🚨 **Risk Assessment**

### **High Risk**
- **Production Impact**: Users seeing raw translation keys instead of text
- **UX Degradation**: Non-English users cannot use dashboard effectively
- **Brand Impact**: Unprofessional appearance on staging/production

### **Low Risk**
- **Technical Implementation**: Simple constant changes, no logic modification
- **Translation Files**: Already complete and correct
- **Rollback**: Easy to revert constant changes

## 🎯 **Success Criteria**

### **Immediate Success**
- [ ] `dashboard.title` displays "Dashboard" (EN) / "Tableau de bord" (FR)
- [ ] `dashboard.description` displays correct welcome message
- [ ] Language switching works on dashboard page

### **Long-term Success**  
- [ ] No translation keys showing as raw strings
- [ ] Validation prevents future regression
- [ ] 99%+ translation coverage maintained

## 🔗 **Related Work**

- **KEY-258**: Translation system standardization (completed audit)
- **Previous Translation Cleanup**: 4,492 calls across 166 files working
- **Translation Constants**: Created but contains namespace errors

## 📝 **Technical Notes**

### **Translation Key Format Standards**
```typescript
// ✅ CORRECT: Include namespace prefix
'namespace.key' → t('dashboard.title', { ns: 'dashboard' })

// ❌ INCORRECT: Missing namespace  
'key' → t('title') // Looks in default namespace only
```

### **Component Usage Pattern**
```typescript
// ✅ How it should work:
import { useTranslation } from 'react-i18next';
import { TRANSLATION_KEYS } from '@/lib/constants/translation-keys';

const { t } = useTranslation('dashboard');
const title = t(TRANSLATION_KEYS.DASHBOARD.TITLE); // 'dashboard.title'
```

## 🔧 **Testing Checklist**

- [ ] English dashboard displays translated text
- [ ] French dashboard displays translated text  
- [ ] Language switcher works correctly
- [ ] No console errors related to missing translations
- [ ] Fallback text works if translation missing
- [ ] Other dashboard elements (add_property, premium_view) working 