#!/usr/bin/env python3
"""
Hardcoded Text Replacement Script

Automatically replaces hardcoded text with translation calls.
Part of Phase 3 implementation for translation system cleanup.
"""

import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Translation replacements mapping
TRANSLATION_REPLACEMENTS = {
    # Dashboard related
    '"Dashboard"': '{t(TRANSLATION_KEYS.DASHBOARD.TITLE)}',
    "'Dashboard'": '{t(TRANSLATION_KEYS.DASHBOARD.TITLE)}',
    '>Dashboard<': '>{t(TRANSLATION_KEYS.DASHBOARD.TITLE)}<',
    
    # Properties related
    '"Properties"': '{t(TRANSLATION_KEYS.NAVIGATION.PROPERTIES)}',
    "'Properties'": '{t(TRANSLATION_KEYS.NAVIGATION.PROPERTIES)}',
    '>Properties<': '>{t(TRANSLATION_KEYS.NAVIGATION.PROPERTIES)}<',
    
    # Settings related
    '"Settings"': '{t(TRANSLATION_KEYS.NAVIGATION.SETTINGS)}',
    "'Settings'": '{t(TRANSLATION_KEYS.NAVIGATION.SETTINGS)}',
    '>Settings<': '>{t(TRANSLATION_KEYS.NAVIGATION.SETTINGS)}<',
    
    # Common actions
    '"Add Property"': '{t(TRANSLATION_KEYS.DASHBOARD.ADD_PROPERTY)}',
    "'Add Property'": '{t(TRANSLATION_KEYS.DASHBOARD.ADD_PROPERTY)}',
    '"Save"': '{t(TRANSLATION_KEYS.ACTIONS.SAVE)}',
    "'Save'": '{t(TRANSLATION_KEYS.ACTIONS.SAVE)}',
    '"Cancel"': '{t(TRANSLATION_KEYS.ACTIONS.CANCEL)}',
    "'Cancel'": '{t(TRANSLATION_KEYS.ACTIONS.CANCEL)}',
    '"Delete"': '{t(TRANSLATION_KEYS.ACTIONS.DELETE)}',
    "'Delete'": '{t(TRANSLATION_KEYS.ACTIONS.DELETE)}',
    '"Edit"': '{t(TRANSLATION_KEYS.ACTIONS.EDIT)}',
    "'Edit'": '{t(TRANSLATION_KEYS.ACTIONS.EDIT)}',
    
    # Navigation items
    '"Tenants"': '{t(TRANSLATION_KEYS.NAVIGATION.TENANTS)}',
    "'Tenants'": '{t(TRANSLATION_KEYS.NAVIGATION.TENANTS)}',
    '"Leases"': '{t(TRANSLATION_KEYS.NAVIGATION.LEASES)}',
    "'Leases'": '{t(TRANSLATION_KEYS.NAVIGATION.LEASES)}',
    '"Expenses"': '{t(TRANSLATION_KEYS.NAVIGATION.EXPENSES)}',
    "'Expenses'": '{t(TRANSLATION_KEYS.NAVIGATION.EXPENSES)}',
    '"Reports"': '{t(TRANSLATION_KEYS.NAVIGATION.REPORTS)}',
    "'Reports'": '{t(TRANSLATION_KEYS.NAVIGATION.REPORTS)}',
}

# Required imports for files that get translation calls
REQUIRED_IMPORTS = [
    "import { useTranslation } from 'react-i18next';",
    "import { TRANSLATION_KEYS } from '@/lib/constants/translation-keys';"
]

def check_imports(content: str) -> Tuple[bool, bool]:
    """Check if required imports are present."""
    has_use_translation = 'useTranslation' in content
    has_translation_keys = 'TRANSLATION_KEYS' in content
    return has_use_translation, has_translation_keys

def add_imports(content: str) -> str:
    """Add required imports to file if missing."""
    lines = content.split('\n')
    
    # Find the last import line
    last_import_idx = -1
    for i, line in enumerate(lines):
        if line.strip().startswith('import ') and 'from ' in line:
            last_import_idx = i
    
    has_use_translation, has_translation_keys = check_imports(content)
    
    # Add missing imports after the last import
    if last_import_idx >= 0:
        new_imports = []
        if not has_use_translation:
            new_imports.append("import { useTranslation } from 'react-i18next';")
        if not has_translation_keys:
            new_imports.append("import { TRANSLATION_KEYS } from '@/lib/constants/translation-keys';")
        
        if new_imports:
            # Insert after last import
            lines[last_import_idx:last_import_idx] = new_imports
    
    return '\n'.join(lines)

def add_translation_hook(content: str) -> str:
    """Add useTranslation hook to component if missing."""
    if 'useTranslation' in content and '= useTranslation(' in content:
        return content  # Already has the hook
    
    # Find component function/export
    patterns = [
        r'export\s+function\s+(\w+)\s*\([^)]*\)\s*\{',
        r'export\s+default\s+function\s+(\w+)\s*\([^)]*\)\s*\{',
        r'const\s+(\w+)\s*=\s*\([^)]*\)\s*=>\s*\{',
        r'function\s+(\w+)\s*\([^)]*\)\s*\{'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, content)
        if match:
            # Insert the hook after the opening brace
            hook_line = "  const { t } = useTranslation();"
            insertion_point = match.end()
            
            # Insert after opening brace, on new line
            content = content[:insertion_point] + '\n' + hook_line + content[insertion_point:]
            break
    
    return content

def fix_file(file_path: Path) -> Tuple[bool, List[str]]:
    """Fix hardcoded text in a single file."""
    changes = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        content = original_content
        
        # Apply translation replacements
        for hardcoded, replacement in TRANSLATION_REPLACEMENTS.items():
            if hardcoded in content:
                content = content.replace(hardcoded, replacement)
                changes.append(f"Replaced {hardcoded} with {replacement}")
        
        # If we made changes, add imports and hooks
        if changes:
            content = add_imports(content)
            content = add_translation_hook(content)
        
        # Write back if changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, changes
        
        return False, []
        
    except Exception as e:
        return False, [f"Error: {e}"]

def find_tsx_files() -> List[Path]:
    """Find all TSX/TS files in the projects directory."""
    projects_dir = Path("./projects")
    if not projects_dir.exists():
        return []
    
    tsx_files = list(projects_dir.rglob("*.tsx")) + list(projects_dir.rglob("*.ts"))
    # Filter out node_modules and test files
    tsx_files = [
        f for f in tsx_files 
        if "node_modules" not in str(f) 
        and "test" not in f.name.lower()
        and ".test." not in f.name
        and ".spec." not in f.name
    ]
    
    return tsx_files

def main():
    """Main function to fix hardcoded text."""
    print("🔧 Hardcoded Text Replacement Tool")
    print("=" * 50)
    
    # Find files to process
    tsx_files = find_tsx_files()
    print(f"📁 Found {len(tsx_files)} TypeScript files to process")
    
    if not tsx_files:
        print("❌ No TypeScript files found in projects directory")
        return 1
    
    # Process files
    fixed_files = []
    total_changes = 0
    
    for file_path in tsx_files:
        print(f"\n🔍 Processing: {file_path}")
        
        changed, changes = fix_file(file_path)
        
        if changed:
            fixed_files.append(file_path)
            total_changes += len(changes)
            print(f"  ✅ Fixed {len(changes)} issues:")
            for change in changes[:3]:  # Show first 3 changes
                print(f"    - {change}")
            if len(changes) > 3:
                print(f"    ... and {len(changes) - 3} more")
        else:
            print(f"  ✨ No hardcoded text found")
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 REPLACEMENT SUMMARY")
    print("=" * 50)
    
    print(f"📁 Files processed: {len(tsx_files)}")
    print(f"🔧 Files modified: {len(fixed_files)}")
    print(f"🔄 Total replacements: {total_changes}")
    
    if fixed_files:
        print(f"\n✅ Successfully fixed hardcoded text in {len(fixed_files)} files:")
        for file_path in fixed_files[:10]:  # Show first 10
            print(f"  - {file_path}")
        if len(fixed_files) > 10:
            print(f"  ... and {len(fixed_files) - 10} more files")
        
        print("\n🎯 Next steps:")
        print("1. Test the modified files")
        print("2. Verify translations display correctly")
        print("3. Commit changes to git")
    else:
        print("\n✨ No hardcoded text found to fix!")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 