"""
Run all tests and generate a detailed report.
"""
import sys
import os
import unittest
import io
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def run_tests():
    """Run all tests and return results."""
    # Discover and run tests
    loader = unittest.TestLoader()
    suite = loader.discover('tests', pattern='test_*.py')
    
    # Capture output
    stream = io.StringIO()
    runner = unittest.TextTestRunner(stream=stream, verbosity=2)
    result = runner.run(suite)
    
    return result, stream.getvalue()

def generate_report(result, output):
    """Generate a markdown test report."""
    report = []
    report.append("# Test Report - py-osrm-backend")
    report.append(f"\n**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"\n**Python**: {sys.version.split()[0]}")
    
    # Summary
    report.append("\n## Summary")
    report.append(f"- **Tests Run**: {result.testsRun}")
    report.append(f"- **Passed**: {result.testsRun - len(result.failures) - len(result.errors)}")
    report.append(f"- **Failures**: {len(result.failures)}")
    report.append(f"- **Errors**: {len(result.errors)}")
    
    status = "✅ ALL TESTS PASSED" if result.wasSuccessful() else "❌ SOME TESTS FAILED"
    report.append(f"\n**Status**: {status}")
    
    # Detailed results
    report.append("\n## Test Details")
    report.append("```")
    report.append(output)
    report.append("```")
    
    # Failures
    if result.failures:
        report.append("\n## Failures")
        for test, traceback in result.failures:
            report.append(f"\n### {test}")
            report.append(f"```\n{traceback}\n```")
    
    # Errors
    if result.errors:
        report.append("\n## Errors")
        for test, traceback in result.errors:
            report.append(f"\n### {test}")
            report.append(f"```\n{traceback}\n```")
    
    return "\n".join(report)

def main():
    os.chdir(os.path.join(os.path.dirname(__file__), '..'))
    print("Running tests...")
    result, output = run_tests()
    
    report = generate_report(result, output)
    
    # Save report
    report_path = os.path.join('tests', 'test_report.md')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\nReport saved to: {report_path}")
    print(f"\nSummary: {result.testsRun} tests, {len(result.failures)} failures, {len(result.errors)} errors")
    
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    sys.exit(main())
