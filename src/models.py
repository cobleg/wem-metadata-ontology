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
    dispatch_interval: str
    pricing_interval: str
    settlement_interval: Optional[str] = None
    category: Optional[str] = None
    wem_rule_reference: Optional[str] = None
    compatible_with: Optional[List[str]] = None
    aggregation_rules: Optional[Dict[str, Any]] = None

class FacilityClass(BaseModel):
    name: str
    description: str
    wem_rule_reference: str

class TechnologyType(BaseModel):
    name: str
    description: str
    wem_rule_reference: str

class FacilityType(BaseModel):
    flows: List[str]
    separate_flows_default: bool = False
    requires: Optional[str] = None
    wikidata_mapping: Optional[Dict[str, str]] = None
    default_class: Optional[str] = None
    default_technology: Optional[str] = None
    quantity_interpretation: Optional[Dict[str, str]] = None
    calculation_requirements: Optional[Dict[str, str]] = None

class QuantityType(BaseModel):
    name: str
    unit: str
    description: str
    category: str
    source: Optional[str] = None
    aliases: Optional[List[str]] = None

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

class DataQualityRule(BaseModel):
    minimum_completeness: Optional[float] = None
    handling_missing_data: Optional[str] = None
    flags_to_check: Optional[List[str]] = None

class Ontology(BaseModel):
    interval_types: Dict[str, IntervalType]
    conversion_rules: List[ConversionRule]
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
