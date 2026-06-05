"""
schema.py — Pydantic models for structured chatbot responses.
"""

from typing import Optional, List
from pydantic import BaseModel, Field


class IntentResult(BaseModel):
    """Structured output from Step 1 — Intent Classifier."""
    intent_type: str = Field(..., description="Classified banking intent")
    confidence: str = Field(..., description="High | Medium | Low")
    urgency: str = Field(..., description="Critical | High | Medium | Low")
    sentiment: str = Field(..., description="Distressed | Angry | Neutral | Positive")
    is_follow_up: bool = Field(False, description="Whether this is a follow-up turn")
    follow_up_refers_to: Optional[str] = Field(None, description="Topic of prior follow-up")
    entities: dict = Field(default_factory=dict, description="Extracted entities")
    language: str = Field("English", description="English | Hindi | Mixed")


class ContextResult(BaseModel):
    """Structured output from Step 2 — Context Retriever."""
    relevant_facts: List[str] = Field(default_factory=list)
    applicable_rates: dict = Field(default_factory=dict)
    applicable_policies: List[str] = Field(default_factory=list)
    regulatory_references: List[str] = Field(default_factory=list)
    risk_flags: List[str] = Field(default_factory=list)
    recommended_products: List[str] = Field(default_factory=list)
    escalation_needed: bool = Field(False)
    escalation_reason: Optional[str] = Field(None)


class ChatResponse(BaseModel):
    """Final structured response stored per turn."""
    turn: int = Field(..., description="Turn number in conversation")
    user_message: str = Field(..., description="Original customer message")
    intent: str = Field(..., description="Classified intent")
    confidence: str = Field(..., description="Classification confidence")
    urgency: str = Field(..., description="Query urgency level")
    sentiment: str = Field(..., description="Customer sentiment")
    escalation_required: bool = Field(False, description="Whether escalation is needed")
    escalation_reason: Optional[str] = Field(None)
    facts_used: int = Field(0, description="Number of KB facts used in response")
    advisor_response: str = Field(..., description="Final natural language response")
    notes: Optional[str] = Field(None, description="Any extra notes or flags")
