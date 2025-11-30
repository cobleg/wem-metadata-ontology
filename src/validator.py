from typing import List, Dict, Any
from .models import ValidationRule, Ontology

class ValidationResult:
    def __init__(self, is_valid: bool, violations: List[str] = [], alternatives: List[str] = []):
        self.is_valid = is_valid
        self.violations = violations
        self.alternatives = alternatives

class Validator:
    def __init__(self, ontology: Ontology):
        self.ontology = ontology

    def validate_operation(self, operation: str, params: Dict[str, Any]) -> ValidationResult:
        violations = []
        alternatives = []

        # Example validation logic based on rules
        # In a real implementation, this would be more dynamic
        
        # Rule: AGG-001 - Service Aggregation
        if 'market_service' in params and isinstance(params['market_service'], list) and len(params['market_service']) > 1:
            if not params.get('aggregate_services', False):
                violations.append("AGG-001: Cannot aggregate across market services without explicit flag")
                alternatives.append("Set aggregate_services=true")
                alternatives.append("Run separate calculations per service")

        # Rule: STOR-001 - Storage Flow Separation
        if params.get('facility_type') == 'Storage' and not params.get('separate_storage_flows', False):
             violations.append("STOR-001: Storage facilities require separate flows for accurate pricing")
             alternatives.append("Set separate_storage_flows=true")

        if violations:
            return ValidationResult(False, violations, alternatives)
        
        return ValidationResult(True)
