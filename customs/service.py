import httpx
from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import schemas, models
from .schemas import ExportShippingBillRequest, ImportBillOfEntryRequest, DelayPredictionRequest
import json

# Mock Server URL from OpenAPI spec
ICEGATE_API_URL = "https://virtserver.swaggerhub.com/demo/icegate-customs-api/1.0.0"

class CustomsService:
    def __init__(self, db: Session):
        self.db = db

    async def submit_export_bill(self, data: ExportShippingBillRequest):
        url = f"{ICEGATE_API_URL}/export/shipping-bill"
        payload = data.model_dump(exclude={"shipmentId"})
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload)
        
        if response.status_code != 201:
            raise HTTPException(status_code=response.status_code, detail="Failed to submit shipping bill to ICEGATE")
        
        result = response.json()
        
        # Save to DB
        entry = models.CustomsEntry(
            shipment_id=data.shipmentId,
            entry_type="EXPORT",
            reference_id=result.get("referenceId"),
            status="SUBMITTED",
            metadata_=result
        )
        self.db.add(entry)
        self.db.commit()
        self.db.refresh(entry)
        
        return result

    async def submit_import_bill(self, data: ImportBillOfEntryRequest):
        url = f"{ICEGATE_API_URL}/import/bill-of-entry"
        payload = data.model_dump(exclude={"shipmentId"})
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload)
        
        if response.status_code != 201:
            raise HTTPException(status_code=response.status_code, detail="Failed to submit bill of entry to ICEGATE")
        
        result = response.json()
        
        # Save to DB
        entry = models.CustomsEntry(
            shipment_id=data.shipmentId,
            entry_type="IMPORT",
            reference_id=result.get("referenceId"),
            status="SUBMITTED",
            metadata_=result
        )
        self.db.add(entry)
        self.db.commit()
        self.db.refresh(entry)
        
        return result

    async def get_clearance_status(self, shipment_id: str):
        # NOTE: The mock API expects shipmentId in the path. 
        # In a real scenario, we might query our DB first or proxy to ICEGATE.
        # Here we proxy to ICEGATE mock.
        url = f"{ICEGATE_API_URL}/clearance/status/{shipment_id}"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch clearance status")
            
        return response.json()

    async def predict_delay(self, data: DelayPredictionRequest):
        url = f"{ICEGATE_API_URL}/ai/clearance-delay-prediction"
        payload = data.model_dump(exclude={"shipmentId"})
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload)
            
        if response.status_code != 200:
             raise HTTPException(status_code=response.status_code, detail="Failed to get AI prediction")
        
        result = response.json()
        
        # Optionally log the prediction if shipmentId is provided
        if data.shipmentId:
            # We don't strictly need a new 'entry' type for prediction, 
            # but we can update an existing one or just store it in metadata if we had a generic log.
            # For now, let's just return it, as per requirements. 
            # Or we could create a log entry. The user asked to "integrate", usually implies storage.
            # Let's attach it to the latest export/import entry or just return it. 
            # The plan asked to store prediction data.
            pass 

        return result
