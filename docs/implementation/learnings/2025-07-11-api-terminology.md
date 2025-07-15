# API Terminology Mapping: Property vs Operation

## Date: 2025-07-11
## Task: KEY-252 (Leases Tab Implementation)

### Issue Discovered
During implementation of the leases tab feature, discovered that the backend API uses different terminology than the frontend:
- Frontend typically uses "property" to refer to properties
- Backend API expects "operation" parameter when filtering by property
- Lease objects store the property ID in the "operation" field

### Root Cause
This is an intentional architectural decision where the backend uses more generic terminology that can accommodate different business contexts.

### Implementation Approach
Initially implemented a conversion layer in the API service that translated 'property' to 'operation'. However, this added unnecessary complexity and confusion about where the conversion happened.

**Updated approach**: Use 'operation' directly in frontend code when dealing with API calls, maintaining clarity about what the backend expects.

### Code Example
```typescript
// In hooks that fetch leases by property:
const [filters, setFilters] = useState<LeaseFilterParams>({
  ...initialFilters,
  operation: propertyId.toString(), // Use 'operation' directly - backend expectation
});

// In API service:
if (params.operation && params.operation !== 'all') {
  queryParams.append('operation', params.operation); // Direct pass-through, no conversion
}
```

### Key Learning
When dealing with API terminology mismatches, consider:
1. Using the API's terminology directly in API-related code for clarity
2. Documenting the terminology difference clearly in comments
3. Avoiding conversion layers that can add confusion about where transformations happen

### Action Items
- ✅ Updated lease hooks to use 'operation' directly
- ✅ Removed conversion logic from API service
- ✅ Added clear comments explaining the backend expectation
- Consider standardizing terminology across frontend and backend in the future 