import fs from 'fs';
import path from 'path';
import { NextRequest, NextResponse } from 'next/server';

const SUPPORTED_LOCALES = ['en', 'fr', 'es', 'de'];
const VALID_NAMESPACES = [
  'common', 'dashboard', 'properties', 'tenants', 'invoices', 'forms',
  'leases', 'expenses', 'budget', 'reports', 'tasks', 'productivity',
  'marketing', 'marketplace', 'demo', 'login', 'signup', 'tickets', 'finance',
];

export async function GET(
  request: NextRequest,
  { params }: { params: { locale: string; namespace: string } }
) {
  const { locale, namespace } = params;

  // Validate locale
  if (!locale || !SUPPORTED_LOCALES.includes(locale)) {
    return NextResponse.json({ error: 'Invalid locale' }, { status: 400 });
  }

  // Validate namespace
  if (!namespace || !VALID_NAMESPACES.includes(namespace)) {
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
      return NextResponse.json({ error: 'Translation file not found' }, { status: 404 });
    }

    // Read the translation file
    const translationData = fs.readFileSync(translationsPath, 'utf8');
    const translations = JSON.parse(translationData);

    // Set cache headers - cache for 1 hour in production, no cache in development
    const headers = new Headers();
    if (process.env.NODE_ENV === 'production') {
      headers.set('Cache-Control', 'public, max-age=3600, s-maxage=3600');
    } else {
      headers.set('Cache-Control', 'no-store, max-age=0');
    }

    return NextResponse.json(translations, { headers });
  } catch (error) {
    console.error('Translation API error:', error);
    
    if (error instanceof SyntaxError) {
      return NextResponse.json({ error: 'Invalid JSON in translation file' }, { status: 500 });
    }

    const accessError = error as NodeJS.ErrnoException;
    if (accessError.code === 'ENOENT') {
      return NextResponse.json({ error: 'Translation file not found' }, { status: 404 });
    }

    return NextResponse.json({ error: 'Failed to load translations' }, { status: 500 });
  }
} 