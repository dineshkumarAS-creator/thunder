from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List
import uuid
from datetime import datetime

from shipments.models import Shipment
from shipments.schemas import ShipmentCreate, ShipmentUpdate
from auth.models import User
from utils.helpers import generate_shipment_number

class ShipmentService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_shipment(
        self, 
        supplier_id: str, 
        buyer_id: str, 
        shipment_data: ShipmentCreate
    ) -> Shipment:
        """Create a new shipment"""
        
        # Generate shipment number
        shipment_number = generate_shipment_number()
        
        shipment = Shipment(
            shipment_number=shipment_number,
            supplier_id=supplier_id,
            buyer_id=buyer_id,
            origin_port=shipment_data.origin_port,
            destination_port=shipment_data.destination_port,
            incoterm=shipment_data.incoterm.value,
            cargo_type=shipment_data.cargo_type.value,
            container_type=shipment_data.container_type,
            container_qty=shipment_data.container_qty,
            goods_description=shipment_data.goods_description,
            hs_code=shipment_data.hs_code,
            gross_weight_kg=shipment_data.gross_weight_kg,
            net_weight_kg=shipment_data.net_weight_kg,
            volume_cbm=shipment_data.volume_cbm,
            total_packages=shipment_data.total_packages,
            package_type=shipment_data.package_type,
            preferred_etd=shipment_data.preferred_etd,
            preferred_eta=shipment_data.preferred_eta,
            declared_value_usd=shipment_data.declared_value_usd,
            insurance_required=shipment_data.insurance_required,
            status="draft",
            metadata_={
                "special_instructions": shipment_data.special_instructions,
                "created_via": "api"
            }
        )
        
        self.db.add(shipment)
        self.db.commit()
        self.db.refresh(shipment)
        
        return shipment
    
    def get_shipment_by_id(self, shipment_id: str) -> Optional[Shipment]:
        """Get shipment by ID"""
        return self.db.query(Shipment).filter(Shipment.id == shipment_id).first()
    
    def get_supplier_shipments(
        self, 
        supplier_id: str, 
        status_filter: Optional[str] = None
    ) -> List[Shipment]:
        """Get all shipments for a supplier"""
        query = self.db.query(Shipment).filter(Shipment.supplier_id == supplier_id)
        
        if status_filter:
            query = query.filter(Shipment.status == status_filter)
        
        return query.order_by(Shipment.created_at.desc()).all()
    
    def get_buyer_shipments(
        self, 
        buyer_id: str, 
        status_filter: Optional[str] = None
    ) -> List[Shipment]:
        """Get all shipments for a buyer"""
        query = self.db.query(Shipment).filter(Shipment.buyer_id == buyer_id)
        
        if status_filter:
            query = query.filter(Shipment.status == status_filter)
        
        return query.order_by(Shipment.created_at.desc()).all()
    
    def update_shipment(
        self, 
        shipment_id: str, 
        update_data: ShipmentUpdate
    ) -> Shipment:
        """Update shipment details"""
        shipment = self.get_shipment_by_id(shipment_id)
        
        if not shipment:
            return None
        
        # Update fields
        for field, value in update_data.dict(exclude_unset=True).items():
            if hasattr(shipment, field):
                setattr(shipment, field, value)
        
        shipment.updated_at = datetime.now()
        self.db.commit()
        self.db.refresh(shipment)
        
        return shipment
    
    def get_shipments_for_forwarder(
        self, 
        forwarder_id: str,
        status_filter: Optional[str] = None
    ) -> List[Shipment]:
        """Get shipments where forwarder has submitted quotes"""
        from quotes.models import Quote
        
        query = (
            self.db.query(Shipment)
            .join(Quote, Quote.shipment_id == Shipment.id)
            .filter(Quote.forwarder_id == forwarder_id)
        )
        
        if status_filter:
            query = query.filter(Shipment.status == status_filter)
        
        return query.order_by(Shipment.created_at.desc()).all()
    
    def update_shipment_from_document(
        self,
        shipment_id: str,
        extracted_data: dict
    ) -> List[str]:
        """Update shipment fields from extracted document data"""
        shipment = self.get_shipment_by_id(shipment_id)
        
        if not shipment:
            return []
        
        updated_fields = []
        
        # Map extracted fields to shipment fields
        field_mapping = {
            "total_gross_weight_kg": "gross_weight_kg",
            "total_net_weight_kg": "net_weight_kg",
            "total_volume_cbm": "volume_cbm",
            "total_packages": "total_packages",
        }
        
        for extracted_field, shipment_field in field_mapping.items():
            if extracted_field in extracted_data and extracted_data[extracted_field]:
                current_value = getattr(shipment, shipment_field)
                new_value = extracted_data[extracted_field]
                
                # Only update if different and new value is valid
                if current_value != new_value and new_value > 0:
                    setattr(shipment, shipment_field, new_value)
                    updated_fields.append(shipment_field)
        
        # Update HS code from first item
        items = extracted_data.get("items", [])
        if items and items[0].get("hs_code"):
            shipment.hs_code = items[0]["hs_code"]
            updated_fields.append("hs_code")
        
        # Update goods description
        if items and len(items) <= 3:
            descriptions = [item.get("description", "") for item in items[:3]]
            shipment.goods_description = "; ".join(filter(None, descriptions))
            updated_fields.append("goods_description")
        
        if updated_fields:
            shipment.updated_at = datetime.now()
            self.db.commit()
        
        return updated_fields
