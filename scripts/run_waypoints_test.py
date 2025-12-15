import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from tests.test_api_waypoints import TestAPIWaypoints

def main():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAPIWaypoints)
    with open('test_output.txt', 'w') as f:
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        result = runner.run(suite)
    
    # Print to console too
    with open('test_output.txt', 'r') as f:
        print(f.read())

if __name__ == '__main__':
    main()
