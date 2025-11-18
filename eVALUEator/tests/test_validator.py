"""
Basic tests for OpportunityValidator

Run with: python -m pytest tests/
"""

import pytest
from src.models.opportunity import Opportunity, OpportunityScore


def test_opportunity_model():
    """Test Opportunity model creation"""
    opp = Opportunity(
        name="Test Opportunity",
        description="A test opportunity",
        icp="Test users",
        problem="Test problem"
    )
    assert opp.name == "Test Opportunity"
    assert opp.icp == "Test users"


def test_opportunity_score_calculation():
    """Test score calculation"""
    score = OpportunityScore(
        opportunity_name="Test",
        aspiration_clarity=8,
        workaround_pain=7,
        stuck_pattern=6,
        market_size=9,
        budget_confirmed=7,
        competition_gap=8,
        domain_expertise=8,
        audience_access=7,
        passion_level=9,
        technical_capability=8,
        reachability=9,
        virality_potential=6
    )
    
    score.calculate_totals()
    
    assert score.total_score == 92
    assert score.efficiency_score == 9.2


def test_efficiency_score_with_zero_market():
    """Test efficiency score when market size is 0"""
    score = OpportunityScore(
        opportunity_name="Test",
        aspiration_clarity=8,
        workaround_pain=7,
        stuck_pattern=6,
        market_size=0,
        budget_confirmed=7,
        competition_gap=8,
        domain_expertise=8,
        audience_access=7,
        passion_level=9,
        technical_capability=8,
        reachability=9,
        virality_potential=6
    )
    
    score.calculate_totals()
    
    # Should not divide by zero
    assert score.efficiency_score == 83.0  # 83 / (0 + 1)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
