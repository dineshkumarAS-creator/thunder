import httpx
from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import schemas, models

CARRIER_API_URL = "https://virtserver.swaggerhub.com/demo/global-carrier-api/1.0.0"

class CarrierService:
    def __init__(self, db: Session):
        self.db = db

    async def create_booking(self, data: schemas.BookingRequest):
        url = f"{CARRIER_API_URL}/booking/create"
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data.model_dump())
        
        if response.status_code != 201:
            raise HTTPException(status_code=response.status_code, detail="Booking failed")
        
        result = response.json()
        
        # Save to DB
        booking = models.CarrierBooking(
            booking_number=result.get("bookingNumber"),
            carrier=result.get("carrier"),
            origin=data.origin,
            destination=data.destination,
            container_type=data.containerType,
            quantity=data.quantity,
            status=result.get("status"),
            vessel=result.get("vessel"),
            etd=result.get("etd"), # Make sure date parsing works if string is returned
            metadata_=result
        )
        self.db.add(booking)
        self.db.commit()
        self.db.refresh(booking)
        return result

    async def get_booking_status(self, booking_number: str):
        url = f"{CARRIER_API_URL}/booking/status/{booking_number}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        
        if response.status_code != 200:
             raise HTTPException(status_code=response.status_code, detail="Failed to fetch booking status")
        return response.json()

    async def search_schedule(self, origin: str, destination: str):
        url = f"{CARRIER_API_URL}/schedule/search"
        params = {"origin": origin, "destination": destination}
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
        
        if response.status_code != 200:
             raise HTTPException(status_code=response.status_code, detail="Failed to fetch schedules")
        return response.json()

    async def get_rate_quote(self, data: schemas.RateRequest):
        url = f"{CARRIER_API_URL}/rates/quote"
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data.model_dump())
        
        if response.status_code != 200:
             raise HTTPException(status_code=response.status_code, detail="Failed to fetch rate quote")
        return response.json()

    async def track_container(self, container_number: str):
        url = f"{CARRIER_API_URL}/tracking/container/{container_number}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        
        if response.status_code != 200:
             raise HTTPException(status_code=response.status_code, detail="Failed to track container")
        return response.json()

    async def predict_rates(self, data: schemas.RatePredictionRequest):
        url = f"{CARRIER_API_URL}/ai/rates/predict"
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data.model_dump())
        
        if response.status_code != 200:
             raise HTTPException(status_code=response.status_code, detail="Failed to predict rates")
        return response.json()
