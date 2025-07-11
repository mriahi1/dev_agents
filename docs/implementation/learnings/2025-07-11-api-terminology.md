# Learning Entry: API Terminology Mapping

**Date**: 2025-07-11  
**Task**: KEY-252 (Leases Tab)  
**Category**: API Design, Backend Integration

## Key Mapping: Property = Operation [[memory:2979217]]

In the keysy3 system, there's a critical terminology difference between frontend and backend:

- **Frontend**: Uses "property" (what users see)
- **Backend API**: Uses "operation" (internal terminology)

### Examples

```typescript
// Frontend code refers to "property"
const propertyId = 123;

// But API expects "operation"
GET /api/leases?operation=123  // ✅ Correct
GET /api/leases?property=123   // ❌ Won't filter properly

// In lease objects, property ID is stored as:
lease.operation = 123;  // Not lease.property
```

### Code Implementation

The `fetchLeases` function in `lease-service.ts` handles this mapping:

```typescript
// Handle property parameter - API uses 'operation' instead of 'property'
// Frontend: property -> Backend: operation
if (params.property && params.property !== 'all') {
  // Convert 'property' to 'operation' for API compatibility
  queryParams.append('operation', params.property);
}
```

### Impact Areas

1. **Lease filtering** - Must use `operation` parameter
2. **Tenant filtering** - May also use operation terminology
3. **Unit filtering** - Check if similar mapping exists
4. **Any property-related API calls** - Verify parameter naming

### Debugging Tips

If data appears empty when filtering by property:
1. Check if API is receiving `operation` parameter
2. Verify lease objects have `operation` field populated
3. Ensure type matching (number vs string)

### Action Items

- [ ] Document all frontend/backend terminology mappings
- [ ] Create a translation layer or constants file
- [ ] Update API documentation to clarify this mapping
- [ ] Consider standardizing terminology across the stack 