
import unittest
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.server import ontology

class TestESROIConcepts(unittest.TestCase):
    def test_esroi_quantity_types(self):
        """Verify ESROI quantity types are defined."""
        expected_types = [
            "RCOQ", "ESROI", "MidPeakESROI", "PeakESROD", 
            "ESRDurationRequirement", "AvailabilityDurationGap", "ESRChargeShortfall"
        ]
        for qt in expected_types:
            self.assertIn(qt, ontology.quantity_types)
            
        # Check specific definitions
        self.assertIn("non-zero only during ESROIs", ontology.quantity_types["RCOQ"].description)
        self.assertIn("4 hours", ontology.quantity_types["ESRDurationRequirement"].description)

    def test_esr_liability(self):
        """Verify ESR technology type includes new liabilities."""
        esr = ontology.technology_types["ESR"]
        self.assertIn("RCOQ", esr.rcm_liability)
        self.assertIn("ESRChargeShortfall", esr.rcm_liability)

if __name__ == "__main__":
    unittest.main()
