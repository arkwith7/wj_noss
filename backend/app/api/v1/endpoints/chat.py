# Chat management endpoints
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, func, desc
from database import get_db
from models.database_models import User, ChatSession, ChatMessage, TokenUsage, ActivityLog
from dependencies import get_current_user, get_admin_user
import schemas

router = APIRouter()

# Chat Sessions
@router.get("/sessions", response_model=schemas.PaginatedResponse)
def get_chat_sessions(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    model_name: Optional[str] = None,
    is_active: Optional[bool] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get paginated list of chat sessions."""
    query = db.query(ChatSession)
    
    # Non-admin users can only see their own sessions
    if current_user.role != "admin":
        query = query.filter(ChatSession.user_id == current_user.id)
    
    # Apply filters
    if search:
        query = query.filter(ChatSession.title.contains(search))
    
    if model_name:
        query = query.filter(ChatSession.model_name == model_name)
    
    if is_active is not None:
        query = query.filter(ChatSession.is_active == is_active)
    
    # Count total
    total = query.count()
    
    # Apply pagination and ordering
    sessions = query.order_by(desc(ChatSession.updated_at)).offset((page - 1) * per_page).limit(per_page).all()
    
    return {
        "items": sessions,
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": (total + per_page - 1) // per_page
    }

@router.get("/sessions/{session_id}", response_model=schemas.ChatSession)
def get_chat_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get chat session by ID."""
    session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    
    # Check permissions
    if current_user.role != "admin" and session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return session

@router.post("/sessions", response_model=schemas.ChatSession)
def create_chat_session(
    session: schemas.ChatSessionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new chat session."""
    db_session = ChatSession(
        title=session.title,
        model_name=session.model_name,
        user_id=current_user.id
    )
    
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    
    # Log activity
    activity_log = ActivityLog(
        user_id=current_user.id,
        activity_type="create_chat",
        description=f"Created chat session: {session.title}",
        metadata={"session_id": db_session.id, "model_name": session.model_name}
    )
    db.add(activity_log)
    db.commit()
    
    return db_session

@router.put("/sessions/{session_id}", response_model=schemas.ChatSession)
def update_chat_session(
    session_id: int,
    session_update: schemas.ChatSessionUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update chat session."""
    session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    
    # Check permissions
    if current_user.role != "admin" and session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    update_data = session_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(session, field, value)
    
    db.add(session)
    db.commit()
    db.refresh(session)
    
    return session

@router.delete("/sessions/{session_id}")
def delete_chat_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete chat session."""
    session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    
    # Check permissions
    if current_user.role != "admin" and session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    title = session.title
    
    # Delete session (messages will be cascade deleted)
    db.delete(session)
    db.commit()
    
    # Log activity
    activity_log = ActivityLog(
        user_id=current_user.id,
        activity_type="delete_chat",
        description=f"Deleted chat session: {title}",
        metadata={"session_id": session_id}
    )
    db.add(activity_log)
    db.commit()
    
    return {"message": "Chat session deleted successfully"}

# Chat Messages
@router.get("/sessions/{session_id}/messages", response_model=List[schemas.ChatMessage])
def get_chat_messages(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get messages for a chat session."""
    session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    
    # Check permissions
    if current_user.role != "admin" and session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    messages = db.query(ChatMessage).filter(
        ChatMessage.session_id == session_id
    ).order_by(ChatMessage.created_at).all()
    
    return messages

@router.post("/messages", response_model=schemas.ChatMessage)
def create_chat_message(
    message: schemas.ChatMessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new chat message."""
    # Verify session exists and user has permission
    session = db.query(ChatSession).filter(ChatSession.id == message.session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    
    if current_user.role != "admin" and session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db_message = ChatMessage(
        session_id=message.session_id,
        role=message.role,
        content=message.content,
        token_count=message.token_count
    )
    
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    
    # Update session timestamp
    session.updated_at = func.now()
    db.add(session)
    db.commit()
    
    # Log activity
    activity_log = ActivityLog(
        user_id=current_user.id,
        activity_type="send_message",
        description=f"Sent message in session: {session.title}",
        metadata={"session_id": message.session_id, "message_id": db_message.id}
    )
    db.add(activity_log)
    db.commit()
    
    return db_message

@router.get("/stats/overview")
def get_chat_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get chat statistics."""
    session_query = db.query(ChatSession)
    message_query = db.query(ChatMessage).join(ChatSession)
    
    # Non-admin users can only see their own stats
    if current_user.role != "admin":
        session_query = session_query.filter(ChatSession.user_id == current_user.id)
        message_query = message_query.filter(ChatSession.user_id == current_user.id)
    
    total_sessions = session_query.count()
    active_sessions = session_query.filter(ChatSession.is_active == True).count()
    total_messages = message_query.count()
    
    # Model usage stats
    model_stats = db.query(
        ChatSession.model_name,
        func.count(ChatSession.id).label('count')
    )
    
    if current_user.role != "admin":
        model_stats = model_stats.filter(ChatSession.user_id == current_user.id)
    
    model_stats = model_stats.group_by(ChatSession.model_name).all()
    model_distribution = {model: count for model, count in model_stats}
    
    return {
        "total_sessions": total_sessions,
        "active_sessions": active_sessions,
        "total_messages": total_messages,
        "model_distribution": model_distribution
    }

@router.get("/models/list")
def get_available_models(current_user: User = Depends(get_current_user)):
    """Get list of available AI models."""
    return {
        "models": [
            {"value": "gpt-4", "label": "GPT-4", "provider": "azure"},
            {"value": "gpt-3.5-turbo", "label": "GPT-3.5 Turbo", "provider": "azure"},
            {"value": "llama2", "label": "Llama 2", "provider": "ollama"},
            {"value": "mistral", "label": "Mistral", "provider": "ollama"},
            {"value": "codellama", "label": "Code Llama", "provider": "ollama"}
        ]
    }
