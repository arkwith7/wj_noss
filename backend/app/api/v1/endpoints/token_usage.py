# Token usage management endpoints
from typing import List, Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_
from database import get_db
from models.database_models import User, TokenUsage, ChatSession
from dependencies import get_current_user, get_admin_user
import schemas

router = APIRouter()

@router.get("/", response_model=schemas.PaginatedResponse)
def get_token_usage(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    user_id: Optional[int] = None,
    model_name: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get paginated list of token usage records."""
    query = db.query(TokenUsage)
    
    # Non-admin users can only see their own usage
    if current_user.role != "admin":
        query = query.filter(TokenUsage.user_id == current_user.id)
    elif user_id:
        query = query.filter(TokenUsage.user_id == user_id)
    
    # Apply filters
    if model_name:
        query = query.filter(TokenUsage.model_name == model_name)
    
    if start_date:
        query = query.filter(TokenUsage.created_at >= start_date)
    
    if end_date:
        query = query.filter(TokenUsage.created_at <= end_date)
    
    # Count total
    total = query.count()
    
    # Apply pagination and ordering
    usage_records = query.order_by(desc(TokenUsage.created_at)).offset((page - 1) * per_page).limit(per_page).all()
    
    return {
        "items": usage_records,
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": (total + per_page - 1) // per_page
    }

@router.post("/", response_model=schemas.TokenUsage)
def create_token_usage(
    usage: schemas.TokenUsageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Record token usage."""
    # Verify user permissions
    if current_user.role != "admin" and usage.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Verify session exists and belongs to user if session_id provided
    if usage.session_id:
        session = db.query(ChatSession).filter(ChatSession.id == usage.session_id).first()
        if not session:
            raise HTTPException(status_code=404, detail="Chat session not found")
        
        if current_user.role != "admin" and session.user_id != usage.user_id:
            raise HTTPException(status_code=403, detail="Session does not belong to user")
    
    db_usage = TokenUsage(
        user_id=usage.user_id,
        session_id=usage.session_id,
        model_name=usage.model_name,
        prompt_tokens=usage.prompt_tokens,
        completion_tokens=usage.completion_tokens,
        total_tokens=usage.total_tokens,
        cost=usage.cost
    )
    
    db.add(db_usage)
    db.commit()
    db.refresh(db_usage)
    
    return db_usage

@router.get("/stats/overview")
def get_token_usage_stats(
    user_id: Optional[int] = None,
    days: int = Query(30, ge=1, le=365),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get token usage statistics."""
    query = db.query(TokenUsage)
    
    # Non-admin users can only see their own stats
    if current_user.role != "admin":
        query = query.filter(TokenUsage.user_id == current_user.id)
    elif user_id:
        query = query.filter(TokenUsage.user_id == user_id)
    
    # Filter by date range
    start_date = datetime.utcnow() - timedelta(days=days)
    query = query.filter(TokenUsage.created_at >= start_date)
    
    # Total tokens
    total_tokens = query.with_entities(func.sum(TokenUsage.total_tokens)).scalar() or 0
    total_prompt_tokens = query.with_entities(func.sum(TokenUsage.prompt_tokens)).scalar() or 0
    total_completion_tokens = query.with_entities(func.sum(TokenUsage.completion_tokens)).scalar() or 0
    total_cost = query.with_entities(func.sum(TokenUsage.cost)).scalar() or 0.0
    
    # Model breakdown
    model_stats = query.group_by(TokenUsage.model_name).with_entities(
        TokenUsage.model_name,
        func.sum(TokenUsage.total_tokens).label('total_tokens'),
        func.sum(TokenUsage.cost).label('total_cost'),
        func.count(TokenUsage.id).label('usage_count')
    ).all()
    
    model_breakdown = [
        {
            "model_name": model,
            "total_tokens": tokens,
            "total_cost": float(cost) if cost else 0.0,
            "usage_count": count
        }
        for model, tokens, cost, count in model_stats
    ]
    
    # Daily usage for chart
    daily_stats = db.query(
        func.date(TokenUsage.created_at).label('date'),
        func.sum(TokenUsage.total_tokens).label('total_tokens'),
        func.sum(TokenUsage.cost).label('total_cost')
    ).filter(
        TokenUsage.created_at >= start_date
    )
    
    if current_user.role != "admin":
        daily_stats = daily_stats.filter(TokenUsage.user_id == current_user.id)
    elif user_id:
        daily_stats = daily_stats.filter(TokenUsage.user_id == user_id)
    
    daily_stats = daily_stats.group_by(func.date(TokenUsage.created_at)).all()
    
    daily_usage = [
        {
            "date": date.isoformat(),
            "total_tokens": tokens,
            "total_cost": float(cost) if cost else 0.0
        }
        for date, tokens, cost in daily_stats
    ]
    
    return {
        "period_days": days,
        "total_tokens": total_tokens,
        "total_prompt_tokens": total_prompt_tokens,
        "total_completion_tokens": total_completion_tokens,
        "total_cost": float(total_cost),
        "model_breakdown": model_breakdown,
        "daily_usage": daily_usage
    }

@router.get("/stats/users")
def get_user_token_stats(
    days: int = Query(30, ge=1, le=365),
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Get token usage statistics by user (admin only)."""
    start_date = datetime.utcnow() - timedelta(days=days)
    
    user_stats = db.query(
        User.id,
        User.username,
        User.full_name,
        func.sum(TokenUsage.total_tokens).label('total_tokens'),
        func.sum(TokenUsage.cost).label('total_cost'),
        func.count(TokenUsage.id).label('usage_count')
    ).join(
        TokenUsage, User.id == TokenUsage.user_id
    ).filter(
        TokenUsage.created_at >= start_date
    ).group_by(
        User.id, User.username, User.full_name
    ).all()
    
    user_breakdown = [
        {
            "user_id": user_id,
            "username": username,
            "full_name": full_name,
            "total_tokens": tokens or 0,
            "total_cost": float(cost) if cost else 0.0,
            "usage_count": count or 0
        }
        for user_id, username, full_name, tokens, cost, count in user_stats
    ]
    
    return {
        "period_days": days,
        "user_breakdown": user_breakdown
    }

@router.get("/realtime")
def get_realtime_usage(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get real-time token usage for current session."""
    # Get usage for last hour
    one_hour_ago = datetime.utcnow() - timedelta(hours=1)
    
    query = db.query(TokenUsage).filter(TokenUsage.created_at >= one_hour_ago)
    
    # Non-admin users see only their own usage
    if current_user.role != "admin":
        query = query.filter(TokenUsage.user_id == current_user.id)
    
    recent_usage = query.order_by(desc(TokenUsage.created_at)).limit(10).all()
    
    # Calculate totals
    total_tokens_hour = query.with_entities(func.sum(TokenUsage.total_tokens)).scalar() or 0
    total_cost_hour = query.with_entities(func.sum(TokenUsage.cost)).scalar() or 0.0
    
    return {
        "recent_usage": recent_usage,
        "last_hour_tokens": total_tokens_hour,
        "last_hour_cost": float(total_cost_hour),
        "timestamp": datetime.utcnow().isoformat()
    }
