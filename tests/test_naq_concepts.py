
import unittest
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.server import ontology

class TestNAQConcepts(unittest.TestCase):
    def test_naq_quantity_types(self):
        """Verify NAQ quantity types are defined."""
        self.assertIn("NetworkAccessQuantity", ontology.quantity_types)
        self.assertIn("HighestNetworkAccessQuantity", ontology.quantity_types)
        self.assertIn("IndicativeNAQ", ontology.quantity_types)
        
        naq = ontology.quantity_types["NetworkAccessQuantity"]
        self.assertIn("Caps Capacity Credits", naq.description)

    def test_naff_facility_class(self):
        """Verify NAFF facility class is defined."""
        self.assertIn("NAFF", ontology.facility_classes)
        naff = ontology.facility_classes["NAFF"]
        self.assertIn("Priority 2", naff.description)

    def test_naq_operation(self):
        """Verify determine_network_access_quantity operation is defined."""
        self.assertIn("determine_network_access_quantity", ontology.operations)
        op = ontology.operations["determine_network_access_quantity"]
        self.assertIn("CertifiedReserveCapacity", op.required_inputs)
        # Check prioritisation logic is captured
        self.assertIn("prioritisation", op.logic)
        self.assertIn("Existing/Committed Facilities", op.logic["prioritisation"][1])

    def test_capacity_credit_update(self):
        """Verify CapacityCredit description mentions NAQ."""
        cc = ontology.quantity_types["CapacityCredit"]
        self.assertIn("Network Access Quantity", cc.description)

if __name__ == "__main__":
    unittest.main()
