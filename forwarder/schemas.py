from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class QuoteCreate(BaseModel):
    freight_amount_usd: float = Field(..., gt=0, description="Base freight charges")
    fuel_surcharge: float = Field(0.0, ge=0, description="BAF - Bunker Adjustment Factor")
    thc_charges: float = Field(0.0, ge=0, description="Terminal Handling Charges")
    documentation_charges: float = Field(0.0, ge=0, description="BL fee, documentation")
    other_charges: float = Field(0.0, ge=0, description="Seal charges, etc.")
    validity_date: datetime = Field(..., description="Quote validity until")
    transit_time_days: int = Field(..., gt=0, description="Estimated transit time")
    free_days_at_destination: int = Field(7, ge=0, description="Free days at destination port")
    routing: str = Field(..., min_length=5, description="Port rotation: Shanghai → Singapore → JNPT")
    vessel_name: Optional[str] = None
    voyage_number: Optional[str] = None
    container_type: Optional[str] = None
    container_quantity: int = Field(1, ge=1)
    remarks: Optional[str] = None
    terms_and_conditions: Optional[str] = Field(
        None,
        description="Credit terms, payment terms, liability clauses"
    )

class QuoteResponse(BaseModel):
    id: str
    shipment_id: str
    forwarder_id: str
    forwarder_name: str
    forwarder_company: str
    
    freight_amount_usd: float
    fuel_surcharge: float
    thc_charges: float
    documentation_charges: float
    other_charges: float
    total_amount_usd: float
    
    validity_date: datetime
    transit_time_days: int
    free_days_at_destination: int
    
    routing: str
    vessel_name: Optional[str]
    voyage_number: Optional[str]
    container_type: Optional[str]
    container_quantity: int
    
    status: str
    remarks: Optional[str]
    terms_and_conditions: Optional[str]
    
    created_at: datetime
    updated_at: Optional[datetime]

class TrackingUpdate(BaseModel):
    status: str = Field(..., description="Current shipment status")
    location: str = Field(..., description="Current location")
    description: str = Field(..., description="Event description")
    remarks: Optional[str] = None
    estimated_datetime: Optional[datetime] = None
    actual_datetime: Optional[datetime] = None
    documents: Optional[list] = Field(default_factory=list)

class ShipmentSummary(BaseModel):
    id: str
    shipment_number: str
    origin_port: str
    destination_port: str
    cargo_type: str
    gross_weight_kg: float
    volume_cbm: float
    preferred_etd: datetime
    status: str
    created_at: datetime
    has_documents: bool
    document_count: int
    quote_count: int
