from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
import os
import tempfile
import uuid

from database import get_db
from auth.dependencies import get_current_user
from auth.models import User
from shipments.models import Shipment
from documents.models import Document, ExtractionJob
from documents.schemas import (
    DocumentResponse, 
    ExtractionResponse, 
    AutoFillRequest, 
    AutoFillResponse,
    DocumentType
)
from documents.extractor import document_extractor
from utils.storage import upload_to_supabase

router = APIRouter()

@router.post("/shipments/{shipment_id}/upload", response_model=DocumentResponse)
async def upload_document(
    shipment_id: str,
    file: UploadFile = File(...),
    document_type: DocumentType = DocumentType.INVOICE,
    background_tasks: BackgroundTasks = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload a document for a shipment
    """
    # Verify shipment exists and user has access
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
            detail="Not authorized to upload documents for this shipment"
        )
    
    # Validate file type
    allowed_types = ["application/pdf", "image/jpeg", "image/png", "image/jpg"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type {file.content_type} not allowed. Use PDF or images."
        )
    
    # Save file temporarily
    temp_dir = tempfile.gettempdir()
    temp_filename = f"{uuid.uuid4()}_{file.filename}"
    temp_path = os.path.join(temp_dir, temp_filename)
    
    try:
        # Write uploaded file to temp location
        with open(temp_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Upload to Supabase Storage
        storage_path = f"shipments/{shipment_id}/documents/{temp_filename}"
        file_url = upload_to_supabase(temp_path, storage_path, file.content_type)
        
        # Create document record
        document = Document(
            shipment_id=shipment_id,
            uploaded_by=current_user.id,
            type=document_type.value,
            file_name=file.filename,
            file_url=file_url,
            file_size=len(content),
            mime_type=file.content_type
        )
        
        db.add(document)
        db.commit()
        db.refresh(document)
        
        # Trigger AI extraction in background
        if background_tasks:
            background_tasks.add_task(
                extract_document_data,
                str(document.id),
                temp_path,
                db
            )
        
        return document
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload document: {str(e)}"
        )
    finally:
        # Clean up temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)

@router.get("/shipments/{shipment_id}/documents", response_model=List[DocumentResponse])
async def get_shipment_documents(
    shipment_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all documents for a shipment
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
            detail="Not authorized"
        )
    
    if current_user.role == "buyer" and str(shipment.buyer_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    documents = db.query(Document).filter(
        Document.shipment_id == shipment_id
    ).all()
    
    return documents

@router.get("/documents/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific document
    """
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    # Check permissions via shipment
    shipment = db.query(Shipment).filter(Shipment.id == document.shipment_id).first()
    if current_user.role == "supplier" and str(shipment.supplier_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    return document

@router.post("/documents/{document_id}/extract", response_model=ExtractionResponse)
async def trigger_extraction(
    document_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Manually trigger AI extraction for a document
    """
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    # Check permissions
    shipment = db.query(Shipment).filter(Shipment.id == document.shipment_id).first()
    if current_user.role == "supplier" and str(shipment.supplier_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    # Download file from storage (simplified - in production use signed URLs)
    # For now, assume we have the file path
    try:
        # This would need to download from Supabase in production
        # For now, return mock extraction
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Extraction from stored files not yet implemented. Upload new document to trigger extraction."
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Extraction failed: {str(e)}"
        )

@router.post("/documents/{document_id}/autofill", response_model=AutoFillResponse)
async def autofill_shipment(
    document_id: str,
    autofill_request: AutoFillRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Auto-fill shipment fields from extracted document data
    """
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    if not document.extracted_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Document has not been extracted yet"
        )
    
    # Get shipment
    shipment = db.query(Shipment).filter(Shipment.id == document.shipment_id).first()
    
    # Check permissions
    if current_user.role == "supplier" and str(shipment.supplier_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    # Auto-fill requested fields
    updated_fields = []
    extracted_values = {}
    
    for field in autofill_request.fields:
        if field in document.extracted_data:
            value = document.extracted_data[field]
            if value:
                setattr(shipment, field, value)
                updated_fields.append(field)
                extracted_values[field] = value
    
    db.commit()
    
    return AutoFillResponse(
        document_id=str(document.id),
        shipment_id=str(shipment.id),
        updated_fields=updated_fields,
        confidence=document.confidence_score,
        extracted_values=extracted_values
    )

async def extract_document_data(document_id: str, file_path: str, db: Session):
    """
    Background task to extract data from document using AI
    """
    try:
        # Get document
        document = db.query(Document).filter(Document.id == document_id).first()
        if not document:
            return
        
        # Create extraction job
        job = ExtractionJob(
            document_id=document_id,
            status="processing"
        )
        db.add(job)
        db.commit()
        
        # Run AI extraction
        import asyncio
        extracted_data = await document_extractor.extract_document(file_path)
        
        # Update document with extracted data
        document.extracted_data = extracted_data
        document.confidence_score = extracted_data.get("confidence", 0.0)
        document.extraction_method = extracted_data.get("extraction_method", "unknown")
        document.needs_review = extracted_data.get("needs_review", True)
        
        # Update job
        job.status = "completed"
        job.model_used = extracted_data.get("extraction_method", "gemini_1.5_pro")
        job.processing_time_ms = extracted_data.get("processing_time_ms", 0)
        
        db.commit()
        
    except Exception as e:
        # Update job with error
        job = db.query(ExtractionJob).filter(ExtractionJob.document_id == document_id).first()
        if job:
            job.status = "failed"
            job.error_message = str(e)
            job.attempts += 1
            db.commit()
        
        print(f"Extraction failed for document {document_id}: {e}")
