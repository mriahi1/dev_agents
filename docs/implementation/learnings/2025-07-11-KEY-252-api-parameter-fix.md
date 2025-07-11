# Learning Entry: KEY-252 - Fixing Leases API Parameter Issue

**Date**: 2025-07-11
**Task**: KEY-252 - Leases tab API call missing operation parameter
**Outcome**: Success

## What Happened
User reported that the leases tab still wasn't working. Investigation revealed that while the PropertyLeasesTab was correctly integrated and using the right hook, there was a second lease service making API calls with the wrong parameter name.

## Root Cause Analysis

### Two Different Lease Services
1. **lease-service.ts** - Correctly uses `operation` parameter (used by `usePropertyLeases` hook)
2. **leases-service.ts** - Was using `property_id` parameter instead of `operation`

The backend API expects `operation` for property filtering, not `property_id`. This caused API calls from the second service to not filter by property, returning all leases instead of property-specific ones.

### API Call Comparison
- **Incorrect**: `https://api.keysy.co/api/v1/leases?status=active&page=1&page_size=10`
- **Correct**: `https://api.keysy.co/api/v1/leases?status=active&operation=123&page=1&page_size=10`

## What Went Well
- ✅ Quickly identified the existence of two different lease services
- ✅ Found the exact parameter mismatch causing the issue
- ✅ Simple fix by updating the interface and method

## What Went Wrong
- ❌ Duplicate service implementations causing confusion
- ❌ Inconsistent parameter naming between services
- ❌ No type checking to catch parameter mismatches

## Solution Applied
Updated `leases-service.ts` to use `operation` instead of `property_id`:
1. Changed `LeaseFilters` interface to use `operation` field
2. Updated `getByProperty` method to pass `operation` parameter
3. Added comment explaining backend expectation

## Learnings

1. **Check for Duplicate Services**
   - Context: When debugging API issues
   - Action: Search for multiple implementations of the same service
   - Validation: Ensure consistent parameter naming across services

2. **Backend API Conventions Matter**
   - Context: The keysy3 backend uses `operation` for property filtering
   - Action: Always verify backend parameter expectations
   - Validation: Check actual API calls in network tab

3. **Type Safety Between Services**
   - Context: Multiple services calling same API endpoints
   - Action: Consider shared interfaces for API parameters
   - Validation: TypeScript should catch parameter mismatches

## Action Items
- [x] Fix leases-service.ts to use operation parameter
- [ ] Consider consolidating lease-service.ts and leases-service.ts
- [ ] Add integration tests for lease API calls
- [ ] Document the operation parameter convention

## Related Issues
- Original KEY-252 implementation (missing UI)
- API terminology memory about operation parameter
- Component integration investigation 