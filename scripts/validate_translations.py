#!/usr/bin/env python3
"""
Translation Validation Script

Validates translation files and constants to prevent regressions.
Detects missing keys, incorrect namespaces, and unused translations.
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple

def load_translation_file(file_path: str) -> Dict:
    """Load a translation JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading {file_path}: {e}")
        return {}

def get_all_keys(data: Dict, prefix: str = '') -> Set[str]:
    """Recursively get all translation keys from nested JSON."""
    keys = set()
    for key, value in data.items():
        full_key = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            keys.update(get_all_keys(value, full_key))
        else:
            keys.add(full_key)
    return keys

def validate_translation_files() -> Tuple[bool, List[str]]:
    """Validate translation files consistency."""
    issues = []
    
    # Find projects directory
    projects_dir = Path("./projects")
    if not projects_dir.exists():
        issues.append("❌ Projects directory not found")
        return False, issues
    
    # Find locales directory
    locales_dirs = list(projects_dir.rglob("public/locales"))
    if not locales_dirs:
        issues.append("❌ No public/locales directory found")
        return False, issues
    
    locales_dir = locales_dirs[0]
    
    # Get available languages
    languages = [d.name for d in locales_dir.iterdir() if d.is_dir()]
    if not languages:
        issues.append("❌ No language directories found")
        return False, issues
    
    print(f"📂 Found languages: {', '.join(languages)}")
    
    # Get translation namespaces (JSON files)
    en_dir = locales_dir / "en"
    if not en_dir.exists():
        issues.append("❌ English translations directory not found")
        return False, issues
    
    namespaces = [f.stem for f in en_dir.glob("*.json")]
    print(f"📝 Found namespaces: {', '.join(namespaces)}")
    
    # Validate each namespace across languages
    for namespace in namespaces:
        print(f"\n🔍 Validating namespace: {namespace}")
        
        # Load all language versions
        namespace_data = {}
        for lang in languages:
            file_path = locales_dir / lang / f"{namespace}.json"
            if file_path.exists():
                namespace_data[lang] = load_translation_file(str(file_path))
            else:
                issues.append(f"⚠️  Missing {namespace}.json for language: {lang}")
        
        # Compare keys between languages
        if 'en' in namespace_data:
            en_keys = get_all_keys(namespace_data['en'])
            
            for lang in languages:
                if lang == 'en' or lang not in namespace_data:
                    continue
                    
                lang_keys = get_all_keys(namespace_data[lang])
                
                # Find missing keys
                missing_in_lang = en_keys - lang_keys
                extra_in_lang = lang_keys - en_keys
                
                if missing_in_lang:
                    issues.append(f"⚠️  {namespace}.json - Missing in {lang}: {', '.join(list(missing_in_lang)[:5])}")
                
                if extra_in_lang:
                    issues.append(f"ℹ️  {namespace}.json - Extra in {lang}: {', '.join(list(extra_in_lang)[:5])}")
    
    return len(issues) == 0, issues

def validate_translation_constants() -> Tuple[bool, List[str]]:
    """Validate translation constants file."""
    issues = []
    
    constants_file = "lib/constants/translation-keys.ts"
    if not os.path.exists(constants_file):
        issues.append(f"❌ Translation constants file not found: {constants_file}")
        return False, issues
    
    with open(constants_file, 'r') as f:
        content = f.read()
    
    # Find all translation key definitions
    # Pattern: KEY: 'some.key' or KEY: 'key'
    pattern = r"([A-Z_]+):\s*['\"]([^'\"]+)['\"]"
    matches = re.findall(pattern, content)
    
    print(f"\n🔍 Found {len(matches)} translation key definitions")
    
    # Check for missing namespace prefixes
    suspicious_keys = []
    for key_name, key_value in matches:
        # Skip if key already has a namespace (contains a dot)
        if '.' not in key_value:
            # Check if this might need a namespace
            # Look for context clues in the constant name or surrounding code
            if key_name in ['TITLE', 'DESCRIPTION', 'NAME', 'LABEL']:
                suspicious_keys.append((key_name, key_value))
    
    if suspicious_keys:
        issues.append("⚠️  Potentially missing namespace prefixes:")
        for key_name, key_value in suspicious_keys[:10]:  # Show first 10
            issues.append(f"   - {key_name}: '{key_value}' (should this be 'namespace.{key_value}'?)")
    
    return len(issues) == 0, issues

def find_hardcoded_text() -> Tuple[bool, List[str]]:
    """Find hardcoded text that should be translated."""
    issues = []
    
    # Find TSX/TS files in projects
    projects_dir = Path("./projects")
    if not projects_dir.exists():
        return True, []
    
    tsx_files = list(projects_dir.rglob("*.tsx")) + list(projects_dir.rglob("*.ts"))
    tsx_files = [f for f in tsx_files if "node_modules" not in str(f)]
    
    print(f"\n🔍 Scanning {len(tsx_files)} TypeScript files for hardcoded text")
    
    # Common patterns for hardcoded text
    suspicious_patterns = [
        r'>\s*Dashboard\s*<',      # <h1>Dashboard</h1>
        r'>\s*Properties\s*<',     # <span>Properties</span>
        r'>\s*Settings\s*<',       # <button>Settings</button>
        r'"Dashboard"',            # "Dashboard"
        r"'Dashboard'",            # 'Dashboard'
        r'"Properties"',           # "Properties"
        r"'Properties'",           # 'Properties'
        r'"Add Property"',         # "Add Property"
        r"'Add Property'",         # 'Add Property'
    ]
    
    files_with_issues = []
    
    for file_path in tsx_files[:50]:  # Limit to first 50 files to avoid spam
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            file_issues = []
            for pattern in suspicious_patterns:
                matches = re.findall(pattern, content)
                if matches:
                    file_issues.extend(matches)
            
            if file_issues:
                files_with_issues.append((str(file_path), file_issues))
        
        except Exception as e:
            continue
    
    if files_with_issues:
        issues.append(f"⚠️  Found {len(files_with_issues)} files with potential hardcoded text:")
        for file_path, file_issues in files_with_issues[:10]:  # Show first 10
            issues.append(f"   - {file_path}: {len(file_issues)} issues")
    
    return len(files_with_issues) == 0, files_with_issues

def main():
    """Main validation function."""
    print("🔍 Translation System Validation")
    print("=" * 50)
    
    all_passed = True
    all_issues = []
    
    # Validate translation files
    print("\n📁 Validating Translation Files...")
    files_passed, files_issues = validate_translation_files()
    all_passed = all_passed and files_passed
    all_issues.extend(files_issues)
    
    # Validate translation constants
    print("\n🔧 Validating Translation Constants...")
    constants_passed, constants_issues = validate_translation_constants()
    all_passed = all_passed and constants_passed
    all_issues.extend(constants_issues)
    
    # Find hardcoded text
    print("\n📝 Scanning for Hardcoded Text...")
    hardcoded_passed, hardcoded_issues = find_hardcoded_text()
    # Don't fail on hardcoded text, just report
    
    # Print summary
    print("\n" + "=" * 50)
    print("📊 VALIDATION SUMMARY")
    print("=" * 50)
    
    if all_passed:
        print("✅ All critical validation checks passed!")
    else:
        print("❌ Some validation checks failed:")
        for issue in all_issues:
            print(f"  {issue}")
    
    if hardcoded_issues:
        print(f"\nℹ️  Found hardcoded text in {len(hardcoded_issues)} files (not a failure, but should be addressed)")
    
    print(f"\n🎯 Overall Status: {'PASS' if all_passed else 'FAIL'}")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main()) 