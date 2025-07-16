/**
 * Translation Keys Constants
 * 
 * Centralized constants for all translation keys used in the application.
 * These keys MUST match the actual structure in the translation JSON files.
 * 
 * Usage:
 * import { TRANSLATION_KEYS } from '@/lib/constants/translation-keys';
 * const title = t(TRANSLATION_KEYS.NAVIGATION.DASHBOARD);
 */

export const TRANSLATION_KEYS = {
  // Main Navigation (from common.json)
  NAVIGATION: {
    DASHBOARD: 'navigation.dashboard',
    PROPERTIES: 'navigation.properties',
    TENANTS: 'navigation.tenants',
    LEASES: 'navigation.leases',
    EXPENSES: 'navigation.expenses',
    BUDGET: 'navigation.budget',
    REPORTS: 'navigation.reports',
    TASKS: 'navigation.tasks',
    CALENDAR: 'navigation.calendar',
    CONTACTS: 'navigation.contacts',
    EMAIL: 'navigation.email',
    FILES: 'navigation.files',
    AI_MARKETING: 'navigation.ai-marketing',
    MARKETPLACE: 'navigation.marketplace',
    APPS: 'navigation.apps',
    LANDLORDS: 'navigation.landlords',
    ACCOUNTING: 'navigation.accounting',
    SETTINGS: 'navigation.settings',
    SUPPORT: 'navigation.support',
    LANGUAGE: 'navigation.language',
    LOGOUT: 'navigation.logout',
    BACK: 'navigation.back',
    MORTGAGES: 'navigation.mortgages',
    MILLIEMES: 'navigation.milliemes',
    METERS: 'navigation.meters',
    TICKETS: 'navigation.tickets',
    INVOICES: 'navigation.invoices',
  },

  // Common Actions (from common.json)
  ACTIONS: {
    SAVE: 'actions.save',
    CANCEL: 'actions.cancel',
    DELETE: 'actions.delete',
    EDIT: 'actions.edit',
    ADD: 'actions.add',
    CREATE: 'actions.create',
    UPDATE: 'actions.update',
    REMOVE: 'actions.remove',
    VIEW: 'actions.view',
    DOWNLOAD: 'actions.download',
    UPLOAD: 'actions.upload',
    SEARCH: 'actions.search',
    FILTER: 'actions.filter',
    SORT: 'actions.sort',
    EXPORT: 'actions.export',
    IMPORT: 'actions.import',
    PRINT: 'actions.print',
    SHARE: 'actions.share',
    COPY: 'actions.copy',
    SUBMIT: 'actions.submit',
    CONFIRM: 'actions.confirm',
    CLOSE: 'actions.close',
    OPEN: 'actions.open',
    REFRESH: 'actions.refresh',
    RESET: 'actions.reset',
  },

  // Settings
  SETTINGS: {
    TITLE: 'settings.title',
    PROFILE: 'settings.profile',
    ACCOUNT: 'settings.account',
    BILLING: 'settings.billing',
    SECURITY: 'settings.security',
    NOTIFICATIONS: 'settings.notifications',
    PREFERENCES: 'settings.preferences',
    API: 'settings.api',
    TEAM: 'settings.team',
    ORGANIZATION: 'settings.organization',
  },

  // AI Marketing (from marketing.json)
  AI_MARKETING: {
    TITLE: 'ai.title',                    // "AI Marketing Studio"
    DESCRIPTION: 'ai.description',        // "Create, publish and analyze..."
    OVERVIEW: 'ai.features.analytics.title',  // Reusing existing key
    CONTENT_GENERATOR: 'ai.features.content.title',
    ANALYTICS: 'ai.features.analytics.title',
  },

  // Dashboard (from dashboard.json)
  DASHBOARD: {
    TITLE: 'dashboard.title',             // "Dashboard" 
    DESCRIPTION: 'dashboard.description', // "Welcome to your property..."
    ADD_PROPERTY: 'dashboard.add_property', // "Add Property"
    PREMIUM_VIEW: 'dashboard.premium_view', // "Premium"
    SETTINGS: 'dashboard.settings',       // Generic settings
  },

  // Property Specific
  PROPERTY: {
    DETAILS: 'property.details',
    OVERVIEW: 'property.overview',
    UNITS: 'property.units',
    TENANTS: 'property.tenants',
    LEASES: 'property.leases',
    DOCUMENTS: 'property.documents',
    FINANCIALS: 'property.financials',
    MAINTENANCE: 'property.maintenance',
    LOCATION: 'property.location',
    METERS: 'property.meters',
    MILLIEMES: 'property.milliemes',
    MARKET_DATA: 'property.marketData',
    // Add Property (from properties.json)
    ADD_PROPERTY: 'addProperty.header',   // Actual key structure
  },

  // Common UI (from common.json)
  UI: {
    LOADING: 'status.loading',            // "Loading..."
    ERROR: 'status.error',                // "An error occurred"
    NO_DATA: 'status.empty',              // "No items found"
    SUCCESS: 'status.success',            // "Success!"
    CATEGORY: 'ui.category',              // "Category"
    FORMAT: 'ui.format',                  // "Format"
    SELECT_PROJECT: 'ui.selectProject',   // "Select a project"
    SELECT_DATA_TYPE: 'ui.selectDataType', // "Select a data type"
    SELECT_FORMAT: 'ui.selectFormat',     // "Select format"
    SELECT_CURRENCY: 'ui.selectCurrency', // "Select currency"
    SELECT_TYPE: 'ui.selectType',         // "Select type"
    SELECT_ENTITY: 'ui.selectEntity',     // "Select primary entity"
  },

  // Placeholders and Form Elements
  PLACEHOLDERS: {
    SEARCH: 'table.noResults',            // Existing key for search
    SELECT_OPTION: 'ui.selectPlaceholder', // Generic select placeholder
    CATEGORY: 'forms.category.placeholder',
    FORMAT: 'forms.format.placeholder',  
    PROJECT: 'forms.project.placeholder',
    DATA_TYPE: 'forms.dataType.placeholder',
    CURRENCY: 'forms.currency.placeholder',
    ACCOUNT_NUMBER: 'forms.accountNumber.placeholder',
  },

  // Validation Messages (from common.json)
  VALIDATION: {
    REQUIRED: 'validation.required',      // "This field is required"
    EMAIL: 'validation.email',            // "Please enter a valid email"
    MIN_LENGTH: 'validation.min',         // "Must be at least {{min}} characters"
    MAX_LENGTH: 'validation.max',         // "Must be at most {{max}} characters"
  },
} as const;

// Export individual sections for convenience
export const NAV_KEYS = TRANSLATION_KEYS.NAVIGATION;
export const ACTION_KEYS = TRANSLATION_KEYS.ACTIONS;
export const PROPERTY_KEYS = TRANSLATION_KEYS.PROPERTY;
export const AI_MARKETING_KEYS = TRANSLATION_KEYS.AI_MARKETING;
export const DASHBOARD_KEYS = TRANSLATION_KEYS.DASHBOARD;
export const UI_KEYS = TRANSLATION_KEYS.UI;
export const SETTINGS_KEYS = TRANSLATION_KEYS.SETTINGS;
export const PLACEHOLDER_KEYS = TRANSLATION_KEYS.PLACEHOLDERS;
export const VALIDATION_KEYS = TRANSLATION_KEYS.VALIDATION; 