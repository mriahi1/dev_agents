// Core Property Types for the PropertyContext system

// Main Property interface based on existing patterns in the codebase
export interface Property {
  id: number;
  name: string;
  address: string;
  type: string;
  status: string;
  
  // Financial properties
  totalValue?: number;
  monthlyRevenue?: number;
  yearlyRevenue?: number;
  
  // Physical properties  
  totalArea?: number;
  totalUnits?: number;
  
  // Location data
  city?: string;
  postalCode?: string;
  latitude?: number;
  longitude?: number;
  
  // Timestamps
  createdAt?: string;
  updatedAt?: string;
  
  // Extensible for additional fields
  [key: string]: any;
}

// Tab state management interface
export interface PropertyTabState {
  // Active tab tracking
  activeTab: string;
  setActiveTab: (tab: string) => void;
  
  // Sub-tab states (for complex tabs like Meters/Milliemes)
  metersSubTab: string;
  setMetersSubTab: (subTab: string) => void;
  
  milliemesSubTab: string;
  setMilliemesSubTab: (subTab: string) => void;
  
  // Search and filtering states (shared across tabs)
  searchQuery: string;
  setSearchQuery: (query: string) => void;
  
  statusFilter: string;
  setStatusFilter: (status: string) => void;
  
  typeFilter: string;
  setTypeFilter: (type: string) => void;
  
  // Pagination state (shared across tabs)
  currentPage: number;
  setCurrentPage: (page: number) => void;
  
  pageSize: number;
  setPageSize: (size: number) => void;
  
  // Clear all filters helper
  clearFilters: () => void;
}

// Main context state interface
export interface PropertyContextState {
  // Core property data
  property: Property | null;
  propertyId: number;
  isLoading: boolean;
  error: string | null;
  
  // Tab state management
  tabState: PropertyTabState;
  
  // Utility functions
  formatCurrency: (value: number | undefined) => string;
  formatArea: (value: number | undefined) => string;
  formatDate: (date: string | undefined) => string;
  
  // Translation function
  t: (key: string, options?: any) => string;
  
  // Refresh data
  refreshProperty: () => Promise<void>;
}

// Provider props interface
export interface PropertyContextProviderProps {
  children: any; // React.ReactNode equivalent
  propertyId: number;
  initialProperty?: Property | null;
  onPropertyUpdate?: (property: Property | null) => void;
}

// =============================================================================
// STANDARDIZED TAB COMPONENT INTERFACES
// =============================================================================

// Standard tab component props (KEY-275 requirement)
export interface PropertyTabProps {
  property: Property | null;
  propertyId: number;
  className?: string;
  isActive?: boolean;
}

// Enhanced tab props for tabs that need additional context
export interface PropertyTabPropsWithContext extends PropertyTabProps {
  onTabChange?: (tabId: string) => void;
  isLoading?: boolean;
  error?: string | null;
}

// =============================================================================
// FILTER STATE INTERFACES (KEY-275 requirement)
// =============================================================================

// Base filter state structure
export interface FilterState {
  search: string;
  status: string;
  type: string;
  category?: string;
  dateRange?: {
    start?: string;
    end?: string;
  };
}

// Filter actions for reducers/hooks
export interface FilterActions {
  setSearch: (value: string) => void;
  setStatus: (value: string) => void;
  setType: (value: string) => void;
  setCategory?: (value: string) => void;
  setDateRange?: (range: { start?: string; end?: string }) => void;
  clearFilters: () => void;
  resetToDefaults: () => void;
}

// Combined filter state and actions
export interface FilterStateWithActions extends FilterState, FilterActions {}

// Filter configuration for different contexts
export interface FilterConfig {
  statusOptions: FilterOption[];
  typeOptions: FilterOption[];
  categoryOptions?: FilterOption[];
  enableDateRange?: boolean;
  enableSearch?: boolean;
  defaultValues?: Partial<FilterState>;
}

// =============================================================================
// PAGINATION INTERFACES (KEY-275 requirement)
// =============================================================================

// Pagination state
export interface PaginationState {
  currentPage: number;
  pageSize: number;
  totalItems: number;
  totalPages: number;
}

// Pagination actions
export interface PaginationActions {
  goToPage: (page: number) => void;
  goToNextPage: () => void;
  goToPreviousPage: () => void;
  changePageSize: (size: number) => void;
  goToFirstPage: () => void;
  goToLastPage: () => void;
}

// Combined pagination props
export interface PaginationProps extends PaginationState, PaginationActions {
  showSizeOptions?: boolean;
  sizeOptions?: number[];
  showPageInfo?: boolean;
  className?: string;
}

// =============================================================================
// DATA FETCHING AND API INTERFACES
// =============================================================================

// Standard API response structure
export interface ApiResponse<T> {
  data: T;
  success: boolean;
  message?: string;
  error?: string;
}

// Paginated API response
export interface PaginatedApiResponse<T> {
  results: T[];
  count: number;
  next?: string;
  previous?: string;
  page: number;
  pageSize: number;
  totalPages: number;
}

// Loading states for async operations
export interface LoadingState {
  isLoading: boolean;
  isError: boolean;
  error?: string | null;
  isSuccess?: boolean;
}

// =============================================================================
// PROPERTY-SPECIFIC ENTITY INTERFACES
// =============================================================================

// Tenant interface (for PropertyTenantsTab)
export interface Tenant {
  id: number;
  name: string;
  email?: string;
  phone?: string;
  status: 'active' | 'inactive' | 'pending';
  moveInDate?: string;
  moveOutDate?: string;
  leaseId?: number;
  unitId?: number;
  propertyId: number;
}

// Unit interface (for PropertyUnitsTab)
export interface Unit {
  id: number;
  name: string;
  type: 'private' | 'common';
  status: 'occupied' | 'vacant' | 'maintenance' | 'listed';
  area?: number;
  bedrooms?: number;
  bathrooms?: number;
  rooms?: number;
  rent?: number;
  propertyId: number;
  tenantId?: number;
}

// Lease interface (for PropertyLeasesTab)
export interface Lease {
  id: number;
  startDate: string;
  endDate?: string;
  monthlyRent: number;
  deposit?: number;
  status: 'active' | 'expired' | 'terminated' | 'pending';
  tenantId: number;
  unitId: number;
  propertyId: number;
  tenant?: Tenant;
  unit?: Unit;
}

// Document interface (for PropertyDocumentsTab)
export interface Document {
  id: number;
  name: string;
  type: string;
  category: 'contract' | 'invoice' | 'photo' | 'report' | 'permit' | 'other';
  size: number;
  url: string;
  uploadDate: string;
  propertyId: number;
  uploadedBy?: string;
}

// Financial data interface (for PropertyFinancialsTab)
export interface FinancialData {
  id: number;
  type: 'income' | 'expense' | 'investment';
  category: string;
  amount: number;
  date: string;
  description?: string;
  propertyId: number;
}

// =============================================================================
// FORM AND INPUT INTERFACES
// =============================================================================

// Form field configuration
export interface FormField {
  name: string;
  label: string;
  type: 'text' | 'email' | 'number' | 'select' | 'textarea' | 'date' | 'currency';
  required?: boolean;
  placeholder?: string;
  options?: FilterOption[];
  validation?: {
    min?: number;
    max?: number;
    pattern?: string;
    custom?: (value: any) => string | null;
  };
}

// Form state management
export interface FormState<T = Record<string, any>> {
  values: T;
  errors: Record<string, string>;
  touched: Record<string, boolean>;
  isSubmitting: boolean;
  isDirty: boolean;
  isValid: boolean;
}

// =============================================================================
// UI COMPONENT INTERFACES
// =============================================================================

// Filter options for dropdowns and selects
export interface FilterOption {
  value: string;
  label: string;
  count?: number;
  disabled?: boolean;
}

// Statistics card data
export interface StatCard {
  title: string;
  value: string | number;
  icon?: string;
  trend?: {
    value: number;
    direction: 'up' | 'down' | 'neutral';
    period?: string;
  };
  color?: 'primary' | 'success' | 'warning' | 'error' | 'info';
}

// Table column configuration
export interface TableColumn<T = any> {
  key: string;
  label: string;
  sortable?: boolean;
  width?: string;
  align?: 'left' | 'center' | 'right';
  render?: (value: any, item: T) => any;
  className?: string;
}

// Table props
export interface TableProps<T = any> {
  data: T[];
  columns: TableColumn<T>[];
  loading?: boolean;
  error?: string | null;
  emptyMessage?: string;
  onSort?: (key: string, direction: 'asc' | 'desc') => void;
  sortConfig?: {
    key: string;
    direction: 'asc' | 'desc';
  };
  className?: string;
}

// =============================================================================
// STANDARD LOADING/ERROR/EMPTY STATE PROPS
// =============================================================================

// Loading state component props
export interface LoadingStateProps {
  isLoading?: boolean;
  error?: string | null;
  isEmpty?: boolean;
  emptyMessage?: string;
  loadingMessage?: string;
  errorRetryAction?: () => void;
  className?: string;
}

// Tab content wrapper props
export interface TabContentProps extends LoadingStateProps {
  children: any; // React.ReactNode
  title?: string;
  actions?: any; // React.ReactNode
  className?: string;
}

// =============================================================================
// HOOK RETURN TYPES
// =============================================================================

// Standard data fetching hook return type
export interface DataHookReturn<T> extends LoadingState {
  data: T | null;
  refetch: () => Promise<void>;
  mutate?: (data: T) => void;
}

// Paginated data hook return type
export interface PaginatedDataHookReturn<T> extends LoadingState {
  data: T[];
  pagination: PaginationState;
  filters: FilterState;
  setFilters: (filters: Partial<FilterState>) => void;
  setPagination: (pagination: Partial<PaginationState>) => void;
  refetch: () => Promise<void>;
}

// =============================================================================
// SEARCH AND SORT INTERFACES
// =============================================================================

// Search configuration
export interface SearchConfig {
  enabled: boolean;
  placeholder?: string;
  debounceMs?: number;
  minLength?: number;
  searchFields?: string[]; // Fields to search in
}

// Sort configuration
export interface SortConfig {
  key: string;
  direction: 'asc' | 'desc';
}

// Sort actions
export interface SortActions {
  setSortConfig: (config: SortConfig) => void;
  toggleSort: (key: string) => void;
  clearSort: () => void;
}

// =============================================================================
// THEME AND STYLING INTERFACES
// =============================================================================

// Standard size variants
export type SizeVariant = 'xs' | 'sm' | 'md' | 'lg' | 'xl';

// Standard color variants
export type ColorVariant = 'primary' | 'secondary' | 'success' | 'warning' | 'error' | 'info';

// Component variant types
export type ComponentVariant = 'default' | 'outlined' | 'filled' | 'ghost' | 'link';

// =============================================================================
// EVENT HANDLER TYPES
// =============================================================================

// Standard event handlers
export type ClickHandler = () => void;
export type ChangeHandler<T = string> = (value: T) => void;
export type SubmitHandler<T = any> = (data: T) => void | Promise<void>;
export type SelectHandler<T = any> = (item: T) => void;

// =============================================================================
// UTILITY TYPES
// =============================================================================

// Make all properties optional
export type PartialBy<T, K extends keyof T> = Omit<T, K> & Partial<Pick<T, K>>;

// Make specific properties required
export type RequiredBy<T, K extends keyof T> = T & Required<Pick<T, K>>;

// Extract array element type
export type ArrayElement<T> = T extends (infer U)[] ? U : never;

// =============================================================================
// EXPORT GROUPS FOR EASIER IMPORTS
// =============================================================================

// Core property types
export type PropertyTypes = Property | PropertyContextState | PropertyTabState;

// Tab component types  
export type TabTypes = PropertyTabProps | PropertyTabPropsWithContext | TabContentProps;

// Filter and pagination types
export type FilterTypes = FilterState | FilterActions | FilterConfig | PaginationProps;

// Entity types
export type EntityTypes = Tenant | Unit | Lease | Document | FinancialData;

// UI component types
export type UITypes = FilterOption | StatCard | TableColumn | LoadingStateProps; 