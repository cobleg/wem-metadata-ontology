from mcp.server.fastmcp import FastMCP
from .loader import OntologyLoader
from .validator import Validator
from .catalog import DataCatalog
import os

# Initialize components
ontology_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ontology')
loader = OntologyLoader(ontology_dir)
ontology = loader.get_ontology()
validator = Validator(ontology)
catalog = DataCatalog(ontology)

mcp = FastMCP("wem-metadata-ontology")

@mcp.tool()
def validate_operation(operation: str, parameters: dict) -> str:
    """
    Validates if an operation with given parameters is semantically valid according to the WEM Ontology.
    """
    result = validator.validate_operation(operation, parameters)
    if result.is_valid:
        return "Operation is valid."
    else:
        return f"Invalid Operation:\nViolations: {result.violations}\nAlternatives: {result.alternatives}"

@mcp.tool()
def get_conversion_rule(source_interval: str, target_interval: str) -> str:
    """
    Returns the conversion rule between two interval types.
    """
    for rule in ontology.conversion_rules:
        if rule.source == source_interval and rule.target == target_interval:
            return str(rule.dict())
    return "No conversion rule found."

@mcp.tool()
def get_table_mapping(concept: str) -> str:
    """
    Returns the physical table mapping for a given ontology concept.
    """
    table = catalog.get_table_for_concept(concept)
    if table:
        columns = catalog.get_columns(table)
        return f"Table: {table}\nColumns: {columns}"
    return "No table mapping found."

@mcp.tool()
def get_concept_definition(concept_name: str) -> str:
    """
    Returns the full definition of a concept, including WEM Rules, Wikidata links, and properties.
    Search order: Market Services, Facility Types, Facility Classes, Technology Types, Quantities.
    """
    # Check Market Services
    if concept_name in ontology.market_services:
        return str(ontology.market_services[concept_name].dict())
    
    # Check Facility Types
    if concept_name in ontology.facility_types:
        return str(ontology.facility_types[concept_name].dict())

    # Check Facility Classes
    if concept_name in ontology.facility_classes:
        return str(ontology.facility_classes[concept_name].dict())

    # Check Technology Types
    if concept_name in ontology.technology_types:
        return str(ontology.technology_types[concept_name].dict())

    # Check Quantity Types
    if concept_name in ontology.quantity_types:
        return str(ontology.quantity_types[concept_name].dict())

    return f"Concept '{concept_name}' not found in ontology."

@mcp.tool()
def list_concepts() -> str:
    """
    Returns a categorized list of all available concepts in the ontology.
    Use this to discover valid concept names for get_concept_definition.
    """
    return f"""
    Market Services: {list(ontology.market_services.keys())}
    Facility Classes: {list(ontology.facility_classes.keys())}
    Facility Types: {list(ontology.facility_types.keys())}
    Technology Types: {list(ontology.technology_types.keys())}
    Quantities: {list(ontology.quantity_types.keys())}
    """

@mcp.tool()
def get_guidelines() -> str:
    """
    Returns guiding notes for AI agents on how to use this ontology correctly.
    """
    return """
    Guiding Notes for AI:
    1. **Validate First**: Always call `validate_operation` before constructing complex queries.
    2. **Check Data Catalog**: Use `get_table_mapping` to find physical tables (e.g., DispatchPrice -> dispatch_prices).
    3. **Handle Intervals**: Use `get_conversion_rule` for interval mismatches (e.g., 5-min vs 30-min).
    4. **Consult WEM Rules**: Use `get_concept_definition` to find the governing WEM Rule (e.g., "Clause 3.9") for a concept.
    5. **Use Facility Classes**: Distinguish between Scheduled, Non-Scheduled, etc., using `get_concept_definition`.
    6. **Leverage Wikidata**: Use `wikidata_mapping` in definitions to link to external knowledge graphs.
    """

if __name__ == "__main__":
    mcp.run()
