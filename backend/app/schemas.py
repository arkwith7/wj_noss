# Pydantic models for API requests and responses
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

# User Models
class UserRole(str, Enum):
    ADMIN = "admin"
    INSTRUCTOR = "instructor"
    STUDENT = "student"

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    role: UserRole = UserRole.STUDENT

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None

class UserInDB(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    model_config = {'from_attributes': True}

class User(UserInDB):
    pass

# Authentication Models
class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    user: UserInDB

class TokenData(BaseModel):
    username: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str

# Document Models
class DocumentStatus(str, Enum):
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    PROCESSED = "processed"
    ERROR = "error"

class DocumentBase(BaseModel):
    filename: str
    title: str
    description: Optional[str] = None
    file_type: str
    file_size: int

class DocumentCreate(DocumentBase):
    pass

class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[DocumentStatus] = None
    metadata: Optional[Dict[str, Any]] = None

class DocumentInDB(DocumentBase):
    id: int
    file_path: str
    status: DocumentStatus
    uploaded_by: int
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime
    model_config = {'from_attributes': True}

class Document(DocumentInDB):
    uploader: User

# Template Models
class TemplateType(str, Enum):
    COURSE = "course"
    UNIT = "unit"
    LESSON = "lesson"
    ASSESSMENT = "assessment"

class TemplateBase(BaseModel):
    name: str
    description: Optional[str] = None
    template_type: TemplateType
    content_template: str
    is_active: bool = True

class TemplateCreate(TemplateBase):
    pass

class TemplateUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    template_type: Optional[TemplateType] = None
    content_template: Optional[str] = None
    is_active: Optional[bool] = None
    metadata: Optional[Dict[str, Any]] = None

class TemplateInDB(TemplateBase):
    id: int
    created_by: int
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime
    model_config = {'from_attributes': True}

class Template(TemplateInDB):
    creator: User

# Chat Models
class ChatSessionBase(BaseModel):
    title: str
    model_name: str
    model_config = {'protected_namespaces': ()}

class ChatSessionCreate(ChatSessionBase):
    pass

class ChatSessionUpdate(BaseModel):
    title: Optional[str] = None
    is_active: Optional[bool] = None
    model_config = {'protected_namespaces': ()}

class ChatSessionInDB(ChatSessionBase):
    id: int
    user_id: int
    is_active: bool = True
    created_at: datetime
    updated_at: datetime
    model_config = {
        'protected_namespaces': (),
        'from_attributes': True
    }

class ChatSession(ChatSessionInDB):
    user: User

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class ChatMessageBase(BaseModel):
    role: MessageRole
    content: str
    token_count: Optional[int] = None

class ChatMessageCreate(ChatMessageBase):
    session_id: int

class ChatMessageInDB(ChatMessageBase):
    id: int
    session_id: int
    created_at: datetime
    model_config = {'from_attributes': True}

class ChatMessage(ChatMessageInDB):
    session: ChatSession

# Template Generation Models
class GenerationStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class TemplateGenerationBase(BaseModel):
    title: str
    template_id: int
    document_ids: List[int]
    parameters: Dict[str, Any]

class TemplateGenerationCreate(TemplateGenerationBase):
    pass

class TemplateGenerationUpdate(BaseModel):
    status: Optional[GenerationStatus] = None
    progress: Optional[int] = None
    result_content: Optional[str] = None
    error_message: Optional[str] = None

class TemplateGenerationInDB(TemplateGenerationBase):
    id: int
    user_id: int
    status: GenerationStatus = GenerationStatus.PENDING
    progress: int = 0
    result_content: Optional[str] = None
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    model_config = {'from_attributes': True}

class TemplateGeneration(TemplateGenerationInDB):
    user: User
    template: Template
    documents: List[Document]

# Metadata Models
class MetadataFieldType(str, Enum):
    TEXT = "text"
    NUMBER = "number"
    DATE = "date"
    BOOLEAN = "boolean"
    SELECT = "select"
    MULTISELECT = "multiselect"

class MetadataFieldBase(BaseModel):
    name: str
    display_name: str
    field_type: MetadataFieldType
    is_required: bool = False
    default_value: Optional[str] = None
    options: Optional[List[str]] = None  # For select/multiselect fields

class MetadataFieldCreate(MetadataFieldBase):
    pass

class MetadataFieldUpdate(BaseModel):
    display_name: Optional[str] = None
    field_type: Optional[MetadataFieldType] = None
    is_required: Optional[bool] = None
    default_value: Optional[str] = None
    options: Optional[List[str]] = None
    is_active: Optional[bool] = None

class MetadataFieldInDB(MetadataFieldBase):
    id: int
    is_active: bool = True
    created_at: datetime
    updated_at: datetime
    model_config = {'from_attributes': True}

class MetadataField(MetadataFieldInDB):
    pass

# Tag Models
class TagBase(BaseModel):
    name: str
    color: Optional[str] = None
    description: Optional[str] = None

class TagCreate(TagBase):
    pass

class TagUpdate(BaseModel):
    name: Optional[str] = None
    color: Optional[str] = None
    description: Optional[str] = None

class TagInDB(TagBase):
    id: int
    created_at: datetime
    model_config = {'from_attributes': True}

class Tag(TagInDB):
    pass

# Token Usage Models
class TokenUsageBase(BaseModel):
    model_name: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    cost: Optional[float] = None
    model_config = {'protected_namespaces': ()}

class TokenUsageCreate(TokenUsageBase):
    user_id: int
    session_id: Optional[int] = None
    model_config = {'protected_namespaces': ()}

class TokenUsageInDB(TokenUsageBase):
    id: int
    user_id: int
    session_id: Optional[int] = None
    created_at: datetime
    model_config = {
        'protected_namespaces': (),
        'from_attributes': True
    }

class TokenUsage(TokenUsageInDB):
    user: User
    session: Optional[ChatSession] = None

# Activity Log Models
class ActivityType(str, Enum):
    LOGIN = "login"
    LOGOUT = "logout"
    UPLOAD_DOCUMENT = "upload_document"
    GENERATE_TEMPLATE = "generate_template"
    CREATE_CHAT = "create_chat"
    SEND_MESSAGE = "send_message"
    CREATE_TEMPLATE = "create_template"
    UPDATE_TEMPLATE = "update_template"
    DELETE_TEMPLATE = "delete_template"

class ActivityLogBase(BaseModel):
    activity_type: ActivityType
    description: str
    metadata: Optional[Dict[str, Any]] = None

class ActivityLogCreate(ActivityLogBase):
    user_id: int

class ActivityLogInDB(ActivityLogBase):
    id: int
    user_id: int
    created_at: datetime
    model_config = {'from_attributes': True}

class ActivityLog(ActivityLogInDB):
    user: User

# Response Models
class ResponseModel(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None

class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    per_page: int
    pages: int
