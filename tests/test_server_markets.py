import unittest
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.server import get_concept_definition, list_concepts

class TestServerMarkets(unittest.TestCase):
    def test_list_concepts(self):
        """Verify markets are listed in hierarchy."""
        import json
        concepts_json = list_concepts()
        concepts = json.loads(concepts_json)
        
        self.assertIn("Markets", concepts)
        self.assertIn("RTM", concepts["Markets"])
        self.assertIn("procures", concepts["Markets"]["RTM"])
        self.assertIn("Energy", concepts["Markets"]["RTM"]["procures"])

    def test_get_market_definition(self):
        """Verify market definition retrieval."""
        rtm_def = get_concept_definition("RTM")
        self.assertIn("'abbreviation': 'RTM'", rtm_def)
        self.assertIn("'name': 'Real-Time Market'", rtm_def)

        stem_def = get_concept_definition("STEM")
        self.assertIn("'abbreviation': 'STEM'", stem_def)
        
        rcm_def = get_concept_definition("RCM")
        self.assertIn("'abbreviation': 'RCM'", rcm_def)

if __name__ == "__main__":
    unittest.main()
