# Learning Entry: React Hook Infinite Loop

**Date**: 2025-07-11  
**Task**: KEY-252 (Leases Tab)  
**Category**: React, Performance, Debugging

## Issue

Infinite loop in PropertyLeasesTab component causing continuous re-renders and API calls.

### Root Cause

The `usePropertyLeases` hook was receiving a new `initialFilters` object on every render:

```typescript
// BAD: Creates new object every render
usePropertyLeases({
  propertyId,
  initialFilters: {
    page: leaseCurrentPage,        // state value
    page_size: leasePageSize,      // state value
    search: leaseSearchQuery,      // state value
    status: leaseStatusFilter,     // state value
  },
});
```

Hook's `useEffect` watches `initialFilters` and updates internal state when it changes, triggering:
1. Component render → new object
2. Hook sees change → updates filters
3. Filters change → fetches data
4. Data updates → component re-renders
5. Loop continues...

## Solution

### Immediate Fix
- Pass only static values to `initialFilters`
- Implement client-side filtering for search/status
- Temporarily disable pagination

### Proper Fix (TODO)
- Modify hook to accept filter update function
- Or create wrapper hook with proper filter management
- Implement server-side filtering API

## Key Learnings

1. **Object Identity Matters in Dependencies**
   - React compares objects by reference, not value
   - New object = new reference = effect triggers

2. **Hook Design Principles**
   - `initialX` props should be truly initial (static)
   - Provide separate methods for updates
   - Don't mix initial and dynamic state

3. **Debugging Infinite Loops**
   - Check `useEffect` dependencies first
   - Look for object/array recreations
   - Use React DevTools Profiler

## Prevention

- Use `useMemo` for object dependencies
- Separate initial config from dynamic state
- Consider `useRef` for values that shouldn't trigger effects
- Design hooks with clear update patterns

## Code Smell Indicators

```typescript
// 🚫 BAD: Dynamic object in hook deps
useCustomHook({
  config: { value: someState }
});

// ✅ GOOD: Static config
const config = useMemo(() => ({ 
  value: someState 
}), [someState]);
useCustomHook({ config });

// ✅ BETTER: Separate update method
const { update } = useCustomHook(staticConfig);
useEffect(() => {
  update({ value: someState });
}, [someState]);
``` 