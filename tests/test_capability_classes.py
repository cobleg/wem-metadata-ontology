
import unittest
import sys
import os
import json

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.server import list_concepts, ontology

class TestCapabilityClasses(unittest.TestCase):
    def test_capability_classes_loaded(self):
        """Verify Capability Classes are loaded into the ontology."""
        self.assertIn("Class1", ontology.capability_classes)
        self.assertIn("Class2", ontology.capability_classes)
        self.assertIn("Class3", ontology.capability_classes)

    def test_priorities(self):
        """Verify priorities are correct."""
        c1 = ontology.capability_classes["Class1"]
        c2 = ontology.capability_classes["Class2"]
        c3 = ontology.capability_classes["Class3"]
        
        self.assertEqual(c1.priority, 1)
        self.assertEqual(c2.priority, 2)
        self.assertEqual(c3.priority, 3)

    def test_server_exposure(self):
        """Verify list_concepts includes Capability Classes."""
        result_json = list_concepts()
        result = json.loads(result_json)
        
        self.assertIn("Capability Classes", result)
        self.assertIn("Class1", result["Capability Classes"])

    def test_availability_duration_requirement(self):
        """Verify AvailabilityDurationRequirement is defined."""
        self.assertIn("AvailabilityDurationRequirement", ontology.quantity_types)

if __name__ == "__main__":
    unittest.main()
