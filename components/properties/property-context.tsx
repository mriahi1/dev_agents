'use client';

import React, { createContext, useContext, useMemo, useState, useCallback } from 'react';
import { useNamespaceTranslations } from '@/lib/i18n';

// Core Property Interface (based on learning docs patterns)
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
  // Location
  city?: string;
  postalCode?: string;
  latitude?: number;
  longitude?: number;
  // Timestamps
  createdAt?: string;
  updatedAt?: string;
  // Additional fields as needed by components
  [key: string]: any;
}

// Tab State Management (based on component extraction needs)
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

// Context State Interface
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

// Create the context
const PropertyContext = createContext<PropertyContextState | null>(null);

// Hook to use the context
export const usePropertyContext = () => {
  const context = useContext(PropertyContext);
  if (!context) {
    throw new Error('usePropertyContext must be used within a PropertyContextProvider');
  }
  return context;
};

// Provider Props
interface PropertyContextProviderProps {
  children: React.ReactNode;
  propertyId: number;
  initialProperty?: Property | null;
  onPropertyUpdate?: (property: Property | null) => void;
}

// Provider Component
export const PropertyContextProvider: React.FC<PropertyContextProviderProps> = ({
  children,
  propertyId,
  initialProperty = null,
  onPropertyUpdate,
}) => {
  // Property data state
  const [property, setProperty] = useState<Property | null>(initialProperty);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  
  // Tab state management
  const [activeTab, setActiveTab] = useState<string>('details');
  const [metersSubTab, setMetersSubTab] = useState<string>('water');
  const [milliemesSubTab, setMilliemesSubTab] = useState<string>('general');
  
  // Search and filtering state
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [typeFilter, setTypeFilter] = useState<string>('all');
  
  // Pagination state
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [pageSize, setPageSize] = useState<number>(10);
  
  // Translation hook
  const { t } = useNamespaceTranslations(['properties']);
  
  // Clear all filters helper
  const clearFilters = useCallback(() => {
    setSearchQuery('');
    setStatusFilter('all');
    setTypeFilter('all');
    setCurrentPage(1);
  }, []);
  
  // Tab state object
  const tabState: PropertyTabState = useMemo(() => ({
    activeTab,
    setActiveTab,
    metersSubTab,
    setMetersSubTab,
    milliemesSubTab,
    setMilliemesSubTab,
    searchQuery,
    setSearchQuery,
    statusFilter,
    setStatusFilter,
    typeFilter,
    setTypeFilter,
    currentPage,
    setCurrentPage,
    pageSize,
    setPageSize,
    clearFilters,
  }), [
    activeTab,
    metersSubTab,
    milliemesSubTab,
    searchQuery,
    statusFilter,
    typeFilter,
    currentPage,
    pageSize,
    clearFilters,
  ]);
  
  // Utility functions
  const formatCurrency = useCallback((value: number | undefined): string => {
    if (value === undefined || value === null) return '€0';
    return new Intl.NumberFormat('fr-FR', {
      style: 'currency',
      currency: 'EUR',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value);
  }, []);
  
  const formatArea = useCallback((value: number | undefined): string => {
    if (value === undefined || value === null) return '0 m²';
    return `${value.toLocaleString('fr-FR')} m²`;
  }, []);
  
  const formatDate = useCallback((date: string | undefined): string => {
    if (!date) return '-';
    try {
      return new Intl.DateTimeFormat('fr-FR', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
      }).format(new Date(date));
    } catch {
      return '-';
    }
  }, []);
  
  // Refresh property data
  const refreshProperty = useCallback(async (): Promise<void> => {
    setIsLoading(true);
    setError(null);
    
    try {
      // This would typically call a data fetching hook or API
      // For now, we'll just simulate the interface
      // In actual implementation, this would be:
      // const updatedProperty = await fetchProperty(propertyId);
      // setProperty(updatedProperty);
      // onPropertyUpdate?.(updatedProperty);
      
      console.log(`[PropertyContext] Refreshing property ${propertyId}`);
      // Placeholder for actual implementation
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to refresh property';
      setError(errorMessage);
      console.error('[PropertyContext] Error refreshing property:', err);
    } finally {
      setIsLoading(false);
    }
  }, [propertyId, onPropertyUpdate]);
  
  // Update property when propertyId changes
  React.useEffect(() => {
    if (propertyId && (!property || property.id !== propertyId)) {
      refreshProperty();
    }
  }, [propertyId, property, refreshProperty]);
  
  // Context value
  const contextValue: PropertyContextState = useMemo(() => ({
    property,
    propertyId,
    isLoading,
    error,
    tabState,
    formatCurrency,
    formatArea,
    formatDate,
    t,
    refreshProperty,
  }), [
    property,
    propertyId,
    isLoading,
    error,
    tabState,
    formatCurrency,
    formatArea,
    formatDate,
    t,
    refreshProperty,
  ]);
  
  return (
    <PropertyContext.Provider value={contextValue}>
      {children}
    </PropertyContext.Provider>
  );
};

// Additional utility hooks for specific use cases

// Hook for accessing only tab state (lighter than full context)
export const usePropertyTabState = () => {
  const { tabState } = usePropertyContext();
  return tabState;
};

// Hook for accessing only formatting functions
export const usePropertyFormatters = () => {
  const { formatCurrency, formatArea, formatDate } = usePropertyContext();
  return { formatCurrency, formatArea, formatDate };
};

// Hook for accessing only property data
export const usePropertyData = () => {
  const { property, propertyId, isLoading, error, refreshProperty } = usePropertyContext();
  return { property, propertyId, isLoading, error, refreshProperty };
};

export default PropertyContext; 