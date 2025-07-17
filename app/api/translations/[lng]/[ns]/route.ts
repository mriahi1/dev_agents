import fs from 'fs';
import path from 'path';
import { NextRequest, NextResponse } from 'next/server';

import { logger } from '@/lib/utils/logger';

// Supported locales and namespaces
const SUPPORTED_LOCALES = ['en', 'fr', 'es', 'de'];
const VALID_NAMESPACES = [
  'common',
  'dashboard',
  'properties',
  'tenants',
  'invoices',
  'forms',
  'leases',
  'expenses',
  'budget',
  'reports',
  'tasks',
  'landlords',
  'financing',
  'accounting',
  'calendar',
  'contacts',
  'email',
  'files',
  'productivity',
  'marketing',
  'marketplace',
  'signup',
  'login',
  'demo',
  'finance',
];

export async function GET(
  request: NextRequest,
  { params }: { params: { lng: string; ns: string } }
) {
  const { lng: locale, ns: namespace } = params;

  // Debug info
  logger.info('Translation request', { locale, namespace });

  // Validate locale
  if (!locale || !SUPPORTED_LOCALES.includes(locale)) {
    logger.error('Invalid locale requested', { locale });
    return NextResponse.json({ error: 'Invalid locale' }, { status: 400 });
  }

  // Validate namespace
  if (!namespace || !VALID_NAMESPACES.includes(namespace)) {
    logger.error('Invalid namespace requested', { namespace });
    return NextResponse.json({ error: 'Invalid namespace' }, { status: 400 });
  }

  try {
    // Construct the path to the translation file
    const translationsPath = path.join(
      process.cwd(),
      'public',
      'locales',
      locale,
      `${namespace}.json`
    );

    // Check if the file exists
    if (!fs.existsSync(translationsPath)) {
      logger.warn('Translation file not found', {
        locale,
        namespace,
        path: translationsPath,
      });
      return NextResponse.json({ error: 'Translation file not found' }, { status: 404 });
    }

    // Read the translation file
    const translationData = fs.readFileSync(translationsPath, 'utf8');
    const translations = JSON.parse(translationData);

    logger.debug('Translation file loaded successfully', {
      locale,
      namespace,
      keysCount: Object.keys(translations).length,
    });

    // Set cache headers - cache for 1 hour in production, no cache in development
    const headers = new Headers();
    if (process.env.NODE_ENV === 'production') {
      headers.set('Cache-Control', 'public, max-age=3600, s-maxage=3600');
    } else {
      headers.set('Cache-Control', 'no-store, max-age=0');
    }

    logger.info('Successfully returned translations', { locale, namespace });
    return NextResponse.json(translations, { headers });
  } catch (error) {
    if (error instanceof SyntaxError) {
      logger.error('Invalid JSON in translation file', error, {
        locale,
        namespace,
      });
      return NextResponse.json({ error: 'Invalid JSON in translation file' }, { status: 500 });
    }

    const accessError = error as NodeJS.ErrnoException;
    if (accessError.code === 'ENOENT') {
      logger.warn('Translation file not found', {
        locale,
        namespace,
        errorCode: accessError.code,
      });
      return NextResponse.json({ error: 'Translation file not found' }, { status: 404 });
    }

    if (accessError.code === 'EACCES') {
      logger.error('Permission denied accessing translation file', error, {
        locale,
        namespace,
        errorCode: accessError.code,
      });
      return NextResponse.json({ error: 'Permission denied' }, { status: 500 });
    }

    logger.error('Error loading translation file', error, {
      locale,
      namespace,
    });
    return NextResponse.json({ error: 'Failed to load translations' }, { status: 500 });
  }
} 