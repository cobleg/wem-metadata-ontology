import unittest
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.loader import OntologyLoader

class TestMarkets(unittest.TestCase):
    def setUp(self):
        self.loader = OntologyLoader("ontology")
        self.ontology = self.loader.get_ontology()

    def test_markets_loaded(self):
        """Verify markets are loaded correctly."""
        self.assertIn("STEM", self.ontology.markets)
        self.assertIn("RTM", self.ontology.markets)
        self.assertIn("RCM", self.ontology.markets)
        self.assertIn("ESS", self.ontology.markets)

    def test_market_details(self):
        """Verify market details."""
        rtm = self.ontology.markets["RTM"]
        self.assertEqual(rtm.name, "Real-Time Market")
        self.assertEqual(rtm.abbreviation, "RTM")
        self.assertIn("Energy", rtm.procures)
        self.assertIn("RegulationRaise", rtm.procures)
        self.assertIn("dispatch_prices", rtm.related_tables)

        stem = self.ontology.markets["STEM"]
        self.assertEqual(stem.name, "Short Term Energy Market")
        self.assertEqual(stem.mechanism, "STEM Auction (Clause 6.9)")

    def test_ess_market(self):
        """Verify ESS market details."""
        ess = self.ontology.markets["ESS"]
        self.assertIn("RoCoF", ess.procures)
        self.assertEqual(ess.wem_rule_reference, "Clause 3.9")

if __name__ == "__main__":
    unittest.main()
