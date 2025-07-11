# Meticulous.ai Integration Task

**Linear Task**: [KEY-251](https://linear.app/team/issue/KEY-251)  
**Status**: Ready for Dev  
**Type**: Integration

## Overview

Implement Meticulous.ai to automatically capture user actions and network requests during sessions for automated test generation and maintenance. This integration will help keep tests up to date as the application changes and ensure coverage of edge cases.

## Implementation Details

### Script Integration

Add the following script tag to your `/app/layout.tsx` or `/app/layout.jsx` file within the `<head>` tag:

```tsx
<head>
  ...
  {(process.env.NODE_ENV === "development" || process.env.VERCEL_ENV === "preview") && (
    // eslint-disable-next-line @next/next/no-sync-scripts
    <script
      data-recording-token="o3azQ3wyHxv1eOmsBAo8oB1bhTMQTmn0QCHUOMfS"
      data-is-production-environment="false"
      src="https://snippet.meticulous.ai/v1/meticulous.js"
    />
  )}
  ...
</head>
```

### Configuration

- **Recording Token**: `o3azQ3wyHxv1eOmsBAo8oB1bhTMQTmn0QCHUOMfS`
- **Script URL**: `https://snippet.meticulous.ai/v1/meticulous.js`
- **Production Environment Flag**: `false` (for development/preview only)

## Implementation Steps

1. **Locate Layout File**
   - Find your app's main layout file (`/app/layout.tsx` or `/app/layout.jsx`)
   - If no `<head>` tag exists, add one within the `<body>` tag

2. **Add Conditional Script**
   - Add the Meticulous script with environment conditionals
   - Ensure it only loads in development and preview environments
   - Add ESLint disable comment for sync scripts

3. **Configure Environment Detection**
   - Use `process.env.NODE_ENV === "development"` for local development
   - Use `process.env.VERCEL_ENV === "preview"` for Vercel preview deployments
   - Ensure production builds exclude the script

4. **Test Integration**
   - Verify script loads in development environment
   - Check that recording sessions are captured
   - Confirm no impact on production builds

## Acceptance Criteria

- [ ] Script tag added to layout file with proper conditional logic
- [ ] Only loads in development and preview environments  
- [ ] Recording token properly configured
- [ ] No console errors or warnings
- [ ] ESLint rules updated if needed (no-sync-scripts)
- [ ] No impact on production bundle size
- [ ] Sessions are successfully recorded in Meticulous dashboard

## Benefits

1. **Automated Test Maintenance**: Tests automatically update as your application changes
2. **Edge Case Coverage**: Captures real user interactions and edge cases
3. **Network Request Recording**: Records and replays network requests/responses
4. **Continuous Testing**: Maintains test coverage through ongoing user sessions
5. **No Manual Test Writing**: Reduces time spent writing and maintaining tests

## Security Considerations

- Script only loads in non-production environments
- Recording token should not be exposed in production builds
- Ensure sensitive data is not captured in recordings
- Review Meticulous.ai privacy settings for compliance

## Resources

- [Meticulous.ai Documentation](https://meticulous.ai/docs)
- [Next.js Script Optimization](https://nextjs.org/docs/app/api-reference/components/script)
- [Environment Variables in Next.js](https://nextjs.org/docs/app/building-your-application/configuring/environment-variables) 