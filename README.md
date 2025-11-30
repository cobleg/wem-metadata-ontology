# WEM Metadata Ontology MCP

This MCP server provides a semantic layer for the WEM (Wholesale Electricity Market) data. It acts as a source of truth for domain knowledge, validation rules, and database mappings.

## Guiding Notes for AI

When using this tool, follow these guidelines to ensure accurate data analysis:

### 1. Validate First
Before constructing complex SQL queries or performing data analysis, always call `validate_operation` with your intended parameters.
- **Why?** To catch semantic errors like invalid aggregations (e.g., summing prices) or missing flags (e.g., storage flow separation).

### 2. Check Data Catalog
Use `get_table_mapping` to find the correct physical table for a concept. Do not guess table names.
- **Concepts**: `DispatchPrice`, `DispatchQuantity`, `SCADA`, `DateValidation`.

### 3. Handle Intervals Correctly
Use `get_conversion_rule` when dealing with different time intervals (e.g., 5-min Dispatch vs 30-min Trading).
- **Rule**: Never mix intervals without explicit conversion logic.

### 4. Consult WEM Rules
Use `get_concept_definition` to find the governing WEM Rule (e.g., "Clause 3.9") for a concept.
- **Why?** To ensure your analysis aligns with the legal and operational framework.

### 5. Use Facility Classes & Technology Types
Distinguish between `Scheduled`, `Non-Scheduled`, `IGS`, `ESR`, etc.
- **Why?** Different classes have different obligations (e.g., dispatch compliance) which affect data interpretation.

### 6. Leverage Wikidata
Use the `wikidata_mapping` property in concept definitions to link internal WEM data to external knowledge graphs (e.g., finding the location or owner of a facility).

## Tools

- `validate_operation(operation, parameters)`: Validates semantic correctness.
- `get_conversion_rule(source_interval, target_interval)`: Returns conversion logic.
- `get_table_mapping(concept)`: Returns physical table and columns.

## Project Structure

- `ontology/`: YAML files defining the ontology.
- `src/`: Python source code.
- `tests/`: Verification scripts.
