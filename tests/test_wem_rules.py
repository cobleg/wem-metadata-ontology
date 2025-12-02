
import unittest
import sys
import os
import json

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.server import search_wem_rules, get_concept_definition, ontology

class TestWEMRules(unittest.TestCase):
    def test_rules_loaded(self):
        """Verify that rules are loaded into the ontology."""
        print(f"Loaded {len(ontology.wem_rules)} rules.")
        self.assertGreater(len(ontology.wem_rules), 0)

    def test_search_rules(self):
        """Verify searching for rules."""
        # Search for "Frequency" which we saw in the sample
        result_json = search_wem_rules("Frequency")
        results = json.loads(result_json)
        self.assertGreater(len(results), 0)
        print(f"Found {len(results)} rules matching 'Frequency'")
        
        # Check structure
        first_rule = results[0]
        self.assertIn("id", first_rule)
        self.assertIn("content", first_rule)

    def test_concept_linking(self):
        """Verify that get_concept_definition includes related rules."""
        # "Generator" is a key concept likely to be mentioned in rules
        definition_json = get_concept_definition("Generator")
        
        if "not found" in definition_json:
            print("Concept 'Generator' not found, skipping linking test.")
            return

        definition = json.loads(definition_json)
        
        # Check for related rules field
        self.assertIn("related_wem_rules", definition)
        self.assertIn("related_wem_rules_details", definition)
        
        print(f"Generator linked to {len(definition['related_wem_rules'])} rules.")
        self.assertGreater(len(definition['related_wem_rules']), 0)

if __name__ == "__main__":
    unittest.main()
