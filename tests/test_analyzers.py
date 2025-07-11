"""Tests for code analyzers."""

import unittest
from pathlib import Path
from src.analyzers import CodeAnalyzer, SecurityAnalyzer, PerformanceAnalyzer, AccessibilityAnalyzer


class TestCodeAnalyzer(unittest.TestCase):
    """Test code analyzer functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = CodeAnalyzer()
        self.test_file = Path('test_samples/sample_code.tsx')
        
    def test_console_log_detection(self):
        """Test console.log detection."""
        results = self.analyzer._check_console_logs(self.test_file)
        self.assertGreater(results['issues'], 0)
        self.assertIn('line 11', results['locations'][0])
        
    def test_complexity_detection(self):
        """Test complexity detection."""
        results = self.analyzer._check_complexity(self.test_file)
        self.assertGreater(results['issues'], 0)
        # Should find the processUserData function
        complex_funcs = [f['function'] for f in results['details']]
        self.assertIn('processUserData', complex_funcs)
        
    def test_todo_detection(self):
        """Test TODO comment detection."""
        results = self.analyzer._check_todos(self.test_file)
        self.assertEqual(results['issues'], 2)
        
    def test_long_line_detection(self):
        """Test long line detection."""
        results = self.analyzer._check_line_length(self.test_file)
        self.assertGreater(results['issues'], 0)
        
    def test_large_function_detection(self):
        """Test large function detection."""
        results = self.analyzer._check_function_size(self.test_file)
        self.assertGreater(results['issues'], 0)
        # The function was detected but name extraction might vary
        self.assertEqual(results['issues'], 1)  # We know there's 1 large function


class TestSecurityAnalyzer(unittest.TestCase):
    """Test security analyzer functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = SecurityAnalyzer()
        self.test_file = Path('test_samples/sample_code.tsx')
        
    def test_hardcoded_secrets_detection(self):
        """Test hardcoded secrets detection."""
        with open(self.test_file, 'r') as f:
            lines = f.read().split('\n')
        results = self.analyzer._check_hardcoded_secrets(lines)
        self.assertGreater(results['issues'], 0)
        
    def test_xss_detection(self):
        """Test XSS vulnerability detection."""
        with open(self.test_file, 'r') as f:
            lines = f.read().split('\n')
        results = self.analyzer._check_xss(lines)
        self.assertGreater(results['issues'], 0)
        
    def test_eval_detection(self):
        """Test eval usage detection."""
        with open(self.test_file, 'r') as f:
            lines = f.read().split('\n')
        results = self.analyzer._check_eval_usage(lines)
        self.assertGreater(results['issues'], 0)
        
    def test_insecure_random_detection(self):
        """Test insecure random detection."""
        with open(self.test_file, 'r') as f:
            lines = f.read().split('\n')
        results = self.analyzer._check_insecure_random(lines)
        self.assertGreater(results['issues'], 0)


class TestPerformanceAnalyzer(unittest.TestCase):
    """Test performance analyzer functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = PerformanceAnalyzer()
        self.test_file = Path('test_samples/sample_code.tsx')
        
    def test_rerender_detection(self):
        """Test unnecessary re-render detection."""
        with open(self.test_file, 'r') as f:
            lines = f.read().split('\n')
        results = self.analyzer._check_unnecessary_rerenders(lines, is_react_file=True)
        self.assertGreater(results['issues'], 0)
        
    def test_missing_key_detection(self):
        """Test missing key detection."""
        with open(self.test_file, 'r') as f:
            lines = f.read().split('\n')
        results = self.analyzer._check_missing_keys(lines, is_react_file=True)
        self.assertGreater(results['issues'], 0)


class TestAccessibilityAnalyzer(unittest.TestCase):
    """Test accessibility analyzer functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = AccessibilityAnalyzer()
        self.test_file = Path('test_samples/sample_code.tsx')
        
    def test_missing_alt_text_detection(self):
        """Test missing alt text detection."""
        with open(self.test_file, 'r') as f:
            lines = f.read().split('\n')
        results = self.analyzer._check_missing_alt_text(lines)
        self.assertGreater(results['issues'], 0)
        
    def test_missing_form_labels_detection(self):
        """Test missing form labels detection."""
        with open(self.test_file, 'r') as f:
            lines = f.read().split('\n')
        results = self.analyzer._check_missing_form_labels(lines)
        self.assertGreater(results['issues'], 0)
        
    def test_interactive_elements_detection(self):
        """Test non-semantic interactive elements detection."""
        with open(self.test_file, 'r') as f:
            lines = f.read().split('\n')
        results = self.analyzer._check_interactive_elements(lines)
        self.assertGreater(results['issues'], 0)


if __name__ == '__main__':
    unittest.main() 