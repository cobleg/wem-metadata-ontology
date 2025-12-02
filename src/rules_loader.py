
import json
import os
from typing import Dict, List
from .models import WEMRule

class WEMRulesLoader:
    def __init__(self, rules_path: str):
        self.rules_path = rules_path

    def load_rules(self) -> Dict[str, WEMRule]:
        """
        Load WEM Rules from the JSON file.
        """
        if not os.path.exists(self.rules_path):
            print(f"Warning: WEM Rules file not found at {self.rules_path}")
            return {}

        try:
            with open(self.rules_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            rules = {}
            for item in data:
                # Validate and create WEMRule object
                # We use .get() to handle potential missing fields gracefully, 
                # though the model defines defaults for lists.
                rule = WEMRule(
                    id=item.get("id"),
                    title=item.get("title", ""),
                    content=item.get("content", ""),
                    section=item.get("section", ""),
                    conditions=item.get("conditions", []),
                    actions=item.get("actions", []),
                    entities=item.get("entities", []),
                    effective_date=item.get("effective_date"),
                    types=item.get("types", [])
                )
                rules[rule.id] = rule
            
            return rules
            
        except Exception as e:
            print(f"Error loading WEM Rules: {e}")
            return {}
