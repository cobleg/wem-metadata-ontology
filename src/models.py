from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class IntervalType(BaseModel):
    duration_minutes: Optional[int] = None
    duration_seconds: Optional[int] = None
    alignment: Optional[str] = None
    duration_unit: Optional[str] = None

class ConversionRule(BaseModel):
    source: str
    target: str
    cardinality: str
    factor: Optional[float] = None
    aggregation: str
    edge_cases: Dict[str, str]
    validation: Optional[str] = None

class MarketService(BaseModel):
    dispatch_interval: Optional[str] = None
    pricing_interval: str
    settlement_interval: Optional[str] = None
    category: Optional[str] = None
    wem_rule_reference: Optional[str] = None
    compatible_with: Optional[List[str]] = None
    aggregation_rules: Optional[Dict[str, Any]] = None

class Market(BaseModel):
    name: str
    abbreviation: str
    description: str
    function: str
    mechanism: str
    participation: Optional[str] = None
    wem_rule_reference: Optional[str] = None
    procures: Optional[List[str]] = None
    related_tables: Optional[List[str]] = None

class FacilityClass(BaseModel):
    name: str
    description: str
    wem_rule_reference: str

class TechnologyType(BaseModel):
    name: str
    description: str
    wem_rule_reference: str
    rcm_eligibility: Optional[List[str]] = None
    rcm_liability: Optional[List[str]] = None

class FacilityType(BaseModel):
    flows: List[str]
    separate_flows_default: bool = False
    requires: Optional[str] = None
    wikidata_mapping: Optional[Dict[str, str]] = None
    default_class: Optional[str] = None
    default_technology: Optional[str] = None
    quantity_interpretation: Optional[Dict[str, str]] = None
    calculation_requirements: Optional[Dict[str, str]] = None
    capacity_factor_notes: Optional[str] = None
    rcm_eligibility: Optional[List[str]] = None
    rcm_liability: Optional[List[str]] = None

class QuantityType(BaseModel):
    name: str
    unit: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    source: Optional[str] = None
    aliases: Optional[List[str]] = None
    applies_to: Optional[List[str]] = None
    formula: Optional[str] = None
    valid_range: Optional[List[float]] = None
    requires: Optional[List[str]] = None
    time_period: Optional[str] = None
    interpretation: Optional[str] = None
    abstract: Optional[bool] = False
    variants: Optional[Dict[str, 'QuantityType']] = None
    definition: Optional[str] = None
    required_for: Optional[List[str]] = None
    last_modified: Optional[str] = None
    changes: Optional[str] = None

class RelationshipType(BaseModel):
    name: str
    inverse: Optional[str] = None
    description: str
    category: str

class PriceType(BaseModel):
    granularity: str
    scope: str
    derived_from: Optional[List[str]] = None

class TableMapping(BaseModel):
    concept: str
    columns: Dict[str, str]
    constraints: List[Dict[str, Any]] = []

class ValidationRule(BaseModel):
    id: str
    category: str
    severity: str
    condition: str
    message: str

class DomainInstance(BaseModel):
    name: str
    type: str
    description: str
    uri: Optional[str] = None
    location: Optional[str] = None

class EnergySource(BaseModel):
    name: str
    wikidata_id: str
    color_hex: str

# New Validation Models
class UnitValidation(BaseModel):
    inputs: Dict[str, Dict[str, str]]
    output: Dict[str, Any]
    validation: Optional[str] = None
    formula: Optional[str] = None

class OperationDefinition(BaseModel):
    required_inputs: List[str]
    join_conditions: Optional[List[Dict[str, str]]] = None
    filters: Optional[List[str]] = None
    aggregation: Optional[Dict[str, Any]] = None
    special_cases: Optional[Dict[str, Any]] = None
    validation: Optional[List[str]] = None
    parameters: Optional[List[Dict[str, Any]]] = None
    validation_logic: Optional[List[Dict[str, Any]]] = None
    returns: Optional[List[Dict[str, Any]]] = None

class DataQualityRule(BaseModel):
    minimum_completeness: Optional[float] = None
    handling_missing_data: Optional[str] = None
    flags_to_check: Optional[List[str]] = None

class OntologyMetadata(BaseModel):
    version: str
    last_updated: str
    description: Optional[str] = None

class WEMRule(BaseModel):
    id: str
    title: str
    content: str
    section: str
    conditions: List[str] = []
    actions: List[str] = []
    entities: List[str] = []
    effective_date: Optional[str] = None
    types: List[str] = []

class Ontology(BaseModel):
    metadata: Optional[OntologyMetadata] = None
    wem_rules: Dict[str, WEMRule] = {}
    interval_types: Dict[str, IntervalType]
    conversion_rules: List[ConversionRule]
    markets: Dict[str, Market] = {}
    market_services: Dict[str, MarketService]
    facility_classes: Dict[str, FacilityClass] = {}
    technology_types: Dict[str, TechnologyType] = {}
    facility_types: Dict[str, FacilityType]
    price_types: Dict[str, PriceType]
    quantity_types: Dict[str, QuantityType] = {}
    relationships: Dict[str, RelationshipType] = {}
    tables: Dict[str, TableMapping]
    rules: List[ValidationRule]
    domain_instances: List[DomainInstance] = []
    energy_sources: Dict[str, EnergySource] = {}
    
    # New sections
    unit_validation: Dict[str, UnitValidation] = {}
    operations: Dict[str, OperationDefinition] = {}
    data_quality_rules: Dict[str, DataQualityRule] = {}
