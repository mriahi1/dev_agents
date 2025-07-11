# KEY-252 Debugging Guide

**Issue**: Leases tab still not working after API parameter fix

## Current Status
- ✅ PropertyLeasesTab component is properly integrated
- ✅ usePropertyLeases hook is correctly passing `operation` parameter
- ✅ fetchLeases function correctly handles `operation` parameter
- ✅ Leases tab is defined in property detail tabs
- ❌ Still not working in production

## Debugging Steps

### 1. Check Browser Console
Open browser DevTools (F12) and check the Console tab for:
- Component mounting logs: `[PropertyLeasesTab] Component mounted with:`
- Hook debug logs: `[usePropertyLeases] Hook called with:`
- API debug logs: `Sending operation filter to API:`
- Any error messages

### 2. Check Network Tab
In DevTools Network tab, look for:
- API call to `/api/v1/leases` 
- Verify it includes `operation=<propertyId>` parameter
- Check if the API call returns data or errors
- Look for status codes (200, 401, 404, etc.)

### 3. Verify Component Mounting
When clicking the leases tab:
1. Check if PropertyLeasesTab component appears in React DevTools
2. Verify the propertyId prop is passed correctly
3. Check if the usePropertyLeases hook is being called

### 4. Check API Response
If API call is made, check the response:
- Does it return `{ results: [], count: 0 }` (empty)?
- Does it return actual lease data?
- Are there any error messages in the response?

### 5. Test with Different Property
Try the leases tab on different properties to see if:
- Issue is property-specific
- Issue is global across all properties

### 6. Check for Cached Data
- Clear browser cache (Ctrl+Shift+R)
- Try incognito/private mode
- Check if the issue persists

## Potential Issues

### A. Component Not Mounting
**Symptoms**: No debug logs in console
**Solutions**:
- Check if leases tab is actually clickable
- Verify activeTab state is being set to 'leases'
- Check for JavaScript errors preventing rendering

### B. API Call Not Made
**Symptoms**: No network request in DevTools
**Solutions**:
- Check if usePropertyLeases hook is being called
- Verify propertyId is valid (not null/undefined)
- Check for errors in hook initialization

### C. API Call Made But Wrong Parameters
**Symptoms**: API call without `operation` parameter
**Solutions**:
- Check if `operation` parameter is being passed
- Verify propertyId is converted to string properly
- Check for conflicting parameters

### D. API Call Made But No Data
**Symptoms**: API returns empty results
**Solutions**:
- Check if property actually has leases in database
- Verify API endpoint is correct
- Check authentication/permissions

### E. API Call Made But Error Response
**Symptoms**: API returns error status
**Solutions**:
- Check for 401 (authentication) errors
- Check for 404 (endpoint not found) errors
- Check for 500 (server) errors

## Quick Test Commands

### Console Commands to Test
```javascript
// Test if component is mounted
document.querySelector('[data-testid="property-leases-tab"]') || 
document.querySelector('.property-leases-tab') || 
'PropertyLeasesTab not found'

// Test API call manually
fetch('/api/v1/leases?operation=123&page=1&page_size=10', {
  headers: {
    'Authorization': 'Bearer ' + localStorage.getItem('token')
  }
}).then(r => r.json()).then(console.log)
```

## Expected Behavior
When working correctly, you should see:
1. Console log: `[PropertyLeasesTab] Component mounted with: {propertyId: 123, propertyName: "..."}`
2. Console log: `[usePropertyLeases] Hook called with: {propertyId: 123, initialFilters: {...}}`
3. Network request: `GET /api/v1/leases?operation=123&page=1&page_size=10`
4. Either lease data displayed or "No leases found" message

## Next Steps
Based on debugging results:
1. **If no console logs**: Component mounting issue
2. **If no API call**: Hook initialization issue  
3. **If API call but wrong params**: Parameter passing issue
4. **If API call but no data**: Backend/database issue
5. **If API call but error**: Authentication/permission issue

Please share the debugging results so we can identify the exact issue. 