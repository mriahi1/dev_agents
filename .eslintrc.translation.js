module.exports = {
  /**
   * ESLint Configuration for Translation System
   * 
   * Prevents hardcoded strings and enforces translation usage.
   * Part of Phase 2 implementation for durable translation fixes.
   */
  
  extends: [
    // Base configuration would go here
  ],
  
  rules: {
    /**
     * Prevent hardcoded strings in JSX
     * Catches: <div>Dashboard</div>, <span>Properties</span>
     */
    'react/jsx-no-literals': [
      'error',
      {
        noStrings: true,
        allowedStrings: [
          // Allow common non-translatable strings
          ' ',     // spaces
          '-',     // dashes
          '/',     // slashes
          '|',     // pipes
          '•',     // bullets
          '...',   // ellipsis
        ],
        ignoreProps: [
          // Props that don't need translation
          'className',
          'id',
          'key',
          'data-testid',
          'aria-label',
          'role',
          'type',
          'href',
          'src',
          'alt',
          'placeholder', // Let specific placeholder rules handle this
        ],
      },
    ],

    /**
     * Prevent hardcoded strings in function calls
     * Catches: toast.success("Property saved"), alert("Error occurred")
     */
    'no-literal-strings': [
      'error',
      {
        // Allow certain function calls with strings
        allowedCalls: [
          'console.log',
          'console.error',
          'console.warn',
          'console.info',
          'require',
          'import',
        ],
        // Allow certain object properties
        allowedProperties: [
          'className',
          'id',
          'key',
          'data-testid',
          'role',
          'type',
          'href',
          'src',
        ],
      },
    ],

    /**
     * Require translation keys to follow naming convention
     * Ensures: t('namespace.key') format
     */
    'translation-key-format': [
      'error',
      {
        pattern: '^[a-z]+\\.[a-zA-Z.]+$',
        message: 'Translation keys must follow "namespace.key" format (e.g., "dashboard.title")',
      },
    ],

    /**
     * Warn about missing useTranslation hook
     * When t() function is used but hook is not imported
     */
    'missing-translation-hook': [
      'warn',
      {
        message: 'Components using t() must import useTranslation hook',
      },
    ],

    /**
     * Enforce TRANSLATION_KEYS constant usage
     * Prefer: t(TRANSLATION_KEYS.DASHBOARD.TITLE)
     * Over: t('dashboard.title')
     */
    'prefer-translation-constants': [
      'warn',
      {
        message: 'Use TRANSLATION_KEYS constants instead of hardcoded key strings',
      },
    ],
  },

  // Custom rule implementations
  plugins: ['@translation-rules'],

  settings: {
    'translation-rules': {
      // Allowed hardcoded strings (emergency exceptions)
      allowedStrings: [
        // Development/debug strings
        'TODO',
        'FIXME',
        'DEBUG',
        
        // Common UI symbols that don't need translation
        '×',     // close symbol
        '▼',     // dropdown arrow
        '✓',     // checkmark
        '!',     // exclamation
        '?',     // question mark
        
        // Date/time formats (handled by i18n libraries)
        'YYYY-MM-DD',
        'HH:mm',
        'MMM DD, YYYY',
        
        // API/technical strings
        'GET',
        'POST',
        'PUT',
        'DELETE',
        'application/json',
        'text/html',
        
        // Component lifecycle (React specific)
        'beforeMount',
        'mounted',
        'beforeUpdate',
        'updated',
      ],
      
      // Translation key patterns
      translationKeyPattern: '^[a-z][a-zA-Z]*\\.[a-z][a-zA-Z.]*$',
      
      // Required imports for translation usage
      requiredImports: {
        'react-i18next': ['useTranslation'],
        '@/lib/constants/translation-keys': ['TRANSLATION_KEYS'],
      },
    },
  },

  overrides: [
    {
      // More lenient rules for test files
      files: ['**/*.test.{ts,tsx}', '**/*.spec.{ts,tsx}', '**/__tests__/**/*'],
      rules: {
        'react/jsx-no-literals': 'off',
        'no-literal-strings': 'off',
        'translation-key-format': 'off',
      },
    },
    
    {
      // Allow hardcoded strings in configuration files
      files: ['*.config.{js,ts}', '*.conf.{js,ts}', '.eslintrc.{js,ts}'],
      rules: {
        'no-literal-strings': 'off',
      },
    },
    
    {
      // Strict mode for main application files
      files: ['src/**/*.{ts,tsx}', 'app/**/*.{ts,tsx}', 'pages/**/*.{ts,tsx}'],
      rules: {
        'react/jsx-no-literals': 'error',
        'no-literal-strings': 'error',
        'translation-key-format': 'error',
        'missing-translation-hook': 'error',
        'prefer-translation-constants': 'error',
      },
    },
  ],

  // Example of how to create custom rules (would be in separate plugin)
  /*
  rules: {
    'translation-key-format': function(context) {
      return {
        CallExpression(node) {
          if (
            node.callee.name === 't' &&
            node.arguments.length > 0 &&
            node.arguments[0].type === 'Literal'
          ) {
            const key = node.arguments[0].value;
            if (typeof key === 'string' && !key.includes('.')) {
              context.report({
                node: node.arguments[0],
                message: 'Translation key must include namespace (e.g., "dashboard.title")',
              });
            }
          }
        },
      };
    },
  },
  */
}; 