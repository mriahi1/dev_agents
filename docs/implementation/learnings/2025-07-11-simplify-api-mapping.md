# Simplifying API Parameter Mapping

## Date: 2025-07-11
## Task: KEY-252 (Code Review Feedback)

### What Happened
After implementing property → operation conversion in the API service layer, received feedback that the comment "This will be converted to 'operation' by the API" was confusing and the approach seemed wrong.

### Initial Approach
```typescript
// In hook:
property: propertyId.toString(), // This will be converted to 'operation' by the API

// In API service:
if (params.property) {
  queryParams.append('operation', params.property); // Convert property to operation
}
```

### Problem
- Unclear where conversion happens ("by the API" is ambiguous)
- Added unnecessary abstraction layer
- Made debugging harder (have to trace through conversion)
- Created confusion about frontend vs backend terminology

### Better Approach
Use backend terminology directly in API-related code:
```typescript
// In hook:
operation: propertyId.toString(), // Backend API expects 'operation' for property filtering

// In API service:
if (params.operation) {
  queryParams.append('operation', params.operation); // Direct pass-through
}
```

### Benefits
1. **Clarity**: Clear what parameter the backend expects
2. **Simplicity**: No conversion layer to maintain
3. **Debuggability**: What you see is what gets sent
4. **Documentation**: Comments explain why, not what transformation happens

### Key Learning
When frontend and backend use different terminology:
- Consider using backend terminology in API layers for clarity
- Document the terminology difference, not the conversion
- Avoid "magic" conversions that hide what's actually happening
- Make the code's intent obvious to future developers

### When to Apply This Pattern
- API integration layers
- Database query builders  
- External service integrations
- Any boundary where terminology differs

### Related
- [[memory:2979217]] - Backend API terminology mapping 