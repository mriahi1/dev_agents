"""Main code analyzer for quality checks."""

import re
import os
import subprocess
from typing import Dict, List, Tuple, Any
from pathlib import Path
from loguru import logger


class CodeAnalyzer:
    """Analyzes code for quality issues."""
    
    def __init__(self, repo_path: str = "."):
        """Initialize analyzer with repository path."""
        self.repo_path = Path(repo_path)
        
    def analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze a single file for issues."""
        results = {
            'console_logs': self._check_console_logs(file_path),
            'complexity': self._check_complexity(file_path),
            'todos': self._check_todos(file_path),
            'long_lines': self._check_line_length(file_path),
            'large_functions': self._check_function_size(file_path)
        }
        return results
    
    def analyze_pr_files(self, changed_files: List[str]) -> Dict[str, Any]:
        """Analyze all changed files in a PR."""
        all_results = {
            'console_logs': {'status': 'pass', 'issues': 0, 'locations': []},
            'complexity': {'status': 'pass', 'issues': 0, 'details': []},
            'todos': {'status': 'pass', 'issues': 0, 'locations': []},
            'formatting': {'status': 'pass', 'issues': 0, 'fixable': True},
            'linting': {'status': 'pass', 'issues': 0, 'details': []},
            'type_checking': {'status': 'pass', 'issues': 0, 'details': []},
            'long_lines': {'status': 'pass', 'issues': 0, 'locations': []},
            'large_functions': {'status': 'pass', 'issues': 0, 'details': []}
        }
        
        # Check each file
        for file in changed_files:
            if not self._should_analyze_file(file):
                continue
                
            file_path = self.repo_path / file
            if not file_path.exists():
                continue
                
            file_results = self.analyze_file(file_path)
            
            # Aggregate results
            for check, result in file_results.items():
                if check in all_results and result['issues'] > 0:
                    all_results[check]['issues'] += result['issues']
                    if 'locations' in result:
                        all_results[check].setdefault('locations', []).extend(
                            [f"{file}:{loc}" for loc in result['locations']]
                        )
                    if 'details' in result:
                        all_results[check].setdefault('details', []).extend(
                            [{**detail, 'file': file} for detail in result['details']]
                        )
        
        # Run project-wide checks
        all_results['formatting'] = self._check_formatting()
        all_results['linting'] = self._check_linting()
        all_results['type_checking'] = self._check_type_checking()
        
        # Update statuses based on issue counts
        for check, result in all_results.items():
            if result['issues'] > 0:
                if check in ['console_logs', 'type_checking']:
                    result['status'] = 'fail'
                else:
                    result['status'] = 'warning'
                    
                # Add messages
                if check == 'console_logs':
                    result['message'] = f"Found {result['issues']} console.log statements"
                elif check == 'complexity':
                    result['message'] = f"Found {result['issues']} complex functions"
                elif check == 'todos':
                    result['message'] = f"Found {result['issues']} TODO comments"
                elif check == 'formatting':
                    result['message'] = f"Found {result['issues']} formatting issues"
                elif check == 'linting':
                    result['message'] = f"Found {result['issues']} linting errors"
                elif check == 'type_checking':
                    result['message'] = f"Found {result['issues']} TypeScript errors"
                elif check == 'long_lines':
                    result['message'] = f"Found {result['issues']} lines over 120 characters"
                elif check == 'large_functions':
                    result['message'] = f"Found {result['issues']} functions over 50 lines"
            else:
                result['message'] = self._get_pass_message(check)
                
        return all_results
    
    def _should_analyze_file(self, file_path: str) -> bool:
        """Check if file should be analyzed."""
        # Only analyze TypeScript/JavaScript files
        extensions = ['.ts', '.tsx', '.js', '.jsx']
        return any(file_path.endswith(ext) for ext in extensions)
    
    def _check_console_logs(self, file_path: Path) -> Dict[str, Any]:
        """Check for console.log statements."""
        pattern = re.compile(r'console\.(log|error|warn|info|debug)\s*\(')
        locations = []
        
        try:
            with open(file_path, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    if pattern.search(line):
                        # Skip if it's commented out
                        stripped = line.strip()
                        if not stripped.startswith('//') and not stripped.startswith('*'):
                            locations.append(f"line {line_num}")
        except Exception as e:
            logger.error(f"Error checking console logs in {file_path}: {e}")
            
        return {
            'issues': len(locations),
            'locations': locations
        }
    
    def _check_complexity(self, file_path: Path) -> Dict[str, Any]:
        """Check cyclomatic complexity of functions."""
        # Simplified complexity check - counts decision points
        complexity_threshold = 10
        complex_functions = []
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                
            # Find function declarations
            func_pattern = re.compile(
                r'(?:function\s+(\w+)|(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s*)?\([^)]*\)\s*=>)',
                re.MULTILINE
            )
            
            for match in func_pattern.finditer(content):
                func_name = match.group(1) or match.group(2)
                func_start = match.start()
                
                # Extract function body (simplified)
                brace_count = 0
                func_end = func_start
                in_function = False
                
                for i, char in enumerate(content[func_start:], func_start):
                    if char == '{':
                        brace_count += 1
                        in_function = True
                    elif char == '}':
                        brace_count -= 1
                        if brace_count == 0 and in_function:
                            func_end = i
                            break
                
                if func_end > func_start:
                    func_body = content[func_start:func_end]
                    
                    # Count complexity indicators
                    complexity = 1  # Base complexity
                    complexity += len(re.findall(r'\bif\b', func_body))
                    complexity += len(re.findall(r'\belse\b', func_body))
                    complexity += len(re.findall(r'\bfor\b', func_body))
                    complexity += len(re.findall(r'\bwhile\b', func_body))
                    complexity += len(re.findall(r'\bcase\b', func_body))
                    complexity += len(re.findall(r'\bcatch\b', func_body))
                    complexity += len(re.findall(r'\?\s*[^:]+\s*:', func_body))  # Ternary
                    
                    if complexity > complexity_threshold:
                        line_num = content[:func_start].count('\n') + 1
                        complex_functions.append({
                            'function': func_name,
                            'complexity': complexity,
                            'line': line_num
                        })
                        
        except Exception as e:
            logger.error(f"Error checking complexity in {file_path}: {e}")
            
        return {
            'issues': len(complex_functions),
            'details': complex_functions
        }
    
    def _check_todos(self, file_path: Path) -> Dict[str, Any]:
        """Check for TODO comments."""
        pattern = re.compile(r'(TODO|FIXME|HACK|XXX|BUG):', re.IGNORECASE)
        locations = []
        
        try:
            with open(file_path, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    if pattern.search(line):
                        locations.append(f"line {line_num}")
        except Exception as e:
            logger.error(f"Error checking TODOs in {file_path}: {e}")
            
        return {
            'issues': len(locations),
            'locations': locations
        }
    
    def _check_line_length(self, file_path: Path, max_length: int = 120) -> Dict[str, Any]:
        """Check for lines exceeding maximum length."""
        long_lines = []
        
        try:
            with open(file_path, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    if len(line.rstrip()) > max_length:
                        long_lines.append(f"line {line_num} ({len(line.rstrip())} chars)")
        except Exception as e:
            logger.error(f"Error checking line length in {file_path}: {e}")
            
        return {
            'issues': len(long_lines),
            'locations': long_lines
        }
    
    def _check_function_size(self, file_path: Path, max_lines: int = 50) -> Dict[str, Any]:
        """Check for functions exceeding maximum lines."""
        large_functions = []
        
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
                
            # Find function declarations
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                
                # Check if this is a function declaration
                if (re.match(r'(?:export\s+)?(?:async\s+)?function\s+\w+', line) or
                    re.match(r'(?:const|let|var)\s+\w+\s*=\s*(?:async\s*)?\([^)]*\)\s*=>', line) or
                    re.match(r'\w+\s*\([^)]*\)\s*{', line)):
                    
                    func_start = i
                    func_name = re.search(r'(?:function\s+)?(\w+)', line)
                    func_name = func_name.group(1) if func_name else 'anonymous'
                    
                    # Find function end
                    brace_count = 0
                    j = i
                    while j < len(lines):
                        brace_count += lines[j].count('{')
                        brace_count -= lines[j].count('}')
                        if brace_count == 0 and j > i:
                            func_lines = j - func_start + 1
                            if func_lines > max_lines:
                                large_functions.append({
                                    'function': func_name,
                                    'lines': func_lines,
                                    'start_line': func_start + 1
                                })
                            break
                        j += 1
                    i = j
                i += 1
                
        except Exception as e:
            logger.error(f"Error checking function size in {file_path}: {e}")
            
        return {
            'issues': len(large_functions),
            'details': large_functions
        }
    
    def _check_formatting(self) -> Dict[str, Any]:
        """Check code formatting using prettier."""
        try:
            # Run prettier check
            result = subprocess.run(
                ['npx', 'prettier', '--check', 'src/**/*.{ts,tsx,js,jsx}'],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                # Count unformatted files
                output_lines = result.stdout.strip().split('\n')
                unformatted_files = [line for line in output_lines if line and not line.startswith('Checking')]
                
                return {
                    'status': 'warning',
                    'issues': len(unformatted_files),
                    'fixable': True
                }
        except subprocess.CalledProcessError:
            logger.error("Prettier not found")
        except Exception as e:
            logger.error(f"Error checking formatting: {e}")
            
        return {'status': 'pass', 'issues': 0, 'fixable': True}
    
    def _check_linting(self) -> Dict[str, Any]:
        """Check linting using ESLint."""
        try:
            # Run ESLint
            result = subprocess.run(
                ['npx', 'eslint', 'src', '--format', 'json'],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            if result.stdout:
                import json
                lint_results = json.loads(result.stdout)
                
                total_errors = sum(file['errorCount'] for file in lint_results)
                total_warnings = sum(file['warningCount'] for file in lint_results)
                
                if total_errors > 0:
                    return {
                        'status': 'fail',
                        'issues': total_errors,
                        'details': [
                            {
                                'file': file['filePath'],
                                'errors': file['errorCount'],
                                'warnings': file['warningCount']
                            }
                            for file in lint_results
                            if file['errorCount'] > 0
                        ]
                    }
                elif total_warnings > 0:
                    return {
                        'status': 'warning',
                        'issues': total_warnings,
                        'details': []
                    }
        except subprocess.CalledProcessError:
            logger.error("ESLint not found")
        except Exception as e:
            logger.error(f"Error checking linting: {e}")
            
        return {'status': 'pass', 'issues': 0, 'details': []}
    
    def _check_type_checking(self) -> Dict[str, Any]:
        """Check TypeScript types."""
        try:
            # Run TypeScript compiler
            result = subprocess.run(
                ['npx', 'tsc', '--noEmit'],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                # Parse TypeScript errors
                error_lines = result.stdout.strip().split('\n')
                error_count = len([line for line in error_lines if ': error TS' in line])
                
                return {
                    'status': 'fail',
                    'issues': error_count,
                    'details': error_lines[:10]  # First 10 errors
                }
        except subprocess.CalledProcessError:
            logger.error("TypeScript compiler not found")
        except Exception as e:
            logger.error(f"Error checking types: {e}")
            
        return {'status': 'pass', 'issues': 0, 'details': []}
    
    def _get_pass_message(self, check: str) -> str:
        """Get pass message for a check."""
        messages = {
            'console_logs': 'No console.log statements',
            'complexity': 'All functions have acceptable complexity',
            'todos': 'No TODO comments',
            'formatting': 'Code is properly formatted',
            'linting': 'No linting errors',
            'type_checking': 'No TypeScript errors',
            'long_lines': 'All lines within length limit',
            'large_functions': 'All functions are reasonably sized'
        }
        return messages.get(check, 'Check passed') 