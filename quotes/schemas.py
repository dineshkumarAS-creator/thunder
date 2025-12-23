from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

class QuoteStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    EXPIRED = "expired"

class QuoteCreate(BaseModel):
    freight_amount_usd: float = Field(..., gt=0)
    fuel_surcharge: float = Field(0.0, ge=0)
    thc_charges: float = Field(0.0, ge=0)
    documentation_charges: float = Field(0.0, ge=0)
    other_charges: float = Field(0.0, ge=0)
    validity_date: datetime
    transit_time_days: int = Field(..., gt=0)
    free_days_at_destination: int = Field(7, ge=0)
    routing: str
    vessel_name: Optional[str] = None
    voyage_number: Optional[str] = None
    container_type: Optional[str] = None
    container_quantity: int = Field(1, ge=1)
    remarks: Optional[str] = None
    terms_and_conditions: Optional[str] = None
    
    @validator('total_amount_usd', always=True)
    def calculate_total(cls, v, values):
        """Calculate total amount automatically"""
        if values:
            total = (
                values.get('freight_amount_usd', 0) +
                values.get('fuel_surcharge', 0) +
                values.get('thc_charges', 0) +
                values.get('documentation_charges', 0) +
                values.get('other_charges', 0)
            )
            return total
        return v

class QuoteUpdate(BaseModel):
    status: QuoteStatus
    remarks: Optional[str] = None

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
    
    status: QuoteStatus
    remarks: Optional[str]
    terms_and_conditions: Optional[str]
    
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True
