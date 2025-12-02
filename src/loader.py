import yaml
from pathlib import Path
from .models import Ontology

class OntologyLoader:
    def __init__(self, ontology_dir: str):
        self.ontology_dir = Path(ontology_dir)
        self.ontology = self._load_ontology()

    def _load_yaml(self, filename: str) -> dict:
        with open(self.ontology_dir / filename, 'r') as f:
            return yaml.safe_load(f)

    def _load_ontology(self) -> Ontology:
        upper = self._load_yaml('upper.yaml')
        lower = self._load_yaml('lower.yaml')
        catalog = self._load_yaml('catalog.yaml')
        rules = self._load_yaml('rules.yaml')

        # Merge dictionaries
        data = {
            'metadata': upper.get('metadata'),
            'interval_types': upper['temporal']['interval_types'],
            'conversion_rules': upper['temporal']['conversion_rules'],
            'relationships': upper.get('relationships', {}),
            'markets': lower.get('markets', {}),
            'market_services': lower['market_services'],
            'facility_classes': lower.get('facility_classes', {}),
            'technology_types': lower.get('technology_types', {}),
            'facility_types': lower['facility_types'],
            'price_types': lower['price_types'],
            'quantity_types': {**lower.get('quantity_types', {}), **{
                k: v for k, v in upper.items() 
                if k in ['NameplateCapacity', 'EnergyCapacity', 'DurationRating', 
                        'CapacityFactor', 'AvailabilityFactor', 'RoundTripEfficiency', 
                        'EquivalentFullCycles', 'SCADA']
            }},
            'tables': catalog['tables'],
            'rules': rules['rules'],
            'domain_instances': lower.get('domain_instances', []),
            'energy_sources': lower.get('energy_sources', {}),
            'unit_validation': upper.get('unit_validation', {}),
            'operations': upper.get('operations', {}),
            'data_quality_rules': upper.get('data_quality_rules', {})
        }
        
        return Ontology(**data)

    def get_ontology(self) -> Ontology:
        return self.ontology
