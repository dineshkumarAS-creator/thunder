from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict
from database import get_db
from . import schemas, service

router = APIRouter(
    prefix="/api/customs",
    tags=["Customs (ICEGATE)"]
)

@router.post("/export/shipping-bill", response_model=schemas.SubmissionResponse, status_code=status.HTTP_201_CREATED)
async def submit_export_shipping_bill(
    request: schemas.ExportShippingBillRequest,
    db: Session = Depends(get_db)
):
    """
    Submit an Export Shipping Bill to ICEGATE.
    """
    customs_service = service.CustomsService(db)
    return await customs_service.submit_export_bill(request)

@router.post("/import/bill-of-entry", response_model=schemas.SubmissionResponse, status_code=status.HTTP_201_CREATED)
async def submit_import_bill_of_entry(
    request: schemas.ImportBillOfEntryRequest,
    db: Session = Depends(get_db)
):
    """
    Submit an Import Bill of Entry to ICEGATE.
    """
    customs_service = service.CustomsService(db)
    return await customs_service.submit_import_bill(request)

@router.get("/clearance/status/{shipment_id}", response_model=schemas.ClearanceStatusResponse)
async def get_clearance_status(
    shipment_id: str,
    db: Session = Depends(get_db)
):
    """
    Get the clearance status for a shipment from ICEGATE.
    """
    customs_service = service.CustomsService(db)
    return await customs_service.get_clearance_status(shipment_id)

@router.post("/ai/prediction", response_model=Dict) 
# Note: Using Dict response model or specific DelayPredictionResponse schema
# if the mock returns exactly that. The mock returns a JSON object.
# Let's use the schema if it matches, otherwise Dict is safer for a simulated backend.
# The schema DelayPredictionResponse is defined in schemas.py, let's use it.
# Actually, the mock response example has `delayRisk`, `predictedDelayDays`, etc.
# which matches our DelayPredictionResponse.
async def predict_clearance_delay(
    request: schemas.DelayPredictionRequest,
    db: Session = Depends(get_db)
):
    """
    Predict customs clearance delay using AI based on shipment details.
    """
    customs_service = service.CustomsService(db)
    return await customs_service.predict_delay(request)
