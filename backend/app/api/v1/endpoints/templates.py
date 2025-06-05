# Template management endpoints
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, func, desc
from database import get_db
from models.database_models import User, Template, ActivityLog
from dependencies import get_current_user, get_instructor_or_admin_user
import schemas

router = APIRouter()

@router.get("/", response_model=schemas.PaginatedResponse)
def get_templates(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    template_type: Optional[str] = None,
    is_active: Optional[bool] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get paginated list of templates."""
    query = db.query(Template)
    
    # Apply filters
    if search:
        query = query.filter(
            or_(
                Template.name.contains(search),
                Template.description.contains(search)
            )
        )
    
    if template_type:
        query = query.filter(Template.template_type == template_type)
    
    if is_active is not None:
        query = query.filter(Template.is_active == is_active)
    
    # Count total
    total = query.count()
    
    # Apply pagination and ordering
    templates = query.order_by(desc(Template.created_at)).offset((page - 1) * per_page).limit(per_page).all()
    
    return {
        "items": templates,
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": (total + per_page - 1) // per_page
    }

@router.get("/{template_id}", response_model=schemas.Template)
def get_template(
    template_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get template by ID."""
    template = db.query(Template).filter(Template.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    return template

@router.post("/", response_model=schemas.Template)
def create_template(
    template: schemas.TemplateCreate,
    current_user: User = Depends(get_instructor_or_admin_user),
    db: Session = Depends(get_db)
):
    """Create a new template."""
    # Check if template name already exists
    existing_template = db.query(Template).filter(Template.name == template.name).first()
    if existing_template:
        raise HTTPException(
            status_code=400,
            detail="Template with this name already exists"
        )
    
    db_template = Template(
        name=template.name,
        description=template.description,
        template_type=template.template_type,
        content_template=template.content_template,
        is_active=template.is_active,
        created_by=current_user.id
    )
    
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    
    # Log activity
    activity_log = ActivityLog(
        user_id=current_user.id,
        activity_type="create_template",
        description=f"Created template: {template.name}",
        metadata={"template_id": db_template.id, "template_type": template.template_type}
    )
    db.add(activity_log)
    db.commit()
    
    return db_template

@router.put("/{template_id}", response_model=schemas.Template)
def update_template(
    template_id: int,
    template_update: schemas.TemplateUpdate,
    current_user: User = Depends(get_instructor_or_admin_user),
    db: Session = Depends(get_db)
):
    """Update template."""
    template = db.query(Template).filter(Template.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    # Check permissions (only creator or admin can update)
    if current_user.role != "admin" and template.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    update_data = template_update.dict(exclude_unset=True)
    
    # Check for name conflicts
    if "name" in update_data:
        existing_template = db.query(Template).filter(
            Template.name == update_data["name"],
            Template.id != template_id
        ).first()
        if existing_template:
            raise HTTPException(
                status_code=400,
                detail="Template with this name already exists"
            )
    
    for field, value in update_data.items():
        setattr(template, field, value)
    
    db.add(template)
    db.commit()
    db.refresh(template)
    
    # Log activity
    activity_log = ActivityLog(
        user_id=current_user.id,
        activity_type="update_template",
        description=f"Updated template: {template.name}",
        metadata={"template_id": template.id, "changes": update_data}
    )
    db.add(activity_log)
    db.commit()
    
    return template

@router.delete("/{template_id}")
def delete_template(
    template_id: int,
    current_user: User = Depends(get_instructor_or_admin_user),
    db: Session = Depends(get_db)
):
    """Delete template."""
    template = db.query(Template).filter(Template.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    # Check permissions (only creator or admin can delete)
    if current_user.role != "admin" and template.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    name = template.name
    
    # Soft delete by deactivating instead of hard delete
    template.is_active = False
    db.add(template)
    db.commit()
    
    # Log activity
    activity_log = ActivityLog(
        user_id=current_user.id,
        activity_type="delete_template",
        description=f"Deactivated template: {name}",
        metadata={"template_id": template_id}
    )
    db.add(activity_log)
    db.commit()
    
    return {"message": "Template deactivated successfully"}

@router.post("/{template_id}/activate")
def activate_template(
    template_id: int,
    current_user: User = Depends(get_instructor_or_admin_user),
    db: Session = Depends(get_db)
):
    """Activate template."""
    template = db.query(Template).filter(Template.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    # Check permissions
    if current_user.role != "admin" and template.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    template.is_active = True
    db.add(template)
    db.commit()
    
    # Log activity
    activity_log = ActivityLog(
        user_id=current_user.id,
        activity_type="activate_template",
        description=f"Activated template: {template.name}",
        metadata={"template_id": template_id}
    )
    db.add(activity_log)
    db.commit()
    
    return {"message": "Template activated successfully"}

@router.post("/bulk-delete")
def bulk_delete_templates(
    template_ids: List[int],
    current_user: User = Depends(get_instructor_or_admin_user),
    db: Session = Depends(get_db)
):
    """Bulk delete (deactivate) templates."""
    query = db.query(Template).filter(Template.id.in_(template_ids))
    
    # Non-admin users can only delete their own templates
    if current_user.role != "admin":
        query = query.filter(Template.created_by == current_user.id)
    
    templates = query.all()
    
    if not templates:
        raise HTTPException(status_code=404, detail="No templates found or permission denied")
    
    deactivated_count = 0
    for template in templates:
        template.is_active = False
        db.add(template)
        deactivated_count += 1
    
    db.commit()
    
    # Log activity
    activity_log = ActivityLog(
        user_id=current_user.id,
        activity_type="bulk_delete_templates",
        description=f"Bulk deactivated {deactivated_count} templates",
        metadata={"template_ids": template_ids, "deactivated_count": deactivated_count}
    )
    db.add(activity_log)
    db.commit()
    
    return {"message": f"Successfully deactivated {deactivated_count} templates"}

@router.get("/stats/overview")
def get_template_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get template statistics."""
    query = db.query(Template)
    
    total_templates = query.count()
    active_templates = query.filter(Template.is_active == True).count()
    inactive_templates = total_templates - active_templates
    
    # Type distribution
    type_stats = db.query(
        Template.template_type,
        func.count(Template.id).label('count')
    ).group_by(Template.template_type).all()
    
    type_distribution = {template_type: count for template_type, count in type_stats}
    
    # Creator distribution (for admins)
    creator_stats = {}
    if current_user.role == "admin":
        creator_stats_query = db.query(
            User.username,
            func.count(Template.id).label('count')
        ).join(Template, User.id == Template.created_by).group_by(User.username).all()
        
        creator_stats = {username: count for username, count in creator_stats_query}
    
    return {
        "total_templates": total_templates,
        "active_templates": active_templates,
        "inactive_templates": inactive_templates,
        "type_distribution": type_distribution,
        "creator_distribution": creator_stats
    }

@router.get("/types/list")
def get_template_types(current_user: User = Depends(get_current_user)):
    """Get list of available template types."""
    return {
        "template_types": [
            {"value": "course", "label": "Course"},
            {"value": "unit", "label": "Unit"},
            {"value": "lesson", "label": "Lesson"},
            {"value": "assessment", "label": "Assessment"}
        ]
    }
