from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum

class DocumentType(str, Enum):
    INVOICE = "invoice"
    PACKING_LIST = "packing_list"
    COMMERCIAL_INVOICE = "commercial_invoice"
    CERTIFICATE_OF_ORIGIN = "certificate_of_origin"
    BILL_OF_LADING = "bill_of_lading"
    HOUSE_BL = "house_bl"
    MASTER_BL = "master_bl"
    TELEX_RELEASE = "telex_release"
    OTHER = "other"

class DocumentCreate(BaseModel):
    type: DocumentType
    file_name: str
    file_url: str
    file_size: int
    mime_type: str

class DocumentResponse(BaseModel):
    id: str
    shipment_id: str
    type: DocumentType
    file_name: str
    file_url: str
    file_size: int
    mime_type: str
    extracted_data: Optional[Dict[str, Any]] = None
    confidence_score: float = 0.0
    extraction_method: Optional[str] = None
    needs_review: bool = True
    created_at: datetime
    
    class Config:
        from_attributes = True

class ExtractionResponse(BaseModel):
    document_id: str
    extracted_data: Dict[str, Any]
    confidence: float
    needs_review: bool
    extraction_method: str
    processing_time_ms: Optional[int] = None

class AutoFillRequest(BaseModel):
    fields: List[str] = Field(default_factory=lambda: [
        "gross_weight_kg",
        "net_weight_kg", 
        "volume_cbm",
        "total_packages",
        "hs_code",
        "goods_description"
    ])

class AutoFillResponse(BaseModel):
    document_id: str
    shipment_id: str
    updated_fields: List[str]
    confidence: float
    extracted_values: Dict[str, Any]
