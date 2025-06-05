# API router for v1
from fastapi import APIRouter
from .endpoints import (
    upload, processing, files, websocket, ai_switch,
    auth, users, documents, templates, chat, token_usage, dashboard
)

router = APIRouter()

# Existing endpoints
router.include_router(upload.router, prefix="/upload", tags=["upload"])
router.include_router(processing.router, prefix="/processing", tags=["processing"])
router.include_router(files.router, prefix="/files", tags=["files"])
router.include_router(websocket.router, prefix="/ws", tags=["websocket"])
router.include_router(ai_switch.router, prefix="/ai-service", tags=["ai-service"])

# New authentication and management endpoints
router.include_router(auth.router, prefix="/auth", tags=["authentication"])
router.include_router(users.router, prefix="/users", tags=["user-management"])
router.include_router(documents.router, prefix="/documents", tags=["document-management"])
router.include_router(templates.router, prefix="/templates", tags=["template-management"])
router.include_router(chat.router, prefix="/chat", tags=["chat-management"])
router.include_router(token_usage.router, prefix="/token-usage", tags=["token-usage"])
router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
