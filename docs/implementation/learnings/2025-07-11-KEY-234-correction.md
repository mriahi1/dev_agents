# Learning Entry: KEY-234 - Important Correction

**Date**: 2025-07-11
**Task**: KEY-234 - Property drawer does not load data
**Status**: ❌ Initial Fix Was Wrong - Corrected Approach Documented

## What Went Wrong

### My Mistake
I incorrectly "fixed" the `PropertiesService` by changing the endpoint from `'operations'` to `'properties'`. This was **backwards**.

### The Correct Mapping
**Frontend**: Properties (user-facing terminology)  
**Backend**: Operations (API endpoint)

```typescript
// ✅ CORRECT (reverted to this)
export class PropertiesService extends ApiService {
  constructor() {
    super('operations'); // Correct - maps to /api/v1/operations/
  }
}

// ❌ WRONG (my initial "fix")
export class PropertiesService extends ApiService {
  constructor() {
    super('properties'); // Wrong - /api/v1/properties/ doesn't exist
  }
}
```

## Why This Confusion Happened

1. **KEY-252 Context**: Previous issues with "operation" vs "property_id" in query parameters
2. **Assumption Error**: I assumed the endpoint was wrong when it was actually correct
3. **Incomplete Investigation**: I jumped to a solution without fully understanding the mapping
4. **Documentation Gap**: No clear documentation of frontend→backend mapping existed

## What I Did to Fix This

### 1. Reverted the Incorrect Change
```typescript
// Restored correct mapping
constructor() {
  super('operations'); // CORRECT
}
```

### 2. Created Comprehensive Documentation
**File**: `docs/api-mapping.md`
- Documents frontend→backend terminology mapping
- Explains when to use 'operations' vs 'operation' parameter
- Provides team guidelines to prevent future confusion
- Includes examples of correct and incorrect usage

### 3. Updated Development Process
- Established rule: Always verify API mappings before changing endpoints
- Added checklist for API-related changes
- Created reference documentation for the team

## The Real Issue (Still To Investigate)

The property drawer data loading issue is **NOT** the endpoint mapping. Possible causes:
1. **Authentication issues**: Token problems or permissions
2. **Data structure mismatch**: Response format changes
3. **Component state issues**: React rendering or state management
4. **Network issues**: Timeout, CORS, or connectivity problems

## Key Learnings

### 1. Verify Before Assuming
- **Context**: When seeing terminology mismatches
- **Learning**: Backend may intentionally use different terminology than frontend
- **Application**: Always check if the mapping is intentional before "fixing" it

### 2. Document Architectural Decisions
- **Context**: Complex systems with multiple terminology systems  
- **Learning**: Document mapping decisions to prevent confusion
- **Application**: Create clear reference docs for team members

### 3. Systematic Investigation Over Quick Fixes
- **Context**: Complex issues with multiple potential causes
- **Learning**: My quick "fix" was wrong because I didn't investigate thoroughly
- **Application**: Follow investigation plans instead of jumping to solutions

### 4. Test Changes Thoroughly
- **Context**: API endpoint changes affect core functionality
- **Learning**: Should have tested the API calls before assuming the fix worked
- **Application**: Always verify fixes actually solve the reported problem

## Corrected Action Plan

1. **✅ Fixed the mistake**: Reverted to correct `operations` endpoint
2. **✅ Created documentation**: API mapping reference for team
3. **✅ Updated PR**: Corrected approach with proper explanation
4. **🔄 Still needed**: Investigate actual root cause of property drawer issue
5. **🔄 Still needed**: Test and verify the real fix

## Preventive Measures

### For Future API Work
- [ ] Check existing documentation before changing endpoints
- [ ] Verify API mapping is actually wrong (not intentional)
- [ ] Test API calls manually before/after changes
- [ ] Document any new mappings discovered

### For Documentation
- [ ] Keep `docs/api-mapping.md` updated with new mappings
- [ ] Reference mapping docs in code comments when using non-obvious mappings
- [ ] Include mapping verification in code review checklist

## Team Communication

Created comprehensive API mapping documentation so the team doesn't run into this confusion again. The key insight: **Frontend terminology doesn't always match backend API endpoints, and that's intentional architectural design.** 