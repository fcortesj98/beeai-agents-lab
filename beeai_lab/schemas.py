"""Pydantic schemas for structured outputs (lab section 4)."""

from __future__ import annotations

from pydantic import BaseModel, Field


class BusinessPlan(BaseModel):
    """A comprehensive business plan structure."""

    business_name: str = Field(description="Catchy name for the business")
    elevator_pitch: str = Field(description="30-second description of the business")
    target_market: str = Field(description="Primary target audience")
    unique_value_proposition: str = Field(description="What makes this business special")
    revenue_streams: list[str] = Field(description="Ways the business will make money")
    startup_costs: str = Field(description="Estimated initial investment needed")
    key_success_factors: list[str] = Field(description="Critical elements for success")
