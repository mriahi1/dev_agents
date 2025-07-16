# PropertyContext System

## Overview

The PropertyContext system provides centralized state management for property detail pages, eliminating prop drilling and centralizing common functionality across all property tab components.

## 🎯 Purpose

This addresses **KEY-267: Create Shared Property Context** as the foundational piece for the component extraction pipeline. It enables:

- ✅ **Elimination of prop drilling** across property tab components
- ✅ **Centralized state management** for tab navigation, filtering, and pagination
- ✅ **Shared utility functions** (formatCurrency, formatArea, formatDate)
- ✅ **Consistent data access patterns** across all tab components
- ✅ **Performance optimization** through proper memoization

## 📁 File Structure

```
components/properties/
├── property-context.tsx      # Main context implementation
├── types.ts                  # TypeScript interfaces
├── index.ts                  # Barrel exports
└── README.md                 # This documentation
```

## 🔧 Core Components

### PropertyContextProvider

The main provider component that wraps the property detail page and provides shared state to all child components.

```typescript
import { PropertyContextProvider } from '@/components/properties';

function PropertyDetailPage({ params }: { params: { id: string } }) {
  const propertyId = parseInt(params.id);
  
  return (
    <PropertyContextProvider 
      propertyId={propertyId}
      onPropertyUpdate={(property) => {
        // Handle property updates
        console.log('Property updated:', property);
      }}
    >
      {/* All property tab components go here */}
      <PropertyDetailTabs />
      <PropertyTabContent />
    </PropertyContextProvider>
  );
}
```

### usePropertyContext Hook

Primary hook for accessing all context data and functionality.

```typescript
import { usePropertyContext } from '@/components/properties';

function PropertyDetailsTab() {
  const {
    property,           // Current property data
    propertyId,         // Property ID
    isLoading,          // Loading state
    error,              // Error state
    tabState,           // All tab state management
    formatCurrency,     // Utility functions
    formatArea,
    formatDate,
    t,                  // Translation function
    refreshProperty     // Refresh data
  } = usePropertyContext();
  
  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorMessage error={error} />;
  if (!property) return <NotFound />;
  
  return (
    <div className="space-y-6">
      <h2>{property.name}</h2>
      <p>{formatCurrency(property.totalValue)}</p>
      <p>{formatArea(property.totalArea)}</p>
    </div>
  );
}
```

## 🎛️ Specialized Hooks

### usePropertyTabState - Tab Navigation & Filtering

For components that only need tab state management:

```typescript
import { usePropertyTabState } from '@/components/properties';

function PropertyNavigationTabs() {
  const {
    activeTab,
    setActiveTab,
    searchQuery,
    setSearchQuery,
    statusFilter,
    setStatusFilter,
    currentPage,
    setCurrentPage,
    clearFilters
  } = usePropertyTabState();
  
  return (
    <div>
      <SearchInput 
        value={searchQuery} 
        onChange={setSearchQuery} 
      />
      <FilterDropdown 
        value={statusFilter} 
        onChange={setStatusFilter} 
      />
      <button onClick={clearFilters}>Clear Filters</button>
    </div>
  );
}
```

### usePropertyFormatters - Utility Functions

For components that only need formatting functions:

```typescript
import { usePropertyFormatters } from '@/components/properties';

function PropertyStatisticsCard({ value, area, date }) {
  const { formatCurrency, formatArea, formatDate } = usePropertyFormatters();
  
  return (
    <div className="stats-card">
      <p>Value: {formatCurrency(value)}</p>
      <p>Area: {formatArea(area)}</p>
      <p>Date: {formatDate(date)}</p>
    </div>
  );
}
```

### usePropertyData - Property Data Only

For components that only need property data:

```typescript
import { usePropertyData } from '@/components/properties';

function PropertyHeader() {
  const { property, isLoading, refreshProperty } = usePropertyData();
  
  if (isLoading) return <HeaderSkeleton />;
  
  return (
    <header>
      <h1>{property?.name}</h1>
      <button onClick={refreshProperty}>Refresh</button>
    </header>
  );
}
```

## 🗂️ Tab State Management

The context manages all tab-related state centrally:

### Active Tab Management

```typescript
// Get/set active tab
const { activeTab, setActiveTab } = usePropertyTabState();

// Switch to tenants tab
setActiveTab('tenants');
```

### Sub-Tab Management (for complex tabs)

```typescript
// Meters sub-tabs: water, electricity, gas
const { metersSubTab, setMetersSubTab } = usePropertyTabState();

// Milliemes sub-tabs: general, charges, works
const { milliemesSubTab, setMilliemesSubTab } = usePropertyTabState();
```

### Search & Filtering

```typescript
const {
  searchQuery,      // Current search term
  setSearchQuery,   // Update search
  statusFilter,     // Current status filter
  setStatusFilter,  // Update status filter
  typeFilter,       // Current type filter
  setTypeFilter,    // Update type filter
  clearFilters      // Reset all filters
} = usePropertyTabState();
```

### Pagination

```typescript
const {
  currentPage,      // Current page number
  setCurrentPage,   // Change page
  pageSize,         // Items per page
  setPageSize       // Change page size
} = usePropertyTabState();
```

## 💎 Utility Functions

### Currency Formatting

```typescript
const { formatCurrency } = usePropertyFormatters();

formatCurrency(150000)     // "€150,000"
formatCurrency(1500.50)    // "€1,501"  
formatCurrency(undefined)  // "€0"
```

### Area Formatting

```typescript
const { formatArea } = usePropertyFormatters();

formatArea(125.5)      // "126 m²"
formatArea(1000)       // "1,000 m²"
formatArea(undefined)  // "0 m²"
```

### Date Formatting

```typescript
const { formatDate } = usePropertyFormatters();

formatDate('2023-12-25')   // "25 déc. 2023"
formatDate(undefined)      // "-"
```

## 🎨 Component Patterns

### Standard Tab Component Pattern

```typescript
import { usePropertyContext } from '@/components/properties';
import type { PropertyTabProps } from '@/components/properties';

export function PropertyXxxTab({ className }: PropertyTabProps) {
  const { 
    property, 
    propertyId, 
    isLoading, 
    error,
    tabState: { searchQuery, statusFilter },
    formatCurrency,
    t 
  } = usePropertyContext();
  
  if (isLoading) return <TabLoadingSkeleton />;
  if (error) return <TabError error={error} />;
  if (!property) return <TabNotFound />;
  
  return (
    <div className={`space-y-6 ${className}`}>
      <TabHeader title={t('property.xxx')} />
      <TabContent property={property} />
    </div>
  );
}
```

### Integration with Existing Hooks

```typescript
// Combine context with existing data hooks
function PropertyTenantsTab() {
  const { 
    propertyId, 
    tabState: { searchQuery, statusFilter, currentPage, pageSize } 
  } = usePropertyContext();
  
  // Use existing hooks with context values
  const { tenants, loading, error } = usePropertyTenantsFromLeases({
    propertyId,
    search: searchQuery,
    status: statusFilter,
    page: currentPage,
    pageSize
  });
  
  return (
    <TenantsDisplay 
      tenants={tenants} 
      loading={loading} 
      error={error} 
    />
  );
}
```

## 🚀 Performance Optimizations

### Memoization

All expensive operations are memoized:
- Context value creation
- Tab state object
- Utility functions
- Component re-renders

### Selective Hook Usage

Use specialized hooks to minimize re-renders:

```typescript
// ❌ BAD - Re-renders on any context change
const context = usePropertyContext();

// ✅ GOOD - Only re-renders on tab state changes
const tabState = usePropertyTabState();

// ✅ GOOD - Only re-renders on property data changes  
const { property } = usePropertyData();
```

## 🔄 Migration Guide

### From Prop Drilling to Context

**Before (Prop Drilling):**
```typescript
function PropertyDetailPage({ propertyId }) {
  const [property, setProperty] = useState(null);
  const [activeTab, setActiveTab] = useState('details');
  const [searchQuery, setSearchQuery] = useState('');
  
  const formatCurrency = (value) => { /* ... */ };
  
  return (
    <div>
      <PropertyDetailsTab 
        property={property}
        propertyId={propertyId}
        formatCurrency={formatCurrency}
      />
      <PropertyTenantsTab
        property={property}
        propertyId={propertyId}
        searchQuery={searchQuery}
        setSearchQuery={setSearchQuery}
        formatCurrency={formatCurrency}
      />
    </div>
  );
}
```

**After (Context):**
```typescript
function PropertyDetailPage({ propertyId }) {
  return (
    <PropertyContextProvider propertyId={propertyId}>
      <PropertyDetailsTab />
      <PropertyTenantsTab />
    </PropertyContextProvider>
  );
}

// Components automatically get access to all shared state
function PropertyDetailsTab() {
  const { property, propertyId, formatCurrency } = usePropertyContext();
  // ... component logic
}
```

## 🎯 Benefits

### Developer Experience
- ✅ **No more prop drilling** - Components access data directly
- ✅ **Consistent patterns** - All tabs follow the same structure  
- ✅ **Type safety** - Full TypeScript support with IntelliSense
- ✅ **Performance** - Proper memoization prevents unnecessary re-renders

### Maintenance
- ✅ **Centralized state** - All tab state in one place
- ✅ **Shared utilities** - Formatting functions used consistently
- ✅ **Easy testing** - Mock context for component tests
- ✅ **Scalable** - Easy to add new tabs and functionality

### User Experience  
- ✅ **Consistent behavior** - All tabs behave the same way
- ✅ **Shared state persistence** - Search/filters persist across tabs
- ✅ **Better performance** - Optimized re-rendering

## 🧪 Testing

### Testing Components with Context

```typescript
import { render } from '@testing-library/react';
import { PropertyContextProvider } from '@/components/properties';

function renderWithContext(component, { propertyId = 1, ...options } = {}) {
  return render(
    <PropertyContextProvider propertyId={propertyId}>
      {component}
    </PropertyContextProvider>,
    options
  );
}

// Test a tab component
test('PropertyDetailsTab renders correctly', () => {
  renderWithContext(<PropertyDetailsTab />);
  // ... test assertions
});
```

### Mocking Context

```typescript
import { PropertyContext } from '@/components/properties';

const mockContextValue = {
  property: { id: 1, name: 'Test Property' },
  propertyId: 1,
  isLoading: false,
  error: null,
  // ... other required values
};

test('component with mocked context', () => {
  render(
    <PropertyContext.Provider value={mockContextValue}>
      <YourComponent />
    </PropertyContext.Provider>
  );
});
```

## 🔮 Next Steps

Once this context is implemented, it enables the entire component extraction pipeline:

1. **KEY-275**: TypeScript Interface Cleanup ✅ (types already defined)
2. **KEY-266**: Extract Tab-Specific State ✅ (managed by context)
3. **KEY-264-276**: All tab component extractions (use context pattern)
4. **KEY-268**: Hook optimization (context eliminates many dependency issues)

The PropertyContext serves as the foundation that makes all subsequent component extractions clean and consistent. 