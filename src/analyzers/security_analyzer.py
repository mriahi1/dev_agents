"""Security analyzer for detecting potential vulnerabilities."""

import re
from typing import Dict, List, Any
from pathlib import Path
from loguru import logger


class SecurityAnalyzer:
    """Analyzes code for security vulnerabilities."""
    
    def __init__(self, repo_path: str = "."):
        """Initialize analyzer with repository path."""
        self.repo_path = Path(repo_path)
        
    def analyze_pr_files(self, changed_files: List[str]) -> Dict[str, Any]:
        """Analyze changed files for security issues."""
        all_results = {
            'hardcoded_secrets': {'status': 'pass', 'issues': 0, 'locations': []},
            'sql_injection': {'status': 'pass', 'issues': 0, 'locations': []},
            'xss_vulnerabilities': {'status': 'pass', 'issues': 0, 'locations': []},
            'unsafe_regex': {'status': 'pass', 'issues': 0, 'locations': []},
            'exposed_api_keys': {'status': 'pass', 'issues': 0, 'locations': []},
            'insecure_random': {'status': 'pass', 'issues': 0, 'locations': []},
            'eval_usage': {'status': 'pass', 'issues': 0, 'locations': []},
            'cors_issues': {'status': 'pass', 'issues': 0, 'locations': []},
        }
        
        for file in changed_files:
            if not self._should_analyze_file(file):
                continue
                
            file_path = self.repo_path / file
            if not file_path.exists():
                continue
                
            # Run security checks
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
                result['status'] = 'fail' if check in ['hardcoded_secrets', 'sql_injection', 'eval_usage'] else 'warning'
                result['message'] = self._get_issue_message(check, result['issues'])
            else:
                result['message'] = self._get_pass_message(check)
                
        return all_results
    
    def _should_analyze_file(self, file_path: str) -> bool:
        """Check if file should be analyzed."""
        extensions = ['.ts', '.tsx', '.js', '.jsx', '.json', '.env', '.yml', '.yaml']
        return any(file_path.endswith(ext) for ext in extensions)
    
    def _analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze a single file for security issues."""
        results = {}
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                lines = content.split('\n')
                
            results['hardcoded_secrets'] = self._check_hardcoded_secrets(lines)
            results['sql_injection'] = self._check_sql_injection(lines)
            results['xss_vulnerabilities'] = self._check_xss(lines)
            results['unsafe_regex'] = self._check_unsafe_regex(lines)
            results['exposed_api_keys'] = self._check_api_keys(lines)
            results['insecure_random'] = self._check_insecure_random(lines)
            results['eval_usage'] = self._check_eval_usage(lines)
            results['cors_issues'] = self._check_cors_issues(lines)
            
        except Exception as e:
            logger.error(f"Error analyzing {file_path}: {e}")
            
        return results
    
    def _check_hardcoded_secrets(self, lines: List[str]) -> Dict[str, Any]:
        """Check for hardcoded secrets and passwords."""
        patterns = [
            r'password\s*[:=]\s*["\'](?!.*\$\{|process\.env)',  # Hardcoded passwords
            r'secret\s*[:=]\s*["\'](?!.*\$\{|process\.env)',    # Hardcoded secrets
            r'api[_-]?key\s*[:=]\s*["\'](?!.*\$\{|process\.env)', # Hardcoded API keys
            r'token\s*[:=]\s*["\'][A-Za-z0-9+/=]{20,}["\']',   # Hardcoded tokens
        ]
        
        locations = []
        for i, line in enumerate(lines, 1):
            # Skip comments
            stripped = line.strip()
            if stripped.startswith('//') or stripped.startswith('*'):
                continue
                
            for pattern in patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    locations.append(f"line {i}")
                    break
                    
        return {'issues': len(locations), 'locations': locations}
    
    def _check_sql_injection(self, lines: List[str]) -> Dict[str, Any]:
        """Check for potential SQL injection vulnerabilities."""
        patterns = [
            r'query\s*\(\s*[\'"`].*\$\{.*\}.*[\'"`]',  # String interpolation in queries
            r'query\s*\(\s*[\'"`].*\+.*[\'"`]',        # String concatenation in queries
            r'\.raw\s*\(\s*[\'"`].*\$\{.*\}',          # Raw queries with interpolation
        ]
        
        locations = []
        for i, line in enumerate(lines, 1):
            for pattern in patterns:
                if re.search(pattern, line):
                    locations.append(f"line {i}")
                    break
                    
        return {'issues': len(locations), 'locations': locations}
    
    def _check_xss(self, lines: List[str]) -> Dict[str, Any]:
        """Check for potential XSS vulnerabilities."""
        patterns = [
            r'dangerouslySetInnerHTML',                    # React dangerous HTML
            r'innerHTML\s*=',                              # Direct innerHTML assignment
            r'document\.write\s*\(',                       # document.write usage
            r'\.html\s*\(\s*[^)]*\$\{',                   # jQuery html() with interpolation
            r'v-html\s*=',                                 # Vue v-html directive
        ]
        
        locations = []
        for i, line in enumerate(lines, 1):
            for pattern in patterns:
                if re.search(pattern, line):
                    locations.append(f"line {i}")
                    break
                    
        return {'issues': len(locations), 'locations': locations}
    
    def _check_unsafe_regex(self, lines: List[str]) -> Dict[str, Any]:
        """Check for potentially unsafe regular expressions (ReDoS)."""
        # Patterns that might cause catastrophic backtracking
        patterns = [
            r'RegExp\s*\([^)]*\(\.\*\)\+',                # Nested quantifiers
            r'RegExp\s*\([^)]*\(\.\+\)\+',                # Nested quantifiers
            r'/.*\(\.\*\)\+.*/',                          # Regex literal with nested quantifiers
            r'/.*\(\.\+\)\+.*/',                          # Regex literal with nested quantifiers
        ]
        
        locations = []
        for i, line in enumerate(lines, 1):
            for pattern in patterns:
                if re.search(pattern, line):
                    locations.append(f"line {i}")
                    break
                    
        return {'issues': len(locations), 'locations': locations}
    
    def _check_api_keys(self, lines: List[str]) -> Dict[str, Any]:
        """Check for exposed API keys."""
        # Common API key patterns
        patterns = [
            r'AIza[0-9A-Za-z_-]{35}',                     # Google API Key
            r'[0-9a-f]{32}-us[0-9]{1,2}',                 # Mailchimp API Key
            r'sk_live_[0-9a-zA-Z]{24}',                   # Stripe Live Key
            r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}',  # Generic UUID
        ]
        
        locations = []
        for i, line in enumerate(lines, 1):
            # Skip if it's in a comment or uses environment variable
            if 'process.env' in line or 'import.meta.env' in line:
                continue
                
            for pattern in patterns:
                if re.search(pattern, line):
                    locations.append(f"line {i}")
                    break
                    
        return {'issues': len(locations), 'locations': locations}
    
    def _check_insecure_random(self, lines: List[str]) -> Dict[str, Any]:
        """Check for insecure random number generation."""
        patterns = [
            r'Math\.random\s*\(\s*\).*(?:password|token|secret|key)',  # Math.random for security
            r'Date\.now\s*\(\s*\).*(?:password|token|secret|key)',     # Date for randomness
        ]
        
        locations = []
        for i, line in enumerate(lines, 1):
            for pattern in patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    locations.append(f"line {i}")
                    break
                    
        return {'issues': len(locations), 'locations': locations}
    
    def _check_eval_usage(self, lines: List[str]) -> Dict[str, Any]:
        """Check for eval() and similar dangerous functions."""
        patterns = [
            r'\beval\s*\(',                               # eval()
            r'new\s+Function\s*\(',                       # new Function()
            r'setTimeout\s*\(\s*[\'"`]',                  # setTimeout with string
            r'setInterval\s*\(\s*[\'"`]',                 # setInterval with string
        ]
        
        locations = []
        for i, line in enumerate(lines, 1):
            for pattern in patterns:
                if re.search(pattern, line):
                    locations.append(f"line {i}")
                    break
                    
        return {'issues': len(locations), 'locations': locations}
    
    def _check_cors_issues(self, lines: List[str]) -> Dict[str, Any]:
        """Check for insecure CORS configurations."""
        patterns = [
            r'Access-Control-Allow-Origin.*\*',           # Wildcard CORS
            r'credentials:\s*[\'"]include[\'"].*origin:\s*[\'"]?\*',  # Credentials with wildcard
            r'cors\s*\(\s*\{\s*origin:\s*true',          # Allow all origins
        ]
        
        locations = []
        for i, line in enumerate(lines, 1):
            for pattern in patterns:
                if re.search(pattern, line):
                    locations.append(f"line {i}")
                    break
                    
        return {'issues': len(locations), 'locations': locations}
    
    def _get_issue_message(self, check: str, count: int) -> str:
        """Get issue message for a security check."""
        messages = {
            'hardcoded_secrets': f'Found {count} hardcoded secrets or passwords',
            'sql_injection': f'Found {count} potential SQL injection vulnerabilities',
            'xss_vulnerabilities': f'Found {count} potential XSS vulnerabilities',
            'unsafe_regex': f'Found {count} potentially unsafe regular expressions',
            'exposed_api_keys': f'Found {count} exposed API keys',
            'insecure_random': f'Found {count} uses of insecure random generation',
            'eval_usage': f'Found {count} uses of eval() or similar functions',
            'cors_issues': f'Found {count} insecure CORS configurations',
        }
        return messages.get(check, f'Found {count} security issues')
    
    def _get_pass_message(self, check: str) -> str:
        """Get pass message for a security check."""
        messages = {
            'hardcoded_secrets': 'No hardcoded secrets found',
            'sql_injection': 'No SQL injection risks detected',
            'xss_vulnerabilities': 'No XSS vulnerabilities found',
            'unsafe_regex': 'All regular expressions appear safe',
            'exposed_api_keys': 'No exposed API keys found',
            'insecure_random': 'Secure random generation used',
            'eval_usage': 'No dangerous eval() usage found',
            'cors_issues': 'CORS configuration appears secure',
        }
        return messages.get(check, 'Security check passed') 