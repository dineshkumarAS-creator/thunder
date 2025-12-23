from sqlalchemy import Column, String, ForeignKey, Enum, DateTime, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid
from database import Base

class CustomsEntry(Base):
    __tablename__ = "customs_entries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    shipment_id = Column(UUID(as_uuid=True), ForeignKey("shipments.id"), nullable=False)
    
    # EXPORT or IMPORT
    entry_type = Column(Enum('EXPORT', 'IMPORT', name='customs_entry_type'), nullable=False)
    
    # Reference ID from ICEGATE (e.g. ICEGATE-REF-12345)
    reference_id = Column(String(100), nullable=True)
    
    # Status (SUBMITTED, CLEARED, PENDING, REJECTED)
    status = Column(String(50), default="SUBMITTED")
    
    # ID of the submitted document (invoice/bill) linked to this entry
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=True)

    # Store AI prediction result or raw API response if needed
    metadata_ = Column("metadata", JSONB, default=dict)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    shipment = relationship("Shipment", backref="customs_entries")
    # document = relationship("Document") # Uncomment if Document model is available/imported
