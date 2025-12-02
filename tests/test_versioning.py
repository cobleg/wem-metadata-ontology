
import unittest
import sys
import os
import json

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.server import get_ontology_version

class TestVersioning(unittest.TestCase):
    def test_get_version(self):
        """Verify ontology version is returned."""
        version_str = get_ontology_version()
        print(f"Version output: {version_str}")
        
        # Parse the string representation of the dict
        # Note: The tool returns str(dict), which uses single quotes. 
        # We need to be careful if we want to parse it as JSON, but here we can just check substring.
        
        self.assertIn("'version': '1.1.0'", version_str)
        self.assertIn("'last_updated': '2025-12-02'", version_str)

if __name__ == "__main__":
    unittest.main()
