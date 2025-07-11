# KEY-234: Property Drawer Data Loading Issue

**Linear Task**: [KEY-234](https://linear.app/team/issue/KEY-234)  
**Type**: Bug  
**Area**: Frontend  
**Priority**: Medium  
**Created**: 2025-07-03  
**Estimate**: 3 story points

## Problem Description

The property drawer does not load data when opened. This appears to be a data fetching or display issue affecting the property drawer component on the properties page.

## Investigation Notes

### Context from Jam.dev Report
- **URL**: http://localhost:3002/properties
- **Browser**: Chrome 137.0.7151.122 (2400x1320) | macOS (arm) 14.6.1
- **Date**: July 3rd 2025 | 12:49pm UTC
- **Debug info**: [jam.dev/c/ceb8360e-c06c-4a63-b7e1-b5e1729445ea](https://jam.dev/c/ceb8360e-c06c-4a63-b7e1-b5e1729445ea)

### Potential Root Causes

1. **Data Fetching Issue**
   - Property drawer API call failing
   - Missing authentication/permissions
   - Incorrect API endpoint or parameters

2. **Component State Issue**
   - Property drawer component not receiving property ID
   - State not updating when drawer opens
   - Missing loading states

3. **Hook Implementation Issue**
   - Property data hook not triggering
   - Dependencies not set correctly
   - Race condition in data loading

4. **Environment-Specific Issue**
   - May only affect localhost:3002
   - Could be missing API configuration
   - Network/CORS issues

## Technical Investigation Steps

1. **Check the Property Drawer Component**
   ```typescript
   // Look for property drawer implementation
   // Likely in app/properties/page.tsx or components/properties/
   ```

2. **Find the Data Hook**
   ```typescript
   // Look for property fetching logic
   const { property, loading, error } = useProperty(propertyId);
   ```

3. **Verify API Response**
   ```bash
   # Check API directly
   curl -H "Authorization: Bearer $TOKEN" \
     "https://api.keysy.co/api/v1/properties/{id}"
   ```

4. **Check Console Errors**
   - Open DevTools on affected page
   - Look for network errors or console warnings
   - Check if property drawer is being triggered

## Related Code Locations

- **Properties Page**: `/app/properties/page.tsx`
- **Property Drawer**: `/components/properties/PropertyDrawer.tsx` (likely)
- **Property Hooks**: `/lib/hooks/use-property.ts` or similar
- **API Service**: `/lib/api/property-service.ts`

## Similar Issues Pattern

This follows the same pattern as other empty data issues:
- [KEY-252: Leases Tab Empty](./KEY-252-leases-tab-empty.md)
- [Empty Tabs Pattern](./empty-tabs-pattern.md)

### Common Solutions
1. Check API parameter naming (e.g., `operation` vs `property_id`)
2. Verify data hooks are properly implemented
3. Check if components are receiving proper props
4. Verify loading/error states are handled

## Testing Approach

1. **Reproduce Locally**
   - Navigate to properties page
   - Try to open property drawer
   - Verify if issue exists locally

2. **Test Different Properties**
   - Try multiple property IDs
   - Check if issue is property-specific or global

3. **Verify Data Exists**
   - Check if properties exist in database
   - Confirm API returns data for specific property

## Acceptance Criteria Checklist

- [ ] Root cause identified with evidence
- [ ] Property drawer loads data correctly
- [ ] Loading states work properly
- [ ] Error handling provides useful feedback
- [ ] Fix works across all environments
- [ ] Include tests to prevent regression

## Fix Approach

Once root cause is identified:

1. **If API Issue**
   - Fix endpoint or API call parameters
   - Ensure proper authentication

2. **If Hook Issue**
   - Update hook to fetch data correctly
   - Handle edge cases and loading states

3. **If Component Issue**
   - Fix component to receive and display data
   - Ensure proper state management

## Action Items

- [x] Create investigation plan and documentation
- [ ] Clone keysy3 frontend repository (keysylabs/keysy_front3)
- [ ] Reproduce the issue locally
- [ ] Identify the property drawer component
- [ ] Debug the data flow (component → hook → API)
- [ ] Implement fix based on root cause
- [ ] Test fix thoroughly
- [ ] Create PR to staging branch
- [ ] Update Linear task with completion

## Next Steps

Since this is a frontend issue in the keysy3 repository (`keysylabs/keysy_front3`), the investigation needs to continue in the actual frontend codebase. 

**Investigation Plan**: See [KEY-234 Investigation Plan](../../implementation/learnings/2025-07-11-KEY-234-property-drawer-investigation.md) for detailed steps.

**Common Patterns**: Based on similar issues (KEY-252, etc.), check for:
- Component integration issues
- API parameter naming (backend expects `operation`)
- Hook dependency problems
- State management issues

## Remember

- Follow pre-PR checklist [[memory:2965613]]
- Target `staging` branch (not main!)
- Document learnings after completion
- Test in the actual reported environment
- Check for parameter naming issues (backend uses `operation` parameter) [[memory:2979217]] 