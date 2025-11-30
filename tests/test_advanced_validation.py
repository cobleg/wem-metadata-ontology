import sys
import os
sys.path.append(os.getcwd())
import pytest
from src.loader import OntologyLoader
from src.validator import Validator

def test_advanced_validation():
    ontology_dir = os.path.join(os.getcwd(), 'ontology')
    loader = OntologyLoader(ontology_dir)
    ontology = loader.get_ontology()
    validator = Validator(ontology)

    # 1. Test Interval Mismatch
    print("Testing Interval Mismatch...")
    result = validator.validate_operation("any", {
        "source_interval": "DispatchInterval",
        "target_interval": "TradingInterval"
    })
    # Should be valid because conversion rule exists
    assert result.is_valid == True, f"Expected valid interval conversion, got {result.violations}"

    result = validator.validate_operation("any", {
        "source_interval": "DispatchInterval",
        "target_interval": "SettlementPeriod"
    })
    # Should be invalid (no rule)
    assert result.is_valid == False
    assert "Interval Mismatch" in result.violations[0]

    # 2. Test Unit Validation
    print("Testing Unit Validation...")
    result = validator.validate_operation("dispatch_weighted_price", {
        "units": {
            "quantity": "MW",
            "price": "AUD/MWh"
        }
    })
    assert result.is_valid == True

    result = validator.validate_operation("dispatch_weighted_price", {
        "units": {
            "quantity": "MWh", # Wrong unit for quantity in this context
            "price": "AUD/MWh"
        }
    })
    assert result.is_valid == False
    assert "Unit Mismatch" in result.violations[0]

    # 3. Test Market Service Compatibility
    print("Testing Market Service Compatibility...")
    result = validator.validate_operation("aggregation", {
        "market_services": ["RegulationRaise", "RegulationLower"]
    })
    assert result.is_valid == True

    result = validator.validate_operation("aggregation", {
        "market_services": ["Energy", "RegulationRaise"]
    })
    assert result.is_valid == False
    assert "Incompatible Services" in result.violations[0]

    # 4. Test Facility Type Constraints
    print("Testing Facility Type Constraints...")
    result = validator.validate_operation("dispatch_weighted_price", {
        "facility_type": "Storage",
        "separate_flows": True
    })
    assert result.is_valid == True

    result = validator.validate_operation("dispatch_weighted_price", {
        "facility_type": "Storage",
        "separate_flows": False
    })
    assert result.is_valid == False
    assert "Facility Constraint" in result.violations[0]

if __name__ == "__main__":
    test_advanced_validation()
    print("All advanced validation tests passed!")
