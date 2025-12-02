
import unittest
import sys
import os
import json

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.server import get_concept_definition, ontology

class TestRCMOntology(unittest.TestCase):
    def test_rcm_services_exist(self):
        """Verify RCM market services are defined."""
        self.assertIn("PeakReserveCapacity", ontology.market_services)
        self.assertIn("FlexibleReserveCapacity", ontology.market_services)

    def test_rcm_quantities_exist(self):
        """Verify RCM quantity types are defined."""
        self.assertIn("PeakIRCR", ontology.quantity_types)
        self.assertIn("FlexibleIRCR", ontology.quantity_types)

    def test_igs_rcm_properties(self):
        """Verify IGS (Wind/Solar) has correct eligibility and liability."""
        igs = ontology.technology_types["IGS"]
        
        # Check Eligibility
        self.assertIsNotNone(igs.rcm_eligibility)
        self.assertIn("PeakReserveCapacity", igs.rcm_eligibility)
        # Should NOT be eligible for Flexible Reserve Capacity (implied by user prompt "liable to pay")
        # Wait, user said "might be liable to pay", implying they are NOT providers.
        # My implementation only put Peak in eligibility.
        self.assertNotIn("FlexibleReserveCapacity", igs.rcm_eligibility)

        # Check Liability
        self.assertIsNotNone(igs.rcm_liability)
        # IGS should NOT be liable for FlexibleIRCR (user correction)
        self.assertNotIn("FlexibleIRCR", igs.rcm_liability)

    def test_esr_rcm_properties(self):
        """Verify ESR (Storage) has correct eligibility and liability."""
        esr = ontology.technology_types["ESR"]
        
        # Eligible for both
        self.assertIn("PeakReserveCapacity", esr.rcm_eligibility)
        self.assertIn("FlexibleReserveCapacity", esr.rcm_eligibility)
        
        # Liable for Flex
        self.assertIn("FlexibleIRCR", esr.rcm_liability)

    def test_server_response(self):
        """Verify get_concept_definition returns RCM info."""
        definition_json = get_concept_definition("IGS")
        definition = json.loads(definition_json)
        
        self.assertIn("rcm_eligibility", definition)
        self.assertIn("rcm_liability", definition)
        self.assertEqual(definition["rcm_eligibility"], ["PeakReserveCapacity"])

if __name__ == "__main__":
    unittest.main()
