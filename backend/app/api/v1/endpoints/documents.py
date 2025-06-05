# Document management endpoints
import os
import shutil
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query, Form
from sqlalchemy.orm import Session
from sqlalchemy import or_, func, desc
from database import get_db
from models.database_models import User, Document, Tag, ActivityLog, document_tags
from dependencies import get_current_user, get_admin_user
from config import settings
import schemas
from datetime import datetime
import uuid

router = APIRouter()

@router.get("/", response_model=schemas.PaginatedResponse)
def get_documents(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    status: Optional[str] = None,
    file_type: Optional[str] = None,
    tag_ids: Optional[List[int]] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get paginated list of documents."""
    query = db.query(Document)
    
    # Non-admin users can only see their own documents
    if current_user.role != "admin":
        query = query.filter(Document.uploaded_by == current_user.id)
    
    # Apply filters
    if search:
        query = query.filter(
            or_(
                Document.filename.contains(search),
                Document.title.contains(search),
                Document.description.contains(search)
            )
        )
    
    if status:
        query = query.filter(Document.status == status)
    
    if file_type:
        query = query.filter(Document.file_type == file_type)
    
    if tag_ids:
        query = query.join(document_tags).filter(document_tags.c.tag_id.in_(tag_ids))
    
    # Count total
    total = query.count()
    
    # Apply pagination and ordering
    documents = query.order_by(desc(Document.created_at)).offset((page - 1) * per_page).limit(per_page).all()
    
    return {
        "items": documents,
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": (total + per_page - 1) // per_page
    }

@router.get("/{document_id}", response_model=schemas.Document)
def get_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get document by ID."""
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Check permissions
    if current_user.role != "admin" and document.uploaded_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return document

@router.post("/upload", response_model=schemas.Document)
async def upload_document(
    file: UploadFile = File(...),
    title: str = Form(...),
    description: Optional[str] = Form(None),
    tag_ids: Optional[List[int]] = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload a new document."""
    # Validate file type
    file_extension = file.filename.split('.')[-1].lower()
    if file_extension not in settings.ALLOWED_FILE_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed types: {', '.join(settings.ALLOWED_FILE_TYPES)}"
        )
    
    # Validate file size
    file.file.seek(0, 2)  # Move to end of file
    file_size = file.file.tell()
    file.file.seek(0)  # Reset to beginning
    
    if file_size > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {settings.MAX_FILE_SIZE // (1024*1024)}MB"
        )
    
    # Create unique filename
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
    
    # Ensure upload directory exists
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    # Save file
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    
    # Create document record
    document = Document(
        filename=file.filename,
        title=title,
        description=description,
        file_type=file_extension,
        file_size=file_size,
        file_path=file_path,
        uploaded_by=current_user.id,
        status="uploaded"
    )
    
    db.add(document)
    db.commit()
    db.refresh(document)
    
    # Add tags if provided
    if tag_ids:
        tags = db.query(Tag).filter(Tag.id.in_(tag_ids)).all()
        document.tags.extend(tags)
        db.commit()
    
    # Log activity
    activity_log = ActivityLog(
        user_id=current_user.id,
        activity_type="upload_document",
        description=f"Uploaded document: {title}",
        metadata={"document_id": document.id, "filename": file.filename}
    )
    db.add(activity_log)
    db.commit()
    
    return document

@router.put("/{document_id}", response_model=schemas.Document)
def update_document(
    document_id: int,
    document_update: schemas.DocumentUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update document metadata."""
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Check permissions
    if current_user.role != "admin" and document.uploaded_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    update_data = document_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(document, field, value)
    
    db.add(document)
    db.commit()
    db.refresh(document)
    
    # Log activity
    activity_log = ActivityLog(
        user_id=current_user.id,
        activity_type="update_document",
        description=f"Updated document: {document.title}",
        metadata={"document_id": document.id, "changes": update_data}
    )
    db.add(activity_log)
    db.commit()
    
    return document

@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete document."""
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Check permissions
    if current_user.role != "admin" and document.uploaded_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    title = document.title
    file_path = document.file_path
    
    # Delete database record
    db.delete(document)
    db.commit()
    
    # Delete physical file
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f"Warning: Could not delete file {file_path}: {str(e)}")
    
    # Log activity
    activity_log = ActivityLog(
        user_id=current_user.id,
        activity_type="delete_document",
        description=f"Deleted document: {title}",
        metadata={"document_id": document_id, "filename": document.filename}
    )
    db.add(activity_log)
    db.commit()
    
    return {"message": "Document deleted successfully"}

@router.post("/bulk-delete")
def bulk_delete_documents(
    document_ids: List[int],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Bulk delete documents."""
    query = db.query(Document).filter(Document.id.in_(document_ids))
    
    # Non-admin users can only delete their own documents
    if current_user.role != "admin":  
        query = query.filter(Document.uploaded_by == current_user.id)
    
    documents = query.all()
    
    if not documents:
        raise HTTPException(status_code=404, detail="No documents found or permission denied")
    
    deleted_count = 0
    for document in documents:
        # Delete physical file
        try:
            if os.path.exists(document.file_path):
                os.remove(document.file_path)
        except Exception as e:
            print(f"Warning: Could not delete file {document.file_path}: {str(e)}")
        
        db.delete(document)
        deleted_count += 1
    
    db.commit()
    
    # Log activity
    activity_log = ActivityLog(
        user_id=current_user.id,
        activity_type="bulk_delete_documents",
        description=f"Bulk deleted {deleted_count} documents",
        metadata={"document_ids": document_ids, "deleted_count": deleted_count}
    )
    db.add(activity_log)
    db.commit()
    
    return {"message": f"Successfully deleted {deleted_count} documents"}

@router.get("/stats/overview")
def get_document_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get document statistics."""
    query = db.query(Document)
    
    # Non-admin users can only see their own stats
    if current_user.role != "admin":
        query = query.filter(Document.uploaded_by == current_user.id)
    
    total_documents = query.count()
    
    # Status distribution
    status_stats = query.group_by(Document.status).all()
    status_distribution = {}
    for status in ["uploaded", "processing", "processed", "error"]:
        count = query.filter(Document.status == status).count()
        status_distribution[status] = count
    
    # File type distribution
    file_type_stats = db.query(
        Document.file_type,
        func.count(Document.id).label('count')
    )
    
    if current_user.role != "admin":
        file_type_stats = file_type_stats.filter(Document.uploaded_by == current_user.id)
    
    file_type_stats = file_type_stats.group_by(Document.file_type).all()
    file_type_distribution = {file_type: count for file_type, count in file_type_stats}
    
    # Total storage used
    total_size = query.with_entities(func.sum(Document.file_size)).scalar() or 0
    
    return {
        "total_documents": total_documents,
        "status_distribution": status_distribution,
        "file_type_distribution": file_type_distribution,
        "total_storage_bytes": total_size,
        "total_storage_mb": round(total_size / (1024 * 1024), 2)
    }
