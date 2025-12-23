from sqlalchemy import Column, String, Text, Float, Integer, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from database import Base

class Quote(Base):
    __tablename__ = "quotes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    shipment_id = Column(UUID(as_uuid=True), ForeignKey("shipments.id"), nullable=False)
    forwarder_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Quote Details
    freight_amount_usd = Column(Float, nullable=False)
    fuel_surcharge = Column(Float, default=0.0)
    thc_charges = Column(Float, default=0.0)  # Terminal Handling Charges
    documentation_charges = Column(Float, default=0.0)
    other_charges = Column(Float, default=0.0)
    total_amount_usd = Column(Float, nullable=False)
    
    # Validity
    validity_date = Column(DateTime(timezone=True))
    transit_time_days = Column(Integer)
    free_days_at_destination = Column(Integer, default=7)
    
    # Routing
    routing = Column(Text)  # Port rotation
    vessel_name = Column(String(100))
    voyage_number = Column(String(50))
    
    # Container Details
    container_type = Column(String(20))
    container_quantity = Column(Integer, default=1)
    
    # Status
    status = Column(Enum(
        'pending', 'accepted', 'rejected', 'expired',
        name='quote_status'
    ), default='pending')
    
    # Remarks
    remarks = Column(Text)
    terms_and_conditions = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    shipment = relationship("Shipment", back_populates="quotes")
    forwarder = relationship("User", foreign_keys=[forwarder_id])
    
    def calculate_total(self):
        """Calculate total amount"""
        self.total_amount_usd = (
            self.freight_amount_usd +
            self.fuel_surcharge +
            self.thc_charges +
            self.documentation_charges +
            self.other_charges
        )
    
    @property
    def forwarder_name(self):
        """Get forwarder name from relationship"""
        return self.forwarder.name if self.forwarder else ""
    
    @property
    def forwarder_company(self):
        """Get forwarder company from relationship"""
        return self.forwarder.company_name if self.forwarder else ""

