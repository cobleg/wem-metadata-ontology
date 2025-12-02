
import unittest
import sys
import os
import json

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.server import list_concepts, get_ontology_version, ontology

class TestServerExposure(unittest.TestCase):
    def test_list_concepts_includes_facility_classes(self):
        """Verify list_concepts includes Facility Classes."""
        result_json = list_concepts()
        result = json.loads(result_json)
        
        self.assertIn("Facility Classes", result)
        self.assertIn("TransitionalFacility", result["Facility Classes"])

    def test_ontology_version(self):
        """Verify ontology version is 1.2.0."""
        version_json = get_ontology_version()
        # The tool returns a string representation of the dict, so we might need to parse it or check string content
        # The tool implementation: return str(ontology.metadata.dict())
        # So it returns something like "{'version': '1.2.0', ...}"
        self.assertIn("'version': '1.2.0'", version_json)

if __name__ == "__main__":
    unittest.main()
