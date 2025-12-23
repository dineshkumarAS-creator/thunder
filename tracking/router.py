from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from database import get_db
from auth.dependencies import get_current_user, require_forwarder
from auth.models import User
from shipments.models import Shipment
from tracking.models import TrackingEvent
from tracking.schemas import TrackingEventCreate, TrackingEventResponse, ShipmentTrackingResponse

router = APIRouter()

@router.get("/shipments/{shipment_id}", response_model=ShipmentTrackingResponse)
async def get_shipment_tracking(
    shipment_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get complete tracking history for a shipment
    """
    shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )
    
    # Check permissions
    if current_user.role == "supplier" and str(shipment.supplier_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view tracking for this shipment"
        )
    
    if current_user.role == "buyer" and str(shipment.buyer_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view tracking for this shipment"
        )
    
    # Get all tracking events
    events = db.query(TrackingEvent).filter(
        TrackingEvent.shipment_id == shipment_id
    ).order_by(TrackingEvent.timestamp).all()
    
    # Find estimated and actual arrival
    estimated_arrival = None
    actual_arrival = None
    
    for event in events:
        if event.status == "delivered":
            actual_arrival = event.actual_datetime or event.timestamp
        elif event.estimated_datetime and not estimated_arrival:
            estimated_arrival = event.estimated_datetime
    
    return ShipmentTrackingResponse(
        shipment_id=str(shipment.id),
        shipment_number=shipment.shipment_number,
        current_status=shipment.status,
        origin_port=shipment.origin_port,
        destination_port=shipment.destination_port,
        estimated_arrival=estimated_arrival,
        actual_arrival=actual_arrival,
        events=[TrackingEventResponse.from_orm(event) for event in events]
    )

@router.post("/shipments/{shipment_id}/events", response_model=TrackingEventResponse)
async def create_tracking_event(
    shipment_id: str,
    event_data: TrackingEventCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(require_forwarder),
    db: Session = Depends(get_db)
):
    """
    Create a new tracking event (Forwarder only)
    """
    shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )
    
    # Check if forwarder is assigned to this shipment
    from quotes.models import Quote
    quote = db.query(Quote).filter(
        Quote.shipment_id == shipment_id,
        Quote.forwarder_id == current_user.id,
        Quote.status == "accepted"
    ).first()
    
    if not quote:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not the assigned forwarder for this shipment"
        )
    
    # Create tracking event
    tracking_event = TrackingEvent(
        shipment_id=shipment_id,
        created_by=current_user.id,
        status=event_data.status.value,
        location=event_data.location,
        vessel_name=event_data.vessel_name,
        voyage_number=event_data.voyage_number,
        container_number=event_data.container_number,
        description=event_data.description,
        remarks=event_data.remarks,
        estimated_datetime=event_data.estimated_datetime,
        actual_datetime=event_data.actual_datetime or datetime.now(),
        documents=event_data.documents,
        is_milestone=event_data.is_milestone
    )
    
    db.add(tracking_event)
    
    # Update shipment status if milestone
    if event_data.is_milestone:
        shipment.status = event_data.status.value
    
    db.commit()
    db.refresh(tracking_event)
    
    # Notify supplier and buyer
    background_tasks.add_task(
        notify_tracking_update,
        str(shipment.supplier_id),
        str(shipment.buyer_id),
        event_data.status.value,
        event_data.location,
        event_data.description
    )
    
    return TrackingEventResponse.from_orm(tracking_event)

@router.get("/shipments/{shipment_id}/events/latest", response_model=TrackingEventResponse)
async def get_latest_tracking_event(
    shipment_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get the latest tracking event for a shipment
    """
    shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )
    
    # Check permissions (same as above)
    if current_user.role == "supplier" and str(shipment.supplier_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    if current_user.role == "buyer" and str(shipment.buyer_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    latest_event = db.query(TrackingEvent).filter(
        TrackingEvent.shipment_id == shipment_id
    ).order_by(TrackingEvent.timestamp.desc()).first()
    
    if not latest_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No tracking events found"
        )
    
    return TrackingEventResponse.from_orm(latest_event)

async def notify_tracking_update(supplier_id: str, buyer_id: str, status: str, location: str, description: str):
    """Background task to notify about tracking updates"""
    # Implement notification logic
    print(f"Tracking update: {status} at {location} - {description}")
    print(f"Notifying supplier: {supplier_id}, buyer: {buyer_id}")
