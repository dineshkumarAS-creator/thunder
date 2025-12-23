from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from database import get_db
from auth.dependencies import require_supplier, require_forwarder, get_current_user
from auth.models import User
from shipments.models import Shipment
from quotes.models import Quote
from quotes.schemas import QuoteCreate, QuoteResponse, QuoteUpdate

router = APIRouter()

@router.get("/shipments/{shipment_id}/quotes", response_model=List[QuoteResponse])
async def get_shipment_quotes(
    shipment_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all quotes for a shipment
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
            detail="Not authorized to view quotes for this shipment"
        )
    
    if current_user.role == "forwarder":
        # Forwarders can only see their own quotes
        quotes = db.query(Quote).filter(
            Quote.shipment_id == shipment_id,
            Quote.forwarder_id == current_user.id
        ).all()
    else:
        # Supplier sees all quotes
        quotes = db.query(Quote).filter(
            Quote.shipment_id == shipment_id
        ).all()
    
    # Add forwarder details to response
    result = []
    for quote in quotes:
        forwarder = db.query(User).filter(User.id == quote.forwarder_id).first()
        quote_data = QuoteResponse.from_orm(quote)
        quote_data.forwarder_name = forwarder.name if forwarder else "Unknown"
        quote_data.forwarder_company = forwarder.company_name if forwarder else "Unknown"
        result.append(quote_data)
    
    return result

@router.post("/shipments/{shipment_id}/accept-quote", response_model=QuoteResponse)
async def accept_quote(
    shipment_id: str,
    quote_id: str,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(require_supplier),
    db: Session = Depends(get_db)
):
    """
    Accept a quote (Supplier only)
    """
    shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shipment not found"
        )
    
    if str(shipment.supplier_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to accept quotes for this shipment"
        )
    
    quote = db.query(Quote).filter(
        Quote.id == quote_id,
        Quote.shipment_id == shipment_id
    ).first()
    
    if not quote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quote not found"
        )
    
    if quote.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Quote is already {quote.status}"
        )
    
    # Check if quote is expired
    if quote.validity_date and quote.validity_date < datetime.now():
        quote.status = "expired"
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quote has expired"
        )
    
    # Update quote status
    quote.status = "accepted"
    
    # Update shipment status
    shipment.status = "quoted"
    
    # Reject all other pending quotes for this shipment
    db.query(Quote).filter(
        Quote.shipment_id == shipment_id,
        Quote.id != quote_id,
        Quote.status == "pending"
    ).update({"status": "rejected"})
    
    db.commit()
    db.refresh(quote)
    
    # Notify forwarder
    background_tasks.add_task(
        notify_quote_accepted,
        str(quote.forwarder_id),
        str(quote.id),
        str(shipment_id)
    )
    
    # Get forwarder details for response
    forwarder = db.query(User).filter(User.id == quote.forwarder_id).first()
    quote_data = QuoteResponse.from_orm(quote)
    quote_data.forwarder_name = forwarder.name if forwarder else "Unknown"
    quote_data.forwarder_company = forwarder.company_name if forwarder else "Unknown"
    
    return quote_data

@router.put("/quotes/{quote_id}", response_model=QuoteResponse)
async def update_quote(
    quote_id: str,
    update_data: QuoteUpdate,
    current_user: User = Depends(require_forwarder),
    db: Session = Depends(get_db)
):
    """
    Update quote (Forwarder only - for withdrawal, etc.)
    """
    quote = db.query(Quote).filter(Quote.id == quote_id).first()
    if not quote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quote not found"
        )
    
    if str(quote.forwarder_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this quote"
        )
    
    # Only allow certain status updates
    if update_data.status not in ["pending", "rejected"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot set quote to this status"
        )
    
    quote.status = update_data.status
    if update_data.remarks:
        quote.remarks = update_data.remarks
    
    db.commit()
    db.refresh(quote)
    
    # Get forwarder details for response
    forwarder = db.query(User).filter(User.id == quote.forwarder_id).first()
    quote_data = QuoteResponse.from_orm(quote)
    quote_data.forwarder_name = forwarder.name if forwarder else "Unknown"
    quote_data.forwarder_company = forwarder.company_name if forwarder else "Unknown"
    
    return quote_data

async def notify_quote_accepted(forwarder_id: str, quote_id: str, shipment_id: str):
    """Background task to notify forwarder"""
    # Implement notification logic (email, push, etc.)
    print(f"Quote {quote_id} accepted for shipment {shipment_id}. Forwarder: {forwarder_id}")
