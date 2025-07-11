#!/usr/bin/env python3
"""Test script to demonstrate the code analyzers."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.analyzers import CodeAnalyzer, SecurityAnalyzer, PerformanceAnalyzer, AccessibilityAnalyzer
from pathlib import Path


def main():
    """Run all analyzers on the sample file."""
    sample_file = 'test_samples/sample_code.tsx'
    
    print("🔍 Testing Code Analyzers on sample_code.tsx\n")
    print("=" * 60)
    
    # Test Code Analyzer
    print("\n📋 CODE QUALITY ANALYSIS:")
    print("-" * 40)
    code_analyzer = CodeAnalyzer()
    code_results = code_analyzer.analyze_pr_files([sample_file])
    
    for check, result in code_results.items():
        if result['issues'] > 0:
            print(f"❌ {check}: {result['message']}")
            if 'locations' in result:
                for loc in result['locations'][:3]:
                    print(f"   → {loc}")
                if len(result.get('locations', [])) > 3:
                    print(f"   → ... and {len(result['locations']) - 3} more")
        else:
            print(f"✅ {check}: {result['message']}")
    
    # Test Security Analyzer
    print("\n\n🔒 SECURITY ANALYSIS:")
    print("-" * 40)
    security_analyzer = SecurityAnalyzer()
    security_results = security_analyzer.analyze_pr_files([sample_file])
    
    for check, result in security_results.items():
        if result['issues'] > 0:
            print(f"❌ {check}: {result['message']}")
            for loc in result['locations'][:3]:
                print(f"   → {loc}")
        else:
            print(f"✅ {check}: {result['message']}")
    
    # Test Performance Analyzer
    print("\n\n⚡ PERFORMANCE ANALYSIS:")
    print("-" * 40)
    performance_analyzer = PerformanceAnalyzer()
    performance_results = performance_analyzer.analyze_pr_files([sample_file])
    
    for check, result in performance_results.items():
        if result['issues'] > 0:
            print(f"⚠️  {check}: {result['message']}")
            for loc in result['locations'][:3]:
                print(f"   → {loc}")
        else:
            print(f"✅ {check}: {result['message']}")
    
    # Test Accessibility Analyzer
    print("\n\n♿ ACCESSIBILITY ANALYSIS:")
    print("-" * 40)
    accessibility_analyzer = AccessibilityAnalyzer()
    accessibility_results = accessibility_analyzer.analyze_pr_files([sample_file])
    
    for check, result in accessibility_results.items():
        if result['issues'] > 0:
            print(f"⚠️  {check}: {result['message']}")
            for loc in result['locations'][:3]:
                print(f"   → {loc}")
        else:
            print(f"✅ {check}: {result['message']}")
    
    # Summary
    print("\n\n📊 SUMMARY:")
    print("-" * 40)
    
    total_issues = 0
    for results in [code_results, security_results, performance_results, accessibility_results]:
        for check, result in results.items():
            total_issues += result['issues']
    
    print(f"Total issues found: {total_issues}")
    print("\nThis sample file was designed to trigger various analyzers.")
    print("In a real PR review, you would see these issues flagged for fixing.")


if __name__ == "__main__":
    main() 