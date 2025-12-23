from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from database import Base

class TrackingEvent(Base):
    __tablename__ = "tracking_events"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    shipment_id = Column(UUID(as_uuid=True), ForeignKey("shipments.id"), nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    
    # Event Details
    status = Column(String(50))  # booked, in_transit, arrived, etc.
    location = Column(String(200))
    vessel_name = Column(String(100))
    voyage_number = Column(String(50))
    container_number = Column(String(20))
    
    # Description
    description = Column(Text)
    remarks = Column(Text)
    
    # Estimated Times
    estimated_datetime = Column(DateTime(timezone=True))
    actual_datetime = Column(DateTime(timezone=True))
    
    # Documents
    documents = Column(JSONB, default=list)  # URLs to related docs
    
    # Metadata
    is_milestone = Column(Boolean, default=False)
    verified = Column(Boolean, default=False)
    
    # Timestamps
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    shipment = relationship("Shipment", back_populates="tracking_events")
    creator = relationship("User")
