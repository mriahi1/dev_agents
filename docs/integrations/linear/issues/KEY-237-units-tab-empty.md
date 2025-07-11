# KEY-237: Units Tab Empty on Property Detail Page

**Linear Task**: [KEY-237](https://linear.app/team/issue/KEY-237)  
**Type**: Bug  
**Area**: Frontend  
**Priority**: High  
**Created**: 2025-07-03  
**Estimate**: 5 story points

## Problem Description

The units (lots) tab is empty on the property detail page. There used to be a component but it seems like it was misplaced or deleted. This is a critical bug as units are core property functionality.

## Investigation Notes

### Context from Jam.dev Report
- **URL**: http://localhost:3002/properties/1742
- **Browser**: Chrome 137.0.7151.122 (2400x1320) | macOS (arm) 14.6.1
- **Date**: July 3rd 2025 | 1:00pm UTC
- **Debug info**: [jam.dev/c/f8273629-7aec-43db-b70e-21819ff1d2f2](https://jam.dev/c/f8273629-7aec-43db-b70e-21819ff1d2f2)

### Current State Analysis
- Units tab exists in PropertyDetailTabs component
- Tab content area shows empty state
- Component may have been accidentally deleted or misplaced
- Need to investigate what units data should display

### Expected Behavior
- Units tab should display list of property units/lots
- Each unit should show key information (number, type, size, status)
- Should support filtering and sorting
- Should be responsive and accessible

## Technical Investigation Plan

1. **Code Analysis**
   - Check if PropertyUnitsTab component exists
   - Verify tab integration in property detail page
   - Examine data flow and API calls

2. **Component Structure Design**
   - Analyze similar components (leases, tenants)
   - Design unit card layout and information display
   - Plan filtering and sorting capabilities

3. **Implementation Strategy**
   - Create PropertyUnitsTab component if missing
   - Implement unit data fetching
   - Add proper loading and error states
   - Ensure responsive design

## Acceptance Criteria Checklist

- [ ] Issue is reproduced and root cause identified
- [ ] PropertyUnitsTab component exists and functions
- [ ] Units data is properly fetched and displayed
- [ ] Unit cards show relevant information
- [ ] Filtering and sorting work correctly
- [ ] Loading and error states are handled
- [ ] UI changes are responsive and accessible
- [ ] Changes work correctly across major browsers

## Next Steps

1. **Start Investigation**: Analyze current property detail page structure
2. **Identify Missing Component**: Find if PropertyUnitsTab exists
3. **Implement Solution**: Create or restore units tab functionality
4. **Test Integration**: Verify functionality works correctly
5. **Create PR**: Submit for review with testing
6. **Update Linear**: Mark task as complete

## Remember

- Follow pre-PR checklist
- Target `staging` branch (not main!)
- Document learnings after completion
- Test with real property data
- Maintain consistency with existing tabs 