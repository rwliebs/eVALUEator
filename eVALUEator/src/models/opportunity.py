"""
Data models for opportunity validation
"""

from typing import Optional, List, Dict
from pydantic import BaseModel, Field


class Opportunity(BaseModel):
    """Represents a business opportunity to validate"""
    
    name: str = Field(..., description="Short name for the opportunity")
    description: str = Field(..., description="What you're building")
    icp: str = Field(..., description="Ideal Customer Profile - who is this for?")
    problem: str = Field(..., description="What problem does this solve?")
    
    # Optional: Pre-filled information
    aspiration: Optional[str] = Field(None, description="What they want to achieve")
    workaround: Optional[str] = Field(None, description="Current solution they use")
    communities: Optional[List[str]] = Field(None, description="Where ICP hangs out")
    

class ResearchFindings(BaseModel):
    """Research results for an opportunity"""
    
    opportunity_name: str
    
    # Community Discovery
    communities_found: List[Dict[str, any]] = Field(
        default_factory=list,
        description="Communities where ICP gathers"
    )
    
    # Budget Research
    budget_evidence: List[Dict[str, any]] = Field(
        default_factory=list,
        description="Evidence of what they pay for similar tools"
    )
    pays_for_tools: bool = Field(default=False)
    price_range: Optional[str] = None
    
    # Pain Validation
    pain_discussions: List[Dict[str, any]] = Field(
        default_factory=list,
        description="Discussions mentioning the problem"
    )
    emotional_intensity: Optional[str] = Field(None, description="high/medium/low")
    
    # Competition
    competitors: List[Dict[str, any]] = Field(
        default_factory=list,
        description="Existing solutions"
    )
    competition_gap: Optional[str] = Field(None, description="Identified gaps")
    
    confidence: float = Field(0.0, ge=0.0, le=1.0, description="Research confidence")
    notes: str = Field("", description="Additional context")


class OpportunityScore(BaseModel):
    """Validation score for an opportunity"""
    
    opportunity_name: str
    
    # Problem-Solution Fit (0-30)
    aspiration_clarity: int = Field(..., ge=0, le=10)
    workaround_pain: int = Field(..., ge=0, le=10)
    stuck_pattern: int = Field(..., ge=0, le=10)
    
    # Market Signals (0-30)
    market_size: int = Field(..., ge=0, le=10)
    budget_confirmed: int = Field(..., ge=0, le=10)
    competition_gap: int = Field(..., ge=0, le=10)
    
    # Founder-Market Fit (0-30)
    domain_expertise: int = Field(..., ge=0, le=10)
    audience_access: int = Field(..., ge=0, le=10)
    passion_level: int = Field(..., ge=0, le=10)
    
    # Execution Feasibility (0-30)
    technical_capability: int = Field(..., ge=0, le=10)
    reachability: int = Field(..., ge=0, le=10)
    virality_potential: int = Field(..., ge=0, le=10)
    
    # Calculated fields
    total_score: int = Field(0, ge=0, le=120)
    efficiency_score: float = Field(0.0, description="Total / (Market Size + 1)")
    
    # Reasoning
    reasoning: str = Field("", description="Explanation of scores")
    recommendation: str = Field("", description="proceed/monitor/reject")
    next_action: str = Field("", description="What to do next")
    
    def calculate_totals(self):
        """Calculate total and efficiency scores"""
        self.total_score = (
            self.aspiration_clarity + self.workaround_pain + self.stuck_pattern +
            self.market_size + self.budget_confirmed + self.competition_gap +
            self.domain_expertise + self.audience_access + self.passion_level +
            self.technical_capability + self.reachability + self.virality_potential
        )
        self.efficiency_score = round(self.total_score / (self.market_size + 1), 2)


class ValidationResult(BaseModel):
    """Complete validation result including research and scoring"""
    
    opportunity: Opportunity
    research: ResearchFindings
    score: OpportunityScore
    status: str = Field("completed", description="pending/in_progress/completed/failed")
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization"""
        return {
            "opportunity": self.opportunity.model_dump(),
            "research": self.research.model_dump(),
            "score": self.score.model_dump(),
            "status": self.status
        }
