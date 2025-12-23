from sqlalchemy import Column, String, Date, Integer, DateTime, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid
from database import Base

class CarrierBooking(Base):
    __tablename__ = "carrier_bookings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    booking_number = Column(String(50), nullable=False, unique=True)
    carrier = Column(String(50), nullable=False)
    origin = Column(String(10), nullable=False)
    destination = Column(String(10), nullable=False)
    container_type = Column(String(10))
    quantity = Column(Integer)
    status = Column(String(50))
    vessel = Column(String(100))
    etd = Column(Date)
    
    # Store full API response or extra details
    metadata_ = Column("metadata", JSONB, default=dict)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
