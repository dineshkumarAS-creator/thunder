from pydantic import BaseModel, Field, condecimal
from typing import List, Optional
from uuid import UUID
from datetime import datetime

# --- Export Schemas ---

class ExportShippingBillRequest(BaseModel):
    exporterName: str = Field(..., example="ABC Exports Pvt Ltd")
    invoiceNumber: str = Field(..., example="INV-EXP-1001")
    portOfLoading: str = Field(..., example="Chennai")
    goodsValue: float = Field(..., example=1250000)
    shipmentId: UUID = Field(..., description="Internal Shipment ID to link the filing")

class SubmissionResponse(BaseModel):
    message: str = Field(..., example="Submitted successfully")
    referenceId: str = Field(..., example="ICEGATE-REF-12345")

# --- Import Schemas ---

class ImportBillOfEntryRequest(BaseModel):
    importerName: str = Field(..., example="XYZ Imports Ltd")
    invoiceNumber: str = Field(..., example="INV-IMP-2001")
    portOfDischarge: str = Field(..., example="Mumbai")
    dutyAmount: float = Field(..., example=78000)
    shipmentId: UUID = Field(..., description="Internal Shipment ID to link the filing")

# --- Clearance Schemas ---

class ClearanceStatusResponse(BaseModel):
    shipmentId: str = Field(..., example="SHIP-78901")
    exportStatus: str = Field(..., example="CLEARED")
    importStatus: str = Field(..., example="PENDING")
    reason: Optional[str] = Field(None, example="Awaiting duty payment")

# --- AI Prediction Schemas ---

class DelayPredictionRequest(BaseModel):
    port: str = Field(..., example="Chennai")
    rmsExamination: bool = Field(..., example=True)
    dutyAmount: float = Field(..., example=78000)
    documentsComplete: bool = Field(..., example=False)
    shipmentId: Optional[UUID] = Field(None, description="Optional Shipment ID to log prediction")

class DelayPredictionResponse(BaseModel):
    delayRisk: str = Field(..., example="MEDIUM")
    predictedDelayDays: int = Field(..., example=2)
    confidenceScore: float = Field(..., example=0.78)
    reasons: List[str] = Field(..., example=["RMS examination required", "Port congestion"])
    recommendation: str = Field(..., example="Upload missing documents early")
