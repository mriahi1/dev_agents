"""Accessibility analyzer for detecting a11y issues."""

import re
from typing import Dict, List, Any
from pathlib import Path
from loguru import logger


class AccessibilityAnalyzer:
    """Analyzes code for accessibility issues."""
    
    def __init__(self, repo_path: str = "."):
        """Initialize analyzer with repository path."""
        self.repo_path = Path(repo_path)
        
    def analyze_pr_files(self, changed_files: List[str]) -> Dict[str, Any]:
        """Analyze changed files for accessibility issues."""
        all_results = {
            'missing_alt_text': {'status': 'pass', 'issues': 0, 'locations': []},
            'missing_aria_labels': {'status': 'pass', 'issues': 0, 'locations': []},
            'missing_form_labels': {'status': 'pass', 'issues': 0, 'locations': []},
            'color_contrast': {'status': 'pass', 'issues': 0, 'locations': []},
            'interactive_elements': {'status': 'pass', 'issues': 0, 'locations': []},
            'heading_hierarchy': {'status': 'pass', 'issues': 0, 'locations': []},
            'focus_management': {'status': 'pass', 'issues': 0, 'locations': []},
            'semantic_html': {'status': 'pass', 'issues': 0, 'locations': []},
        }
        
        for file in changed_files:
            if not self._should_analyze_file(file):
                continue
                
            file_path = self.repo_path / file
            if not file_path.exists():
                continue
                
            # Run accessibility checks
            file_results = self._analyze_file(file_path)
            
            # Aggregate results
            for check, result in file_results.items():
                if result['issues'] > 0:
                    all_results[check]['issues'] += result['issues']
                    all_results[check]['locations'].extend(
                        [f"{file}:{loc}" for loc in result['locations']]
                    )
        
        # Update statuses and messages
        for check, result in all_results.items():
            if result['issues'] > 0:
                # Accessibility issues are important but usually not blocking
                result['status'] = 'warning'
                result['message'] = self._get_issue_message(check, result['issues'])
            else:
                result['message'] = self._get_pass_message(check)
                
        return all_results
    
    def _should_analyze_file(self, file_path: str) -> bool:
        """Check if file should be analyzed."""
        extensions = ['.tsx', '.jsx']  # Only JSX files have markup
        return any(file_path.endswith(ext) for ext in extensions)
    
    def _analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze a single file for accessibility issues."""
        results = {}
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                lines = content.split('\n')
                
            results['missing_alt_text'] = self._check_missing_alt_text(lines)
            results['missing_aria_labels'] = self._check_missing_aria_labels(lines)
            results['missing_form_labels'] = self._check_missing_form_labels(lines)
            results['color_contrast'] = self._check_color_contrast(lines)
            results['interactive_elements'] = self._check_interactive_elements(lines)
            results['heading_hierarchy'] = self._check_heading_hierarchy(content)
            results['focus_management'] = self._check_focus_management(lines)
            results['semantic_html'] = self._check_semantic_html(lines)
            
        except Exception as e:
            logger.error(f"Error analyzing {file_path}: {e}")
            
        return results
    
    def _check_missing_alt_text(self, lines: List[str]) -> Dict[str, Any]:
        """Check for images missing alt text."""
        locations = []
        
        for i, line in enumerate(lines, 1):
            # Check for img tags without alt
            if '<img' in line and 'alt=' not in line:
                # Make sure it's not a multi-line tag
                if '>' in line or '/>' in line:
                    locations.append(f"line {i}")
                    
            # Check for Next.js Image component without alt
            if '<Image' in line and 'alt=' not in line:
                if '/>' in line:  # Self-closing
                    locations.append(f"line {i}")
                    
        return {'issues': len(locations), 'locations': locations}
    
    def _check_missing_aria_labels(self, lines: List[str]) -> Dict[str, Any]:
        """Check for interactive elements missing ARIA labels."""
        patterns = [
            r'<button[^>]*>(?:(?!aria-label|aria-labelledby|children).)*<\/button>',  # Empty buttons
            r'<a[^>]*><\/a>',                                                         # Empty links
            r'role="button"(?!.*aria-label)',                                        # Role button without label
            r'<IconButton(?!.*aria-label)',                                          # Icon buttons
        ]
        
        locations = []
        for i, line in enumerate(lines, 1):
            # Check for icon-only buttons
            if 'button' in line.lower() and 'icon' in line.lower():
                if 'aria-label' not in line and 'title=' not in line:
                    locations.append(f"line {i} - icon button needs aria-label")
                    
            # Check for empty interactive elements
            for pattern in patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    locations.append(f"line {i}")
                    break
                    
        return {'issues': len(locations), 'locations': locations}
    
    def _check_missing_form_labels(self, lines: List[str]) -> Dict[str, Any]:
        """Check for form inputs missing labels."""
        input_types = ['input', 'select', 'textarea']
        locations = []
        
        for i, line in enumerate(lines, 1):
            for input_type in input_types:
                if f'<{input_type}' in line:
                    # Check if it has label association
                    has_label = any(attr in line for attr in ['aria-label=', 'aria-labelledby=', 'id='])
                    
                    # For hidden inputs, labels aren't needed
                    if 'type="hidden"' in line or 'type=\'hidden\'' in line:
                        continue
                        
                    if not has_label:
                        # Look for associated label in nearby lines
                        label_found = False
                        for j in range(max(0, i-5), min(len(lines), i+5)):
                            if '<label' in lines[j]:
                                label_found = True
                                break
                                
                        if not label_found:
                            locations.append(f"line {i} - {input_type} without label")
                            
        return {'issues': len(locations), 'locations': locations}
    
    def _check_color_contrast(self, lines: List[str]) -> Dict[str, Any]:
        """Check for potential color contrast issues."""
        locations = []
        
        # Look for low contrast color combinations
        low_contrast_patterns = [
            r'color:\s*[\'"]?#[cdefCDEF][0-9a-fA-F]{5}',     # Very light colors
            r'color:\s*[\'"]?#[0-3][0-9a-fA-F]{5}',          # Very dark colors on dark
            r'text-(gray|grey)-(300|400)',                    # Light gray text (Tailwind)
            r'opacity-[0-5]0',                                 # Low opacity text
        ]
        
        for i, line in enumerate(lines, 1):
            for pattern in low_contrast_patterns:
                if re.search(pattern, line):
                    # Check if it's text content
                    if any(text_el in line for text_el in ['<p', '<span', '<div', '<h', '<a']):
                        locations.append(f"line {i} - potential low contrast")
                        break
                        
        return {'issues': len(locations), 'locations': locations}
    
    def _check_interactive_elements(self, lines: List[str]) -> Dict[str, Any]:
        """Check for non-semantic interactive elements."""
        locations = []
        
        for i, line in enumerate(lines, 1):
            # Divs with onClick
            if '<div' in line and 'onClick' in line:
                if 'role=' not in line and 'tabIndex' not in line:
                    locations.append(f"line {i} - div with onClick needs role and tabIndex")
                    
            # Spans with onClick
            if '<span' in line and 'onClick' in line:
                locations.append(f"line {i} - use button instead of span with onClick")
                
            # Missing keyboard handlers
            if 'onMouseDown' in line and 'onKeyDown' not in line:
                locations.append(f"line {i} - mouse event without keyboard equivalent")
                
        return {'issues': len(locations), 'locations': locations}
    
    def _check_heading_hierarchy(self, content: str) -> Dict[str, Any]:
        """Check for proper heading hierarchy."""
        locations = []
        
        # Find all headings
        heading_pattern = re.compile(r'<h([1-6])[^>]*>')
        headings = [(m.group(1), m.start()) for m in heading_pattern.finditer(content)]
        
        if headings:
            # Check if starts with h1
            if headings[0][0] != '1':
                line_num = content[:headings[0][1]].count('\n') + 1
                locations.append(f"line {line_num} - page should start with h1")
                
            # Check for skipped levels
            for i in range(1, len(headings)):
                prev_level = int(headings[i-1][0])
                curr_level = int(headings[i][0])
                
                if curr_level > prev_level + 1:
                    line_num = content[:headings[i][1]].count('\n') + 1
                    locations.append(f"line {line_num} - skipped heading level")
                    
        return {'issues': len(locations), 'locations': locations}
    
    def _check_focus_management(self, lines: List[str]) -> Dict[str, Any]:
        """Check for focus management issues."""
        locations = []
        
        for i, line in enumerate(lines, 1):
            # Check for outline removal without alternative
            if 'outline-none' in line or 'outline: none' in line:
                # Check if there's a focus style
                if 'focus:' not in line and ':focus' not in lines[max(0, i-3):i+3]:
                    locations.append(f"line {i} - outline removed without focus indicator")
                    
            # Check for autofocus on page load
            if 'autoFocus' in line and 'Modal' not in line and 'Dialog' not in line:
                locations.append(f"line {i} - avoid autoFocus on page load")
                
        return {'issues': len(locations), 'locations': locations}
    
    def _check_semantic_html(self, lines: List[str]) -> Dict[str, Any]:
        """Check for non-semantic HTML usage."""
        locations = []
        
        for i, line in enumerate(lines, 1):
            # Check for divs that should be semantic elements
            if '<div' in line:
                # Navigation areas
                if 'navigation' in line.lower() or 'nav-' in line:
                    if '<nav' not in line:
                        locations.append(f"line {i} - use <nav> for navigation")
                        
                # Main content
                if 'main-content' in line or 'id="main"' in line:
                    if '<main' not in line:
                        locations.append(f"line {i} - use <main> for main content")
                        
            # Lists without semantic markup
            if 'className="list"' in line or 'class="list"' in line:
                if '<ul' not in line and '<ol' not in line:
                    locations.append(f"line {i} - use <ul> or <ol> for lists")
                    
        return {'issues': len(locations), 'locations': locations}
    
    def _get_issue_message(self, check: str, count: int) -> str:
        """Get issue message for an accessibility check."""
        messages = {
            'missing_alt_text': f'Found {count} images missing alt text',
            'missing_aria_labels': f'Found {count} elements missing ARIA labels',
            'missing_form_labels': f'Found {count} form inputs without labels',
            'color_contrast': f'Found {count} potential color contrast issues',
            'interactive_elements': f'Found {count} non-accessible interactive elements',
            'heading_hierarchy': f'Found {count} heading hierarchy issues',
            'focus_management': f'Found {count} focus management issues',
            'semantic_html': f'Found {count} non-semantic HTML elements',
        }
        return messages.get(check, f'Found {count} accessibility issues')
    
    def _get_pass_message(self, check: str) -> str:
        """Get pass message for an accessibility check."""
        messages = {
            'missing_alt_text': 'All images have alt text',
            'missing_aria_labels': 'Interactive elements have proper labels',
            'missing_form_labels': 'All form inputs have labels',
            'color_contrast': 'No obvious color contrast issues',
            'interactive_elements': 'Interactive elements are accessible',
            'heading_hierarchy': 'Heading hierarchy is correct',
            'focus_management': 'Focus indicators are preserved',
            'semantic_html': 'Semantic HTML is used appropriately',
        }
        return messages.get(check, 'Accessibility check passed') 