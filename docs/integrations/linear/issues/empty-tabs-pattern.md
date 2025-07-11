# Empty Tabs Pattern - Property Detail Page

## Pattern Overview

Multiple tabs on the property detail page are showing empty states when they should display data. This appears to be a systemic issue affecting data fetching or display logic.

## Affected Areas

1. **Tenants Tab** 
   - Reported: Property 1735
   - Uses: `usePropertyTenantsFromLeases` hook
   - Fetches: Tenant data through leases

2. **Leases Tab** ([KEY-252](https://linear.app/team/issue/KEY-252))
   - Reported: General issue
   - Likely uses: `usePropertyLeases` or similar
   - Fetches: Direct lease data

## Common Symptoms

- Tabs show empty state despite data existing
- No error messages displayed
- May work locally but fail in preview/staging
- Affects specific or all properties

## Investigation Checklist

When investigating empty tab issues:

1. **Verify Data Exists**
   ```bash
   # Check API endpoints directly
   curl -H "Authorization: Bearer $TOKEN" "API_URL/endpoint?property=ID"
   ```

2. **Check Hook Implementation**
   - Property ID passed correctly?
   - API parameters correct?
   - Error handling present?

3. **Verify Tab Rendering**
   ```typescript
   // Check if data is reaching the component
   console.log('Data received:', data);
   console.log('Loading state:', loading);
   console.log('Error state:', error);
   ```

4. **Environment Differences**
   - Compare local vs preview/staging
   - Check environment variables
   - Verify API endpoints

## Root Cause Possibilities

### 1. API Configuration
- Different API endpoints per environment
- Missing authentication
- CORS issues

### 2. Data Structure Mismatch
- API returns different structure than expected
- Property ID format differences
- Missing required fields

### 3. React Hook Issues
- Incorrect dependencies
- Race conditions
- Stale closures

### 4. State Management
- Tab state not updating
- Data not persisting between tab switches
- Incorrect initial state

## Recommended Fix Approach

1. **Add Comprehensive Logging**
   ```typescript
   useEffect(() => {
     console.log('[LeaseTab] Fetching for property:', propertyId);
     console.log('[LeaseTab] API params:', params);
   }, [propertyId, params]);
   ```

2. **Implement Proper Error Boundaries**
   ```typescript
   if (error) {
     console.error('[LeaseTab] Error:', error);
     return <ErrorState error={error} />;
   }
   ```

3. **Verify Data Flow**
   - Log at each step from API to UI
   - Check network tab for actual responses
   - Verify data transformations

## Prevention Strategies

1. **Consistent Hook Pattern**
   - Use same error handling across all property tabs
   - Implement standard loading/error states
   - Add retry mechanisms

2. **Testing Requirements**
   - Test with properties that have data
   - Test with properties without data
   - Test in all environments

3. **Monitoring**
   - Add error tracking for failed data fetches
   - Monitor empty state frequency
   - Track which properties are affected

## Related Issues
- Tenants tab empty (PR #21 - didn't fix root cause)
- [KEY-252](https://linear.app/team/issue/KEY-252) - Leases tab empty
- Potential issues with other tabs?

## Action Items
- [ ] Audit all property detail tabs for similar issues
- [ ] Create standard hook pattern for data fetching
- [ ] Add environment-specific testing
- [ ] Implement better error reporting 