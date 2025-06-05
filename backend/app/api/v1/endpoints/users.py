# User management endpoints
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from database import get_db
from models.database_models import User, ActivityLog
from dependencies import get_current_user, get_admin_user
from auth import get_password_hash
import schemas

router = APIRouter()

@router.get("/", response_model=schemas.PaginatedResponse)
def get_users(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    role: Optional[str] = None,
    is_active: Optional[bool] = None,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Get paginated list of users (admin only)."""
    query = db.query(User)
    
    # Apply filters
    if search:
        query = query.filter(
            or_(
                User.username.contains(search),
                User.email.contains(search),
                User.full_name.contains(search)
            )
        )
    
    if role:
        query = query.filter(User.role == role)
    
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    
    # Count total
    total = query.count()
    
    # Apply pagination
    users = query.offset((page - 1) * per_page).limit(per_page).all()
    
    return {
        "items": users,
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": (total + per_page - 1) // per_page
    }

@router.get("/{user_id}", response_model=schemas.User)
def get_user(
    user_id: int,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Get user by ID (admin only)."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

@router.post("/", response_model=schemas.User)
def create_user(
    user: schemas.UserCreate,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Create a new user (admin only)."""
    # Check if user already exists
    existing_user = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User with this username or email already exists"
        )
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        role=user.role,
        hashed_password=hashed_password
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Log activity
    activity_log = ActivityLog(
        user_id=current_user.id,
        activity_type="create_user",
        description=f"Admin {current_user.username} created user {user.username}",
        metadata={"created_user_id": db_user.id}
    )
    db.add(activity_log)
    db.commit()
    
    return db_user

@router.put("/{user_id}", response_model=schemas.User)
def update_user(
    user_id: int,
    user_update: schemas.UserUpdate,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Update user (admin only)."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = user_update.dict(exclude_unset=True)
    
    # Check for username/email conflicts
    if "username" in update_data or "email" in update_data:
        conflict_query = db.query(User).filter(User.id != user_id)
        if "username" in update_data:
            conflict_query = conflict_query.filter(User.username == update_data["username"])
        if "email" in update_data:
            conflict_query = conflict_query.filter(User.email == update_data["email"])
        
        if conflict_query.first():
            raise HTTPException(
                status_code=400,
                detail="User with this username or email already exists"
            )
    
    for field, value in update_data.items():
        setattr(user, field, value)
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Log activity
    activity_log = ActivityLog(
        user_id=current_user.id,
        activity_type="update_user",
        description=f"Admin {current_user.username} updated user {user.username}",
        metadata={"updated_user_id": user.id, "changes": update_data}
    )
    db.add(activity_log)
    db.commit()
    
    return user

@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Delete user (admin only)."""
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot delete yourself")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    username = user.username
    
    # Soft delete by deactivating
    user.is_active = False
    db.add(user)
    db.commit()
    
    # Log activity
    activity_log = ActivityLog(
        user_id=current_user.id,
        activity_type="delete_user",
        description=f"Admin {current_user.username} deactivated user {username}",
        metadata={"deactivated_user_id": user_id}
    )
    db.add(activity_log)
    db.commit()
    
    return {"message": "User deactivated successfully"}

@router.put("/{user_id}/activate")
def activate_user(
    user_id: int,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Activate user (admin only)."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_active = True
    db.add(user)
    db.commit()
    
    # Log activity
    activity_log = ActivityLog(
        user_id=current_user.id,
        activity_type="activate_user",
        description=f"Admin {current_user.username} activated user {user.username}",
        metadata={"activated_user_id": user_id}
    )
    db.add(activity_log)
    db.commit()
    
    return {"message": "User activated successfully"}

@router.get("/stats/overview")
def get_user_stats(
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Get user statistics overview (admin only)."""
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()
    inactive_users = total_users - active_users
    
    # Role distribution
    role_stats = db.query(
        User.role,
        func.count(User.id).label('count')
    ).group_by(User.role).all()
    
    role_distribution = {role: count for role, count in role_stats}
    
    return {
        "total_users": total_users,
        "active_users": active_users,
        "inactive_users": inactive_users,
        "role_distribution": role_distribution
    }
