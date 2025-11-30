import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.loader import OntologyLoader
from src.validator import Validator
from src.catalog import DataCatalog

def test_ontology_load():
    print("Testing Ontology Load...")
    ontology_dir = os.path.join(os.path.dirname(__file__), '../ontology')
    loader = OntologyLoader(ontology_dir)
    ontology = loader.get_ontology()
    assert ontology is not None
    print("✅ Ontology loaded successfully")
    return ontology

def test_validation(ontology):
    print("\nTesting Validation...")
    validator = Validator(ontology)
    
    # Test 1: Invalid Aggregation
    params = {
        "market_service": ["Energy", "FCESS_Raise"],
        "aggregate_services": False
    }
    result = validator.validate_operation("calc_price", params)
    assert not result.is_valid
    assert "AGG-001" in result.violations[0]
    print("✅ Caught invalid aggregation")

    # Test 2: Invalid Storage
    params = {
        "facility_type": "Storage",
        "separate_storage_flows": False
    }
    result = validator.validate_operation("calc_price", params)
    assert not result.is_valid
    assert "STOR-001" in result.violations[0]
    print("✅ Caught invalid storage flow")

def test_catalog(ontology):
    print("\nTesting Data Catalog...")
    catalog = DataCatalog(ontology)
    
    table = catalog.get_table_for_concept("DispatchPrice")
    assert table == "dispatch_prices"
    print(f"✅ Mapped DispatchPrice -> {table}")

    cols = catalog.get_columns("dispatch_quantities")
    assert "quantity" in cols
    print(f"✅ Found columns for dispatch_quantities")

if __name__ == "__main__":
    try:
        ontology = test_ontology_load()
        test_validation(ontology)
        test_catalog(ontology)
        print("\n🎉 All tests passed!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
