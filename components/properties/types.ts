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

// Common tab component props pattern
export interface PropertyTabProps {
  property: Property | null;
  propertyId: number;
  className?: string;
}

// Filter options for consistent filtering across tabs
export interface FilterOptions {
  statuses: Array<{ value: string; label: string }>;
  types: Array<{ value: string; label: string }>;
  categories?: Array<{ value: string; label: string }>;
}

// Standard loading/error/empty state props
export interface TabStateProps {
  isLoading?: boolean;
  error?: string | null;
  isEmpty?: boolean;
  emptyMessage?: string;
} 