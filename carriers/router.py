from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from . import schemas, service

router = APIRouter(
    prefix="/api/carriers",
    tags=["Global Carriers"]
)

@router.post("/booking/create", response_model=schemas.BookingResponse)
async def create_booking(request: schemas.BookingRequest, db: Session = Depends(get_db)):
    carrier_service = service.CarrierService(db)
    return await carrier_service.create_booking(request)

@router.get("/booking/status/{booking_number}", response_model=schemas.BookingStatusResponse)
async def get_booking_status(booking_number: str, db: Session = Depends(get_db)):
    carrier_service = service.CarrierService(db)
    return await carrier_service.get_booking_status(booking_number)

@router.get("/schedule/search", response_model=schemas.ScheduleResponse) # The mock returns a single object in example, but realistically list. Assuming object for now as per spec example
async def search_schedule(origin: str, destination: str, db: Session = Depends(get_db)):
    carrier_service = service.CarrierService(db)
    return await carrier_service.search_schedule(origin, destination)

@router.post("/rates/quote", response_model=schemas.RateResponse)
async def get_rate_quote(request: schemas.RateRequest, db: Session = Depends(get_db)):
    carrier_service = service.CarrierService(db)
    return await carrier_service.get_rate_quote(request)

@router.get("/tracking/container/{container_number}", response_model=schemas.ContainerTrackingResponse)
async def track_container(container_number: str, db: Session = Depends(get_db)):
    carrier_service = service.CarrierService(db)
    return await carrier_service.track_container(container_number)

@router.post("/ai/rates/predict", response_model=schemas.RatePredictionResponse)
async def predict_rates(request: schemas.RatePredictionRequest, db: Session = Depends(get_db)):
    carrier_service = service.CarrierService(db)
    return await carrier_service.predict_rates(request)
