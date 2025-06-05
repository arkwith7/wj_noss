# Pydantic models for Enhanced Competency Unit
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class CompetencyUnitMetadata(BaseModel):
    extraction_method: str
    ai_model_used: str
    confidence_score: float
    validation_status: str
    source_pages: List[int]
    extraction_timestamp: datetime
    quality_indicators: Dict[str, float]
    processing_metrics: Dict[str, Any]

class WorkActivity(BaseModel):
    id: str
    title: str
    description: str
    sequence_number: int
    performance_criteria: List[str]
    range_of_variables: Optional[str]
    evidence_guide: Optional[str]

class ExcelMatch(BaseModel):
    sheet_name: str
    row_index: int
    match_score: float
    data: Dict[str, Any]

class EnhancedCompetencyUnit(BaseModel):
    id: str = Field(..., description="고유 식별자")
    program_code: str
    program_name: str
    program_level: str
    competency_unit_name: str
    competency_unit_title: str
    work_activities: List[WorkActivity]
    learning_outcomes: List[str]
    assessment_criteria: List[str]
    metadata: CompetencyUnitMetadata
    relationships: Dict[str, Any]
    excel_matches: List[ExcelMatch] = []
    matching_confidence: Optional[float] = None
