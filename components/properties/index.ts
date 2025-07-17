// Property Context and Core System
export { 
  PropertyContextProvider, 
  usePropertyContext,
  usePropertyTabState,
  usePropertyFormatters,
  usePropertyData,
} from './property-context';

// Property Tab Components
export { PropertyFinancialsTab } from './property-financials-tab';
export { PropertyTasksTab } from './property-tasks-tab';

// =============================================================================
// CORE TYPE EXPORTS (organized by category)
// =============================================================================

// Core Property & Context Types
export type {
  Property,
  PropertyContextState,
  PropertyTabState,
  PropertyContextProviderProps,
} from './types';

// Tab Component Interface Exports (KEY-275 requirement)
export type {
  PropertyTabProps,
  PropertyTabPropsWithContext,
  TabContentProps,
} from './types';

// Filter & Pagination Interface Exports (KEY-275 requirement)  
export type {
  FilterState,
  FilterActions,
  FilterStateWithActions,
  FilterConfig,
  PaginationState,
  PaginationActions,
  PaginationProps,
} from './types';

// Entity Type Exports (for specific tab components)
export type {
  Tenant,
  Unit,
  Lease,
  Document,
  FinancialData,
} from './types';

// API & Data Fetching Types
export type {
  ApiResponse,
  PaginatedApiResponse,
  LoadingState,
  DataHookReturn,
  PaginatedDataHookReturn,
} from './types';

// UI Component Types
export type {
  FilterOption,
  StatCard,
  TableColumn,
  TableProps,
  LoadingStateProps,
} from './types';

// Form & Input Types
export type {
  FormField,
  FormState,
} from './types';

// Search & Sort Types
export type {
  SearchConfig,
  SortConfig,
  SortActions,
} from './types';

// Styling & Theme Types
export type {
  SizeVariant,
  ColorVariant,
  ComponentVariant,
} from './types';

// Event Handler Types
export type {
  ClickHandler,
  ChangeHandler,
  SubmitHandler,
  SelectHandler,
} from './types';

// Utility Types
export type {
  PartialBy,
  RequiredBy,
  ArrayElement,
} from './types';

// Grouped Type Exports (for bulk imports)
export type {
  PropertyTypes,
  TabTypes,
  FilterTypes,
  EntityTypes,
  UITypes,
} from './types';

// =============================================================================
// COMPONENT EXPORTS (as they get extracted)
// =============================================================================

// Future tab component exports will go here as they're extracted:
// export { PropertyDetailsTab } from './property-details-tab';
// export { PropertyTenantsTab } from './property-tenants-tab';
// export { PropertyUnitsTab } from './property-units-tab';
// export { PropertyLeasesTab } from './property-leases-tab';
// export { PropertyDocumentsTab } from './property-documents-tab';
// export { PropertyFinancialsTab } from './property-financials-tab';
// export { PropertyMetersTab } from './property-meters-tab';
// export { PropertyMilliemesTab } from './property-milliemes-tab';
// export { PropertyLocationTab } from './property-location-tab';
// export { PropertyMarketDataTab } from './property-market-data-tab';

// =============================================================================
// CONVENIENCE IMPORT EXAMPLES FOR COMMON PATTERNS
// =============================================================================

// Example: For basic property tab component
// import type { Property, PropertyTabProps, LoadingStateProps } from '@/components/properties';

// Example: For tabs with filtering
// import type { FilterState, FilterConfig, FilterOption } from '@/components/properties';

// Example: For tabs with pagination  
// import type { PaginationProps, PaginationState } from '@/components/properties';

// Example: For tabs with entity data
// import type { Tenant, Unit, Lease, Document } from '@/components/properties';

// Example: For UI components
// import type { StatCard, TableColumn, TableProps } from '@/components/properties'; 