import sys
import os
sys.path.append(os.getcwd())
import pytest
from src.loader import OntologyLoader
from src.catalog import DataCatalog

def test_new_schemas_loaded():
    ontology_dir = os.path.join(os.getcwd(), 'ontology')
    loader = OntologyLoader(ontology_dir)
    ontology = loader.get_ontology()
    catalog = DataCatalog(ontology)

    # Verify DPVForecast
    dpv_table = catalog.get_table_for_concept("DPVForecast")
    assert dpv_table == "dpv_forecast"
    
    dpv_columns = catalog.get_columns("dpv_forecast")
    assert "timestamp" in dpv_columns
    assert "value" in dpv_columns
    assert "trading_date" in dpv_columns

    # Verify SentOutGeneration
    sent_out_table = catalog.get_table_for_concept("SentOutGeneration")
    assert sent_out_table == "sent_out_data"
    
    sent_out_columns = catalog.get_columns("sent_out_data")
    assert "timestamp" in sent_out_columns
    assert "quantity" in sent_out_columns
    assert sent_out_columns["quantity"] == "Total Sent Out Generation (MWh)"

    # Verify Alias and Table Lookup via Server Logic
    # We need to mock the server's get_concept_definition logic or test it directly if we can import it.
    # Since get_concept_definition is a tool, we can test the logic by instantiating the server or extracting the logic.
    # For simplicity, let's verify the ontology structure first.
    
    assert "SentOutData" in ontology.quantity_types["SentOutGeneration"].aliases
    assert "SentOut" in ontology.quantity_types["SentOutGeneration"].aliases
    assert "DPV" in ontology.quantity_types["DPVForecast"].aliases

    # To test the lookup logic, we can simulate what the server does:
    def mock_lookup(name):
        # 1. Direct
        if name in ontology.quantity_types: return "Found Direct"
        # 2. Table
        if name in ontology.tables: return "Found Table"
        # 3. Alias
        for qt in ontology.quantity_types.values():
            if qt.aliases and name in qt.aliases: return "Found Alias"
        return "Not Found"

    assert mock_lookup("SentOutGeneration") == "Found Direct"
    assert mock_lookup("sent_out_data") == "Found Table"
    assert mock_lookup("SentOutData") == "Found Alias"
    assert mock_lookup("DPV") == "Found Alias"

if __name__ == "__main__":
    test_new_schemas_loaded()
    print("All tests passed!")
