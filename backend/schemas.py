from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(..., min_length=1)
    timestamp: datetime | None = None
    used_model: str | None = None
    concerns: list[str] = Field(default_factory=list)


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    model: str | None = None
    session_id: str = Field(default="default")


class ChatResponse(BaseModel):
    response: str
    used_model: str
    session_id: str
    safety_triggered: bool
    fallback_used: bool
    inferred_concerns: list[str] = Field(default_factory=list)


class ModelResponse(BaseModel):
    id: str
    label: str
    description: str
    status: str


class ModelListResponse(BaseModel):
    default_model: str
    fallback_model: str
    models: list[ModelResponse]


class SessionSummaryResponse(BaseModel):
    session_id: str
    title: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
    message_count: int
    preview: str = ""


class SessionListResponse(BaseModel):
    sessions: list[SessionSummaryResponse]


class SessionDetailResponse(BaseModel):
    session_id: str
    title: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
    messages: list[ChatMessage]
