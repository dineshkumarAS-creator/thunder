from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime
from uuid import UUID

# --- Booking Schemas ---
class BookingRequest(BaseModel):
    carrier: str = Field(..., example="MAERSK")
    origin: str = Field(..., example="INMAA")
    destination: str = Field(..., example="SGSIN")
    containerType: str = Field(..., example="40HC")
    quantity: int = Field(..., example=2)

class BookingResponse(BaseModel):
    bookingNumber: str = Field(..., example="BK12345678")
    carrier: str = Field(..., example="MAERSK")
    status: str = Field(..., example="CONFIRMED")
    vessel: Optional[str] = Field(None, example="MAERSK ESSEX")
    etd: Optional[date] = Field(None, example="2025-01-25")

class BookingStatusResponse(BaseModel):
    bookingNumber: str = Field(..., example="BK12345678")
    carrier: str = Field(..., example="MSC")
    status: str = Field(..., example="CONFIRMED")
    containerAllocated: bool = Field(..., example=True)

# --- Schedule Schemas ---
class ScheduleResponse(BaseModel):
    carrier: str = Field(..., example="CMA_CGM")
    vessel: str = Field(..., example="CMA CGM MARCO POLO")
    etd: date = Field(..., example="2025-01-22")
    eta: date = Field(..., example="2025-02-10")
    transitDays: int = Field(..., example=19)

# --- Rates Schemas ---
class RateRequest(BaseModel):
    origin: str = Field(..., example="INMUN")
    destination: str = Field(..., example="NLRTM")
    containerType: str = Field(..., example="20GP")

class RateResponse(BaseModel):
    carrier: str = Field(..., example="HAPAG_LLOYD")
    containerType: str = Field(..., example="40HC")
    rateUSD: float = Field(..., example=1850)
    currency: str = Field(..., example="USD")
    validity: date = Field(..., example="2025-02-15")

# --- Tracking Schemas ---
class ContainerTrackingResponse(BaseModel):
    containerNumber: str = Field(..., example="MSKU1234567")
    carrier: str = Field(..., example="MAERSK")
    currentLocation: str = Field(..., example="Port of Singapore")
    status: str = Field(..., example="IN_TRANSIT")
    lastUpdated: datetime = Field(..., example="2025-01-18T10:30:00Z")

class BLStatusResponse(BaseModel):
    blNumber: str = Field(..., example="BL987654")
    carrier: str = Field(..., example="ONE")
    status: str = Field(..., example="RELEASED")
    releaseDate: date = Field(..., example="2025-01-20")

# --- AI Prediction Schemas ---
class RatePredictionRequest(BaseModel):
    origin: str = Field(..., example="INMUN")
    destination: str = Field(..., example="NLRTM")
    carrier: str = Field(..., example="MAERSK")
    containerType: str = Field(..., example="40HC")
    currentRateUSD: float = Field(..., example=1850)

class RatePredictionResponse(BaseModel):
    predictedRateUSD: float = Field(..., example=2100)
    trend: str = Field(..., example="UP")
    confidenceScore: float = Field(..., example=0.82)
    recommendation: str = Field(..., example="Book early before rates increase")
