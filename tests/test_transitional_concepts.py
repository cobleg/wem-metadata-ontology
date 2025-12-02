
import unittest
import sys
import os
import json

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.server import get_concept_definition, ontology

class TestTransitionalConcepts(unittest.TestCase):
    def test_transitional_facility_exists(self):
        """Verify TransitionalFacility is defined in facility_classes."""
        self.assertIn("TransitionalFacility", ontology.facility_classes)
        tf = ontology.facility_classes["TransitionalFacility"]
        self.assertIn("2018 Reserve Capacity Cycle", tf.description)
        self.assertIn("price caps", tf.description)

    def test_transitional_component_exists(self):
        """Verify TransitionalComponent is defined in facility_classes."""
        self.assertIn("TransitionalComponent", ontology.facility_classes)
        tc = ontology.facility_classes["TransitionalComponent"]
        self.assertIn("Separately Certified Component", tc.description)

    def test_price_type_exists(self):
        """Verify FacilityMonthlyPeakReserveCapacityPrice is defined."""
        self.assertIn("FacilityMonthlyPeakReserveCapacityPrice", ontology.price_types)
        price = ontology.price_types["FacilityMonthlyPeakReserveCapacityPrice"]
        self.assertEqual(price.scope, "facility")
        self.assertEqual(price.granularity, "CapacityMonth")

    def test_server_response(self):
        """Verify get_concept_definition returns Transitional Facility info."""
        definition_json = get_concept_definition("TransitionalFacility")
        definition = json.loads(definition_json)
        self.assertEqual(definition["name"], "Transitional Facility")

if __name__ == "__main__":
    unittest.main()
