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

        # 1. Validate against Operation Definition
        if operation in self.ontology.operations:
            op_def = self.ontology.operations[operation]
            
            # Check required inputs
            for req_input in op_def.required_inputs:
                # Simplistic check: assumes params keys match input names or are present in 'inputs' dict
                # In reality, this would need to parse the input structure
                pass 

            # Check filters
            if op_def.filters:
                # Logic to check if required filters are present in params
                pass

            # Check Join Conditions
            if op_def.join_conditions:
                provided_joins = params.get('join_keys', [])
                for condition in op_def.join_conditions:
                    field = condition['field']
                    if field not in provided_joins:
                        violations.append(f"Missing Join Key: Operation requires joining on '{field}'")
                        alternatives.append(f"Add '{field}' to join_keys")

        # 2. Interval Validation
        if 'source_interval' in params and 'target_interval' in params:
            source = params['source_interval']
            target = params['target_interval']
            if source != target:
                # Check if conversion rule exists
                rule = next((r for r in self.ontology.conversion_rules if r.source == source and r.target == target), None)
                if not rule:
                    violations.append(f"Interval Mismatch: No conversion rule from {source} to {target}")
                    alternatives.append("Use get_conversion_rule() to find valid path")
                elif rule.validation:
                    # Check if specific validation requirement is met (e.g., alignment)
                    # This is a placeholder for actual logic
                    pass

        # 3. Unit Validation
        if 'units' in params:
            # params['units'] = {'quantity': 'MW', 'price': 'AUD/MWh'}
            for rule_name, rule in self.ontology.unit_validation.items():
                # Check if this rule applies (e.g., based on operation name or inputs)
                if operation == rule_name or rule_name in params.get('rules', []):
                    # Validate inputs
                    for input_name, input_def in rule.inputs.items():
                        if input_name in params['units']:
                            provided_unit = params['units'][input_name]
                            if provided_unit != input_def['unit']:
                                violations.append(f"Unit Mismatch: Expected {input_def['unit']} for {input_name}, got {provided_unit}")
                                alternatives.append(f"Convert {input_name} to {input_def['unit']}")

        # 4. Market Service Compatibility
        if 'market_services' in params and isinstance(params['market_services'], list):
            services = params['market_services']
            if len(services) > 1:
                base_service = services[0]
                if base_service in self.ontology.market_services:
                    base_def = self.ontology.market_services[base_service]
                    for other_service in services[1:]:
                        if base_def.compatible_with is not None and other_service not in base_def.compatible_with:
                            violations.append(f"Incompatible Services: {base_service} cannot be aggregated with {other_service}")
                            alternatives.append("Calculate separately")

        # 5. Facility Type Constraints
        if 'facility_type' in params:
            ftype = params['facility_type']
            if ftype in self.ontology.facility_types:
                ft_def = self.ontology.facility_types[ftype]
                
                # Check calculation requirements
                if ft_def.calculation_requirements:
                    if operation in ft_def.calculation_requirements:
                        req = ft_def.calculation_requirements[operation]
                        if req == "must_separate_charge_discharge" and not params.get('separate_flows', False):
                            violations.append(f"Facility Constraint: {ftype} requires separate flows for {operation}")
                            alternatives.append("Set separate_flows=true")
                        if req == "not_applicable":
                            violations.append(f"Invalid Operation: {operation} is not applicable for {ftype}")

        if violations:
            return ValidationResult(False, violations, alternatives)
        
        return ValidationResult(True)
