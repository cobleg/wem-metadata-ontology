from typing import List, Optional
from .models import TableMapping

class DataCatalog:
    def __init__(self, ontology):
        self.tables = ontology.tables

    def get_table_for_concept(self, concept: str) -> Optional[str]:
        for table_name, mapping in self.tables.items():
            if mapping.concept == concept:
                return table_name
        return None

    def get_columns(self, table_name: str) -> Optional[dict]:
        if table_name in self.tables:
            return self.tables[table_name].columns
        return None

    def validate_dependency(self, required_tables: List[str]) -> List[str]:
        missing = []
        for table in required_tables:
            if table not in self.tables:
                missing.append(table)
        return missing
