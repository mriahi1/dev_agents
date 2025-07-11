"""Performance analyzer for detecting potential performance issues."""

import re
from typing import Dict, List, Any
from pathlib import Path
from loguru import logger


class PerformanceAnalyzer:
    """Analyzes code for performance issues."""
    
    def __init__(self, repo_path: str = "."):
        """Initialize analyzer with repository path."""
        self.repo_path = Path(repo_path)
        
    def analyze_pr_files(self, changed_files: List[str]) -> Dict[str, Any]:
        """Analyze changed files for performance issues."""
        all_results = {
            'unnecessary_rerenders': {'status': 'pass', 'issues': 0, 'locations': []},
            'missing_memoization': {'status': 'pass', 'issues': 0, 'locations': []},
            'large_bundle_imports': {'status': 'pass', 'issues': 0, 'locations': []},
            'inefficient_loops': {'status': 'pass', 'issues': 0, 'locations': []},
            'missing_keys': {'status': 'pass', 'issues': 0, 'locations': []},
            'sync_operations': {'status': 'pass', 'issues': 0, 'locations': []},
            'memory_leaks': {'status': 'pass', 'issues': 0, 'locations': []},
            'unoptimized_images': {'status': 'pass', 'issues': 0, 'locations': []},
        }
        
        for file in changed_files:
            if not self._should_analyze_file(file):
                continue
                
            file_path = self.repo_path / file
            if not file_path.exists():
                continue
                
            # Run performance checks
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
                result['status'] = 'warning'
                result['message'] = self._get_issue_message(check, result['issues'])
            else:
                result['message'] = self._get_pass_message(check)
                
        return all_results
    
    def _should_analyze_file(self, file_path: str) -> bool:
        """Check if file should be analyzed."""
        extensions = ['.ts', '.tsx', '.js', '.jsx']
        return any(file_path.endswith(ext) for ext in extensions)
    
    def _analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze a single file for performance issues."""
        results = {}
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                lines = content.split('\n')
                
            # Check if it's a React component file
            is_react_file = 'import React' in content or 'from \'react\'' in content
            
            results['unnecessary_rerenders'] = self._check_unnecessary_rerenders(lines, is_react_file)
            results['missing_memoization'] = self._check_missing_memoization(lines, is_react_file)
            results['large_bundle_imports'] = self._check_large_imports(lines)
            results['inefficient_loops'] = self._check_inefficient_loops(lines)
            results['missing_keys'] = self._check_missing_keys(lines, is_react_file)
            results['sync_operations'] = self._check_sync_operations(lines)
            results['memory_leaks'] = self._check_memory_leaks(lines)
            results['unoptimized_images'] = self._check_unoptimized_images(lines)
            
        except Exception as e:
            logger.error(f"Error analyzing {file_path}: {e}")
            
        return results
    
    def _check_unnecessary_rerenders(self, lines: List[str], is_react_file: bool) -> Dict[str, Any]:
        """Check for patterns that cause unnecessary React re-renders."""
        if not is_react_file:
            return {'issues': 0, 'locations': []}
            
        patterns = [
            r'style\s*=\s*\{\{',                          # Inline style objects
            r'onClick\s*=\s*\{\s*\(\)\s*=>',             # Inline arrow functions
            r'(?<!use)(?<!set)\w+\s*=\s*\[\]',           # Array literals as props
            r'(?<!use)(?<!set)\w+\s*=\s*\{\}',           # Object literals as props
        ]
        
        locations = []
        for i, line in enumerate(lines, 1):
            # Skip if in useEffect, useMemo, useCallback
            if 'useEffect' in line or 'useMemo' in line or 'useCallback' in line:
                continue
                
            for pattern in patterns:
                if re.search(pattern, line):
                    locations.append(f"line {i}")
                    break
                    
        return {'issues': len(locations), 'locations': locations}
    
    def _check_missing_memoization(self, lines: List[str], is_react_file: bool) -> Dict[str, Any]:
        """Check for expensive operations that should be memoized."""
        if not is_react_file:
            return {'issues': 0, 'locations': []}
            
        patterns = [
            r'\.filter\s*\(.*\)\.map\s*\(',               # filter().map() chains
            r'\.sort\s*\(.*\)(?!.*useMemo)',              # Sorting without memoization
            r'\.reduce\s*\(.*\)(?!.*useMemo)',            # Complex reduces
            r'new Date\s*\(.*\)(?!.*useMemo)',            # Date calculations
        ]
        
        locations = []
        for i, line in enumerate(lines, 1):
            for pattern in patterns:
                if re.search(pattern, line):
                    # Check if it's inside a component (rough heuristic)
                    if any(keyword in lines[max(0, i-10):i] for keyword in ['function', 'const', '=>']):
                        locations.append(f"line {i}")
                        break
                        
        return {'issues': len(locations), 'locations': locations}
    
    def _check_large_imports(self, lines: List[str]) -> Dict[str, Any]:
        """Check for imports that increase bundle size."""
        patterns = [
            r'import\s+\*\s+as',                          # Import entire module
            r'from\s+[\'"]lodash[\'"]',                   # Non-tree-shakeable lodash
            r'from\s+[\'"]moment[\'"]',                   # Large moment.js library
            r'import\s+\{[^}]{100,}\}',                   # Very large destructured imports
        ]
        
        locations = []
        for i, line in enumerate(lines, 1):
            for pattern in patterns:
                if re.search(pattern, line):
                    locations.append(f"line {i}")
                    break
                    
        return {'issues': len(locations), 'locations': locations}
    
    def _check_inefficient_loops(self, lines: List[str]) -> Dict[str, Any]:
        """Check for inefficient loop patterns."""
        locations = []
        
        for i, line in enumerate(lines, 1):
            # Nested array methods
            if '.map(' in line and any(method in line for method in ['.filter(', '.find(', '.forEach(']):
                if line.count('(') - line.count(')') > 2:  # Rough nesting check
                    locations.append(f"line {i} - nested array methods")
                    
            # Array operations in loops
            if 'for' in line or 'while' in line:
                # Look ahead for array operations
                for j in range(i, min(i + 10, len(lines))):
                    if any(op in lines[j] for op in ['.push(', '.unshift(', '.splice(']):
                        locations.append(f"line {j} - array mutation in loop")
                        break
                        
        return {'issues': len(locations), 'locations': locations}
    
    def _check_missing_keys(self, lines: List[str], is_react_file: bool) -> Dict[str, Any]:
        """Check for missing keys in React lists."""
        if not is_react_file:
            return {'issues': 0, 'locations': []}
            
        locations = []
        in_map = False
        map_start_line = 0
        
        for i, line in enumerate(lines, 1):
            # Detect start of map
            if '.map(' in line:
                in_map = True
                map_start_line = i
                
            # If we're in a map, look for JSX without key
            if in_map:
                if '<' in line and '>' in line and 'key=' not in line:
                    # Check if this is JSX element (rough check)
                    if not any(skip in line for skip in ['</', '< ', '<=', '>=', '=>']):
                        locations.append(f"line {i} - missing key in list")
                        
                # End of map (rough detection)
                if ')' in line and line.count(')') > line.count('('):
                    in_map = False
                    
        return {'issues': len(locations), 'locations': locations}
    
    def _check_sync_operations(self, lines: List[str]) -> Dict[str, Any]:
        """Check for synchronous operations that should be async."""
        patterns = [
            r'fs\.readFileSync',                          # Sync file operations
            r'fs\.writeFileSync',
            r'localStorage\.(getItem|setItem)\s*\([^)]*JSON\.parse',  # Large localStorage ops
            r'while\s*\(.*Date\.now\(\)',                 # Busy waiting
        ]
        
        locations = []
        for i, line in enumerate(lines, 1):
            for pattern in patterns:
                if re.search(pattern, line):
                    locations.append(f"line {i}")
                    break
                    
        return {'issues': len(locations), 'locations': locations}
    
    def _check_memory_leaks(self, lines: List[str]) -> Dict[str, Any]:
        """Check for potential memory leaks."""
        locations = []
        
        # Track event listeners and intervals
        add_listener_lines = []
        set_interval_lines = []
        
        for i, line in enumerate(lines, 1):
            # Event listeners without cleanup
            if 'addEventListener' in line:
                add_listener_lines.append(i)
            elif 'removeEventListener' in line:
                add_listener_lines = []  # Reset if we find cleanup
                
            # Timers without cleanup
            if 'setInterval' in line or 'setTimeout' in line:
                set_interval_lines.append(i)
            elif 'clearInterval' in line or 'clearTimeout' in line:
                set_interval_lines = []  # Reset if we find cleanup
                
            # Check for cleanup in useEffect
            if 'useEffect' in line:
                # Look for return cleanup function
                has_cleanup = False
                for j in range(i, min(i + 20, len(lines))):
                    if 'return' in lines[j] and '=>' in lines[j]:
                        has_cleanup = True
                        break
                        
                if not has_cleanup and (add_listener_lines or set_interval_lines):
                    locations.append(f"line {i} - useEffect without cleanup")
                    
        return {'issues': len(locations), 'locations': locations}
    
    def _check_unoptimized_images(self, lines: List[str]) -> Dict[str, Any]:
        """Check for unoptimized image usage."""
        patterns = [
            r'<img\s+.*src=.*\.(?:png|jpg|jpeg).*(?!loading)',  # Images without lazy loading
            r'require\s*\([\'"][^\'"]*(png|jpg|jpeg)',          # Large image imports
        ]
        
        locations = []
        for i, line in enumerate(lines, 1):
            for pattern in patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    # Check if it's missing optimization attributes
                    if 'loading=' not in line and 'Image' not in line:  # Not using Next.js Image
                        locations.append(f"line {i}")
                        break
                        
        return {'issues': len(locations), 'locations': locations}
    
    def _get_issue_message(self, check: str, count: int) -> str:
        """Get issue message for a performance check."""
        messages = {
            'unnecessary_rerenders': f'Found {count} patterns causing unnecessary re-renders',
            'missing_memoization': f'Found {count} expensive operations without memoization',
            'large_bundle_imports': f'Found {count} imports that increase bundle size',
            'inefficient_loops': f'Found {count} inefficient loop patterns',
            'missing_keys': f'Found {count} list items missing keys',
            'sync_operations': f'Found {count} synchronous operations that could block',
            'memory_leaks': f'Found {count} potential memory leaks',
            'unoptimized_images': f'Found {count} unoptimized images',
        }
        return messages.get(check, f'Found {count} performance issues')
    
    def _get_pass_message(self, check: str) -> str:
        """Get pass message for a performance check."""
        messages = {
            'unnecessary_rerenders': 'No unnecessary re-render patterns found',
            'missing_memoization': 'Expensive operations are properly memoized',
            'large_bundle_imports': 'All imports are optimized',
            'inefficient_loops': 'Loop patterns are efficient',
            'missing_keys': 'All list items have proper keys',
            'sync_operations': 'No blocking synchronous operations',
            'memory_leaks': 'No memory leak patterns detected',
            'unoptimized_images': 'Images are properly optimized',
        }
        return messages.get(check, 'Performance check passed') 