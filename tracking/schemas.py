from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class TrackingStatus(str, Enum):
    BOOKED = "booked"
    GATE_IN = "gate_in"
    VESSEL_DEPARTED = "vessel_departed"
    IN_TRANSIT = "in_transit"
    PORT_ARRIVAL = "port_arrival"
    GATE_OUT = "gate_out"
    CUSTOMS_CLEARANCE = "customs_clearance"
    DELIVERED = "delivered"
    HELD = "held"
    DELAYED = "delayed"

class TrackingEventCreate(BaseModel):
    status: TrackingStatus
    location: str = Field(..., min_length=2)
    vessel_name: Optional[str] = None
    voyage_number: Optional[str] = None
    container_number: Optional[str] = None
    description: str = Field(..., min_length=5)
    remarks: Optional[str] = None
    estimated_datetime: Optional[datetime] = None
    actual_datetime: Optional[datetime] = None
    documents: Optional[List[str]] = Field(default_factory=list)
    is_milestone: bool = False

class TrackingEventResponse(BaseModel):
    id: str
    shipment_id: str
    status: str
    location: str
    vessel_name: Optional[str]
    voyage_number: Optional[str]
    container_number: Optional[str]
    description: str
    remarks: Optional[str]
    estimated_datetime: Optional[datetime]
    actual_datetime: Optional[datetime]
    documents: List[str]
    is_milestone: bool
    verified: bool
    timestamp: datetime
    
    class Config:
        from_attributes = True

class ShipmentTrackingResponse(BaseModel):
    shipment_id: str
    shipment_number: str
    current_status: str
    origin_port: str
    destination_port: str
    estimated_arrival: Optional[datetime]
    actual_arrival: Optional[datetime]
    events: List[TrackingEventResponse]
    
    class Config:
        from_attributes = True
