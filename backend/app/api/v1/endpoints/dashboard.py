# Dashboard statistics endpoints
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_
from database import get_db
from models.database_models import (
    User, Document, Template, ChatSession, ChatMessage, 
    TokenUsage, TemplateGeneration, ActivityLog
)
from dependencies import get_current_user, get_admin_user
import schemas

router = APIRouter()

@router.get("/overview")
def get_dashboard_overview(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get dashboard overview statistics."""
    
    if current_user.role == "admin":
        # Admin sees system-wide statistics
        total_users = db.query(User).count()
        active_users = db.query(User).filter(User.is_active == True).count()
        total_documents = db.query(Document).count()
        total_templates = db.query(Template).count()
        total_chat_sessions = db.query(ChatSession).count()
        
        # Recent activity (last 7 days)
        week_ago = datetime.utcnow() - timedelta(days=7)
        recent_documents = db.query(Document).filter(Document.created_at >= week_ago).count()
        recent_templates = db.query(Template).filter(Template.created_at >= week_ago).count()
        recent_chats = db.query(ChatSession).filter(ChatSession.created_at >= week_ago).count()
        
        # Token usage this month
        month_ago = datetime.utcnow() - timedelta(days=30)
        monthly_tokens = db.query(TokenUsage).filter(
            TokenUsage.created_at >= month_ago
        ).with_entities(func.sum(TokenUsage.total_tokens)).scalar() or 0
        
        monthly_cost = db.query(TokenUsage).filter(
            TokenUsage.created_at >= month_ago
        ).with_entities(func.sum(TokenUsage.cost)).scalar() or 0.0
        
        return {
            "user_stats": {
                "total_users": total_users,
                "active_users": active_users,
                "inactive_users": total_users - active_users
            },
            "content_stats": {
                "total_documents": total_documents,
                "total_templates": total_templates,
                "total_chat_sessions": total_chat_sessions,
                "recent_documents": recent_documents,
                "recent_templates": recent_templates,
                "recent_chats": recent_chats
            },
            "usage_stats": {
                "monthly_tokens": monthly_tokens,
                "monthly_cost": float(monthly_cost)
            }
        }
    else:
        # Regular users see their own statistics
        user_documents = db.query(Document).filter(Document.uploaded_by == current_user.id).count()
        user_templates = db.query(Template).filter(Template.created_by == current_user.id).count()
        user_chat_sessions = db.query(ChatSession).filter(ChatSession.user_id == current_user.id).count()
        
        # User's token usage this month
        month_ago = datetime.utcnow() - timedelta(days=30)
        user_monthly_tokens = db.query(TokenUsage).filter(
            and_(
                TokenUsage.user_id == current_user.id,
                TokenUsage.created_at >= month_ago
            )
        ).with_entities(func.sum(TokenUsage.total_tokens)).scalar() or 0
        
        user_monthly_cost = db.query(TokenUsage).filter(
            and_(
                TokenUsage.user_id == current_user.id,
                TokenUsage.created_at >= month_ago
            )
        ).with_entities(func.sum(TokenUsage.cost)).scalar() or 0.0
        
        return {
            "content_stats": {
                "my_documents": user_documents,
                "my_templates": user_templates,
                "my_chat_sessions": user_chat_sessions
            },
            "usage_stats": {
                "monthly_tokens": user_monthly_tokens,
                "monthly_cost": float(user_monthly_cost)
            }
        }

@router.get("/recent-activity")
def get_recent_activity(
    limit: int = Query(10, ge=1, le=50),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get recent activity logs."""
    
    query = db.query(ActivityLog)
    
    # Non-admin users see only their own activity
    if current_user.role != "admin":
        query = query.filter(ActivityLog.user_id == current_user.id)
    
    activities = query.order_by(desc(ActivityLog.created_at)).limit(limit).all()
    
    return {
        "activities": activities
    }

@router.get("/ai-service-status")
def get_ai_service_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get AI service status and availability."""
    
    # Check recent token usage to determine service health
    hour_ago = datetime.utcnow() - timedelta(hours=1)
    recent_usage = db.query(TokenUsage).filter(TokenUsage.created_at >= hour_ago).count()
    
    # Get model usage distribution
    model_stats = db.query(
        TokenUsage.model_name,
        func.count(TokenUsage.id).label('usage_count')
    ).filter(
        TokenUsage.created_at >= datetime.utcnow() - timedelta(days=7)
    ).group_by(TokenUsage.model_name).all()
    
    # Mock service status (in real implementation, you'd check actual service health)
    services = [
        {
            "name": "Azure OpenAI",
            "status": "operational",
            "models": ["gpt-4", "gpt-3.5-turbo"],
            "latency": "120ms",
            "uptime": "99.9%"
        },
        {
            "name": "Ollama",
            "status": "operational",
            "models": ["llama2", "mistral", "codellama"],
            "latency": "80ms",
            "uptime": "99.5%"
        }
    ]
    
    return {
        "services": services,
        "recent_usage_count": recent_usage,
        "model_usage": [{"model": model, "count": count} for model, count in model_stats]
    }

@router.get("/quick-actions")
def get_quick_actions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get suggested quick actions based on user role and recent activity."""
    
    actions = []
    
    if current_user.role == "admin":
        # Admin actions
        actions.extend([
            {
                "title": "User Management",
                "description": "Manage user accounts and permissions",
                "icon": "users",
                "route": "/admin/users",
                "color": "blue"
            },
            {
                "title": "System Overview",
                "description": "View system statistics and health",
                "icon": "chart-bar",
                "route": "/admin/dashboard",
                "color": "green"
            },
            {
                "title": "Document Processing",
                "description": "Monitor document processing queue",
                "icon": "document-text",
                "route": "/admin/documents",
                "color": "yellow"
            }
        ])
    
    if current_user.role in ["admin", "instructor"]:
        # Instructor and admin actions
        actions.extend([
            {
                "title": "Create Template",
                "description": "Create new curriculum template",
                "icon": "plus-circle",
                "route": "/templates/create",
                "color": "purple"
            },
            {
                "title": "Template Management",
                "description": "Manage existing templates",
                "icon": "collection",
                "route": "/admin/templates",
                "color": "indigo"
            }
        ])
    
    # Common actions for all users
    actions.extend([
        {
            "title": "Upload Document",
            "description": "Upload new curriculum document",
            "icon": "cloud-upload",
            "route": "/documents/upload",
            "color": "blue"
        },
        {
            "title": "Start Chat",
            "description": "Begin new AI conversation",
            "icon": "chat",
            "route": "/chat",
            "color": "green"
        },
        {
            "title": "Generate Content",
            "description": "Create curriculum content from templates",
            "icon": "academic-cap",
            "route": "/template-generation",
            "color": "red"
        }
    ])
    
    return {
        "actions": actions
    }

@router.get("/system-health")
def get_system_health(
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Get system health metrics (admin only)."""
    
    # Database health
    try:
        db.execute("SELECT 1")
        database_status = "healthy"
    except Exception:
        database_status = "error"
    
    # Recent error rates
    day_ago = datetime.utcnow() - timedelta(days=1)
    
    # Check for failed template generations
    total_generations = db.query(TemplateGeneration).filter(
        TemplateGeneration.created_at >= day_ago
    ).count()
    
    failed_generations = db.query(TemplateGeneration).filter(
        and_(
            TemplateGeneration.created_at >= day_ago,
            TemplateGeneration.status == "failed"
        )
    ).count()
    
    error_rate = (failed_generations / total_generations * 100) if total_generations > 0 else 0
    
    # Storage usage (mock data - in real implementation, check actual disk usage)
    storage_info = {
        "total_gb": 100,
        "used_gb": 45,
        "available_gb": 55,
        "usage_percent": 45
    }
    
    return {
        "database_status": database_status,
        "error_rate_24h": round(error_rate, 2),
        "storage": storage_info,
        "timestamp": datetime.utcnow().isoformat()
    }
