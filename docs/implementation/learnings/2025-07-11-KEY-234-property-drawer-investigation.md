# Learning Entry: KEY-234 - Property Drawer Investigation Plan

**Date**: 2025-07-11
**Task**: KEY-234 - Property drawer does not load data  
**Status**: Investigation Plan Created
**Outcome**: Pending implementation in keysy3 frontend

## Situation Analysis

### Context
- KEY-234 is reported in the keysy3 frontend application (`keysylabs/keysy_front3`)
- This dev_agents repository contains documentation and tooling, not the actual frontend code
- Need to investigate and fix the issue in the actual keysy3 repository

### Problem Description
Property drawer component on the properties page fails to load data when opened. Based on the Jam.dev report, users see an empty drawer instead of property details.

## Investigation Plan

### Phase 1: Reproduce the Issue
1. **Clone the keysy3 repository**
   ```bash
   git clone https://github.com/keysylabs/keysy_front3.git
   cd keysy_front3
   ```

2. **Set up local environment**
   ```bash
   npm install
   npm run dev
   ```

3. **Navigate to the properties page**
   - URL: `http://localhost:3002/properties` (based on Jam.dev report)
   - Try to open property drawer
   - Confirm the issue exists

### Phase 2: Identify the Component
Based on similar issues in this codebase, likely locations:
- `app/properties/page.tsx` - Main properties page
- `components/properties/PropertyDrawer.tsx` - Drawer component
- `components/ui/drawer.tsx` - Base drawer component
- `lib/hooks/use-property.ts` - Property data hook

### Phase 3: Debug the Data Flow
1. **Check the property drawer component**
   ```typescript
   // Look for patterns like:
   const PropertyDrawer = ({ propertyId, open, onClose }) => {
     const { property, loading, error } = useProperty(propertyId);
     // ...
   }
   ```

2. **Verify the data hook**
   ```typescript
   // Check if useProperty or similar exists
   const useProperty = (propertyId: string) => {
     // Should make API call to fetch property data
     // Check if propertyId is passed correctly
     // Check if API call is made
   }
   ```

3. **Check API calls**
   - Open browser DevTools Network tab
   - Look for API calls to `/api/v1/properties/{id}`
   - Check if calls are made with correct authentication
   - Verify response structure

### Phase 4: Common Issues to Check

#### 1. Component Not Receiving PropertyId
```typescript
// Check if propertyId is passed correctly
<PropertyDrawer 
  propertyId={selectedPropertyId} // Make sure this is set
  open={isDrawerOpen}
  onClose={() => setIsDrawerOpen(false)}
/>
```

#### 2. API Parameter Issues
Based on other issues in this codebase, check for backend API parameter naming:
```typescript
// Backend might expect 'operation' instead of 'property'
// Check if the API call uses correct parameter
const fetchProperty = async (propertyId: string) => {
  const response = await fetch(`/api/v1/properties/${propertyId}`);
  // or maybe: /api/v1/properties?operation=${propertyId}
}
```

#### 3. State Management Issues
```typescript
// Check if drawer state is managed correctly
const [selectedPropertyId, setSelectedPropertyId] = useState<string | null>(null);
const [isDrawerOpen, setIsDrawerOpen] = useState(false);

// Make sure both are set when opening drawer
const handlePropertyClick = (propertyId: string) => {
  setSelectedPropertyId(propertyId);
  setIsDrawerOpen(true);
};
```

#### 4. Hook Dependencies
Check for infinite loop issues similar to KEY-252:
```typescript
// Avoid creating new objects in dependencies
const { property, loading, error } = useProperty(propertyId, {
  // Don't create new objects here
  filters: useMemo(() => ({ ... }), [deps])
});
```

## Expected Fix Approach

### If Component Issue
1. Ensure PropertyDrawer component is properly rendered
2. Check if propertyId prop is passed correctly
3. Verify drawer state management

### If API Issue
1. Check API endpoint and parameters
2. Verify authentication headers
3. Check if backend expects different parameter naming (like `operation`)

### If Hook Issue
1. Check if property data hook is implemented
2. Verify hook is called with correct parameters
3. Check for dependency issues causing infinite loops

## Implementation Steps

1. **Create feature branch**
   ```bash
   git checkout -b fix/KEY-234-property-drawer-data-loading
   ```

2. **Implement fix based on root cause**
   - Fix component integration
   - Fix API calls
   - Fix hook implementation

3. **Test thoroughly**
   - Test with different properties
   - Test loading states
   - Test error states

4. **Create PR**
   ```bash
   gh pr create --title "Fix property drawer data loading issue" \
     --body "Fixes KEY-234..." --base staging
   ```

5. **Update Linear task**
   ```bash
   python -m src.main linear update KEY-234 --state "Done"
   ```

## Learnings from Similar Issues

Based on KEY-252 and other similar issues:
1. **Check for duplicate services** - Multiple API services might exist
2. **Verify parameter naming** - Backend uses `operation` for property filtering
3. **Check component integration** - Components might exist but not be rendered
4. **Test data flow end-to-end** - From API to UI

## Success Criteria
- [ ] Property drawer opens and displays data
- [ ] Loading states work correctly
- [ ] Error states are handled properly
- [ ] Fix works across different properties
- [ ] No console errors or infinite loops

## Next Steps
1. Access the keysy3 frontend repository
2. Follow the investigation plan above
3. Implement the fix based on findings
4. Create PR and update Linear task
5. Document learnings for future similar issues 