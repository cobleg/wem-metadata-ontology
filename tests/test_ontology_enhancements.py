import unittest
import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.loader import OntologyLoader
from src.validator import Validator

class TestOntologyEnhancements(unittest.TestCase):
    def setUp(self):
        self.loader = OntologyLoader("ontology")
        self.ontology = self.loader.get_ontology()
        self.validator = Validator(self.ontology)

    def test_concepts_loaded(self):
        """Verify new concepts are loaded."""
        # Check Physical Capacity concepts
        self.assertIn("NameplateCapacity", self.ontology.quantity_types)
        self.assertIn("EnergyCapacity", self.ontology.quantity_types)
        self.assertIn("DurationRating", self.ontology.quantity_types)
        
        # Check Performance Metrics
        self.assertIn("CapacityFactor", self.ontology.quantity_types)
        self.assertIn("AvailabilityFactor", self.ontology.quantity_types)
        
        # Check variants
        cf = self.ontology.quantity_types["CapacityFactor"]
        self.assertTrue(cf.abstract)
        self.assertIn("GeneratorCapacityFactor", cf.variants)
        self.assertIn("StorageDischargeCapacityFactor", cf.variants)
        
        # Check SCADA link
        self.assertIn("SCADA", self.ontology.quantity_types)
        gen_cf = cf.variants["GeneratorCapacityFactor"]
        self.assertIn("SCADA", gen_cf.requires)

    def test_validation_logic(self):
        """Verify validation logic for calculate_capacity_factor."""
        
        # Test 1: Valid Generator case
        params_gen = {
            "facility_code": "GEN1",
            "start_time": "2023-01-01",
            "end_time": "2023-01-02",
            "facility_type": "Generator"
        }
        result = self.validator.validate_operation("calculate_capacity_factor", params_gen)
        self.assertTrue(result.is_valid, f"Generator validation failed: {result.violations}")

        # Test 2: Invalid Storage case (missing cf_type)
        params_storage_invalid = {
            "facility_code": "BESS1",
            "start_time": "2023-01-01",
            "end_time": "2023-01-02",
            "facility_type": "Storage"
        }
        result = self.validator.validate_operation("calculate_capacity_factor", params_storage_invalid)
        self.assertFalse(result.is_valid)
        self.assertIn("Must specify CF type for storage facilities", result.violations)

        # Test 3: Valid Storage case
        params_storage_valid = {
            "facility_code": "BESS1",
            "start_time": "2023-01-01",
            "end_time": "2023-01-02",
            "facility_type": "Storage",
            "cf_type": "discharge"
        }
        result = self.validator.validate_operation("calculate_capacity_factor", params_storage_valid)
        self.assertTrue(result.is_valid, f"Storage validation failed: {result.violations}")

if __name__ == "__main__":
    unittest.main()
