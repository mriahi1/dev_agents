# KEY-252: Leases Tab Empty Issue

**Linear Task**: [KEY-252](https://linear.app/team/issue/KEY-252)  
**Type**: Bug  
**Area**: Frontend  
**Priority**: Medium  
**Created**: 2025-07-11

## Problem Description

The leases tab on the property detail page shows as empty even when properties should have associated lease data. This is similar to the tenants tab issue and may share a common root cause.

## Investigation Notes

### Similar Issues
- **Tenants Tab**: Had similar empty state issue (see PR #21 investigation)
- Both tabs rely on related data (leases contain tenant information)
- May be API/data fetching issue rather than UI issue

### Potential Root Causes

1. **API Not Returning Data**
   - Check if `/api/leases?property={id}` returns data
   - Verify authentication/permissions

2. **Hook Implementation Issue**
   - Look for `usePropertyLeases` or similar hook
   - Check if property ID is passed correctly

3. **Data Filtering Problem**
   - Leases might be filtered out incorrectly
   - Status filters might be too restrictive

4. **Environment-Specific Issue**
   - May only affect preview/staging environments
   - Could be missing test data

## Technical Investigation Steps

1. **Check the Component**
   ```typescript
   // Look in property detail page for leases tab
   // File: app/properties/[id]/page.tsx
   {activeTab === 'leases' && (
     // Leases implementation
   )}
   ```

2. **Find the Data Hook**
   ```typescript
   // Look for lease fetching logic
   const { leases, loading, error } = usePropertyLeases(propertyId);
   ```

3. **Verify API Response**
   ```bash
   # Check API directly
   curl -H "Authorization: Bearer $TOKEN" \
     "https://api.example.com/leases?property=1735"
   ```

4. **Check Console Errors**
   - Open DevTools on affected page
   - Look for network errors or console warnings

## Related Code Locations

- **Property Detail Page**: `/app/properties/[id]/page.tsx`
- **Lease Hooks**: `/lib/hooks/use-leases.ts` or `/lib/hooks/use-property-leases.ts`
- **API Service**: `/lib/api/lease-service.ts`

## Testing Approach

1. **Reproduce Locally**
   - Set up local environment
   - Navigate to property with known leases
   - Verify if issue exists locally

2. **Test Different Properties**
   - Try multiple property IDs
   - Check if issue is property-specific or global

3. **Verify Data Exists**
   - Check database for lease records
   - Confirm test data is properly seeded

## Acceptance Criteria Checklist

- [ ] Identify root cause with evidence
- [ ] Leases display correctly when data exists
- [ ] Empty state only shows for properties without leases
- [ ] Loading states work properly
- [ ] Error handling provides useful feedback
- [ ] Fix works across all environments
- [ ] Include tests to prevent regression

## Fix Approach

Once root cause is identified:

1. **If API Issue**
   - Fix endpoint to return proper data
   - Ensure proper query parameters

2. **If Hook Issue**
   - Update hook to fetch data correctly
   - Handle edge cases properly

3. **If UI Issue**
   - Fix component rendering logic
   - Ensure proper state management

## Remember

- Follow pre-PR checklist
- Target `staging` branch (not main!)
- Document learnings after completion
- Test in the actual reported environment 