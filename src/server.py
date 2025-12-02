from mcp.server.fastmcp import FastMCP
from .loader import OntologyLoader
from .validator import Validator
from .catalog import DataCatalog
from .catalog import DataCatalog
import os
from typing import List

# Initialize components
ontology_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ontology')
loader = OntologyLoader(ontology_dir)
ontology = loader.get_ontology()
validator = Validator(ontology)
catalog = DataCatalog(ontology)

mcp = FastMCP("wem-metadata-ontology")

@mcp.tool()
def get_ontology_version() -> str:
    """
    Returns the current version of the WEM Ontology.
    Useful for audit trails and ensuring compatibility.
    """
    if ontology.metadata:
        return str(ontology.metadata.dict())
    return "Version information not available."

@mcp.tool()
def compare_versions(base_ref: str, target_ref: str = "HEAD") -> str:
    """
    Compares two versions of the ontology using git.
    
    Args:
        base_ref: The base git reference (e.g., "v1.0.0" or commit hash).
        target_ref: The target git reference (default: "HEAD").
        
    Returns:
        JSON string describing added, modified, and removed concepts.
    """
    import subprocess
    import tempfile
    import shutil
    import json
    from .loader import OntologyLoader
    
    try:
        # Create temp dir to checkout old version
        with tempfile.TemporaryDirectory() as temp_dir:
            # Helper to fetch file content
            def fetch_file(ref, filename, dest_path):
                try:
                    # git show ref:path/to/file
                    # We assume the server is running from the repo root or src
                    # We need to find the relative path to ontology dir
                    # ontology_dir is defined globally as os.path.join(..., 'ontology')
                    # We can try to guess the git path.
                    # Assuming repo structure: wem-metadata-ontology/ontology/filename
                    git_path = f"ontology/{filename}"
                    
                    # Run git show
                    result = subprocess.run(
                        ["git", "show", f"{ref}:{git_path}"],
                        capture_output=True,
                        text=True,
                        cwd=os.path.dirname(ontology_dir) # Run from repo root
                    )
                    
                    if result.returncode != 0:
                        return False
                        
                    with open(dest_path, 'w') as f:
                        f.write(result.stdout)
                    return True
                except Exception as e:
                    return False

            # Load Base Version
            base_dir = os.path.join(temp_dir, "base")
            os.makedirs(base_dir)
            files = ["upper.yaml", "lower.yaml", "catalog.yaml", "rules.yaml"]
            
            for f in files:
                if not fetch_file(base_ref, f, os.path.join(base_dir, f)):
                    return f"Error: Could not fetch {f} from {base_ref}"
            
            try:
                base_loader = OntologyLoader(base_dir)
                base_ontology = base_loader.get_ontology()
            except Exception as e:
                return f"Error loading base ontology from {base_ref}: {e}"

            # Load Target Version (if not HEAD, fetch it; if HEAD, use current)
            if target_ref == "HEAD":
                target_ontology = ontology
            else:
                target_dir = os.path.join(temp_dir, "target")
                os.makedirs(target_dir)
                for f in files:
                    if not fetch_file(target_ref, f, os.path.join(target_dir, f)):
                        return f"Error: Could not fetch {f} from {target_ref}"
                try:
                    target_loader = OntologyLoader(target_dir)
                    target_ontology = target_loader.get_ontology()
                except Exception as e:
                    return f"Error loading target ontology from {target_ref}: {e}"
            
            # Compare
            diff = {
                "added_concepts": [],
                "removed_concepts": [],
                "modified_concepts": [],
                "breaking_changes": False
            }
            
            # Compare Quantity Types
            base_qt = base_ontology.quantity_types
            target_qt = target_ontology.quantity_types
            
            for name in target_qt:
                if name not in base_qt:
                    diff["added_concepts"].append(name)
                elif str(target_qt[name].dict()) != str(base_qt[name].dict()):
                    diff["modified_concepts"].append(name)
                    
            for name in base_qt:
                if name not in target_qt:
                    diff["removed_concepts"].append(name)
                    diff["breaking_changes"] = True
            
            return json.dumps(diff, indent=2)
            
    except Exception as e:
        return f"Comparison failed: {str(e)}"

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
def search_wem_rules(query: str) -> str:
    """
    Search WEM Rules by title or content.
    Returns a list of matching rules.
    """
    import json
    matches = []
    query_lower = query.lower()
    
    for rule_id, rule in ontology.wem_rules.items():
        if query_lower in rule.title.lower() or query_lower in rule.content.lower():
            matches.append(rule.dict())
            
    return json.dumps(matches, indent=2)

def _get_related_rules(concept_name: str) -> List[dict]:
    """Helper to find rules related to a concept."""
    related = []
    concept_lower = concept_name.lower()
    
    for rule_id, rule in ontology.wem_rules.items():
        # Check entities
        if any(concept_lower in entity.lower() for entity in rule.entities):
            related.append(rule.dict())
            continue
            
        # Check content
        if concept_lower in rule.content.lower():
            related.append(rule.dict())
            
    return related

@mcp.tool()
def get_concept_definition(concept_name: str) -> str:
    """
    Returns the full definition of a concept, including WEM Rules, Wikidata links, and properties.
    Search order: Market Services, Facility Types, Facility Classes, Technology Types, Quantities.
    """
    import json
    
    # Helper to search by alias
    def find_by_alias(dictionaries):
        for d in dictionaries:
            for name, item in d.items():
                if hasattr(item, 'aliases') and item.aliases and concept_name in item.aliases:
                    return item
        return None

    item = None
    
    # 1. Direct Lookup
    if concept_name in ontology.market_services:
        item = ontology.market_services[concept_name]
    elif concept_name in ontology.markets:
        item = ontology.markets[concept_name]
    elif concept_name in ontology.facility_types:
        item = ontology.facility_types[concept_name]
    elif concept_name in ontology.facility_classes:
        item = ontology.facility_classes[concept_name]
    elif concept_name in ontology.technology_types:
        item = ontology.technology_types[concept_name]
    elif concept_name in ontology.quantity_types:
        item = ontology.quantity_types[concept_name]
    
    # 2. Table Name Lookup
    elif concept_name in ontology.tables:
        mapped_concept = ontology.tables[concept_name].concept
        return get_concept_definition(mapped_concept)

    # 3. Alias Lookup
    if not item:
        item = find_by_alias([
            ontology.market_services,
            ontology.facility_types,
            ontology.facility_classes,
            ontology.technology_types,
            ontology.quantity_types
        ])

    if item:
        # Enrich with related rules
        definition = item.dict()
        related_rules = _get_related_rules(concept_name)
        if related_rules:
            definition['related_wem_rules'] = [r['id'] for r in related_rules]
            definition['related_wem_rules_details'] = related_rules[:3] # Limit details to top 3
            
        return json.dumps(definition, indent=2)

    return f"Concept '{concept_name}' not found in ontology (checked names, tables, and aliases)."

@mcp.tool()
def list_concepts() -> str:
    """
    Returns a hierarchical view of the ontology concepts.
    """
    import json
    
    structure = {
        "Markets": {},
        "Market Services": list(ontology.market_services.keys()),
        "Facility Types": list(ontology.facility_types.keys()),
        "Technology Types": list(ontology.technology_types.keys()),
        "Quantities": list(ontology.quantity_types.keys())
    }
    
    for market_name, market in ontology.markets.items():
        structure["Markets"][market_name] = {
            "name": market.name,
            "procures": market.procures
        }
        
    return json.dumps(structure, indent=2)

@mcp.tool()
def get_guidelines() -> str:
    """
    Returns guiding notes for AI agents on how to use this ontology correctly.
    """
    return """
    Guiding Notes for AI:
    1. **Validate First**: Always call `validate_operation` before constructing complex queries.
    2. **Check Data Catalog**: Use `get_table_mapping` to find physical tables (e.g., DispatchPrice -> dispatch_prices).
    3. **Advanced Validation**:
        - **Intervals**: Do not mix 5-min (Dispatch) and 30-min (Trading) data without conversion.
        - **Units**: Ensure `MW` (Power) and `MWh` (Energy) are used correctly.
        - **Services**: Do not aggregate Energy with FCESS.
        - **Storage**: Separate charge/discharge flows for price calculations.
    4. **Lookup Flexibility**: You can look up concepts by **Concept Name**, **Table Name** (e.g., `sent_out_data`), or **Alias**.
    5. **Use Tools**:
        - `get_concept_definition(name)`: Get full definition and rules.
        - `get_operation_definition(name)`: Get standard calculation patterns.
        - `validate_operation(op, params)`: Pre-validate your logic.
    """
@mcp.tool()
def get_operation_definition(operation_name: str) -> str:
    """
    Returns the definition of a standard operation, including required inputs and validation rules.
    """
    if operation_name in ontology.operations:
        return str(ontology.operations[operation_name].dict())
    return f"Operation '{operation_name}' not found. Available operations: {list(ontology.operations.keys())}"

if __name__ == "__main__":
    mcp.run()
