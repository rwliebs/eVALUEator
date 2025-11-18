"""
Quick Start Example - Validate Multiple Opportunities

This script demonstrates how to validate several business opportunities
in parallel using the OpportunityValidator.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from validator import OpportunityValidator


def main():
    print("=" * 60)
    print("OPPORTUNITY VALIDATOR - QUICK START")
    print("=" * 60)
    
    # Initialize validator
    validator = OpportunityValidator()
    
    # Define opportunities to validate
    opportunities = [
        {
            "name": "ESL Teacher Feedback Tool",
            "description": "Automated tool for VIPKid teachers to manage and respond to student feedback",
            "icp": "Online ESL teachers on VIPKid platform",
            "problem": "Managing and responding to student feedback is time-consuming and repetitive",
            "communities": ["r/VIPKid", "VIPKid Teachers Facebook Group"]
        },
        {
            "name": "ENM Calendar API",
            "description": "Shared calendar system for polyamorous relationships",
            "icp": "People in ethical non-monogamous relationships",
            "problem": "Coordinating schedules across multiple partners is complex and prone to conflicts",
            "communities": ["r/polyamory", "r/nonmonogamy"]
        },
        {
            "name": "AI Song Generator",
            "description": "Generate custom songs from text prompts for content creators",
            "icp": "YouTube creators and social media influencers",
            "problem": "Creating original music for content is expensive and time-consuming",
        }
    ]
    
    print(f"\n📋 Loaded {len(opportunities)} opportunities to validate")
    
    # Validate all opportunities in parallel
    print("\n" + "=" * 60)
    print("STEP 1: PARALLEL VALIDATION")
    print("=" * 60)
    
    results = validator.validate_opportunities(opportunities, parallel=True)
    
    # Compare results
    print("\n" + "=" * 60)
    print("STEP 2: COMPARISON & RECOMMENDATION")
    print("=" * 60)
    
    comparison = validator.compare_opportunities(results)
    
    # Get top recommendation
    best = validator.recommend_next(results)
    
    print("\n" + "=" * 60)
    print("NEXT STEPS")
    print("=" * 60)
    print(f"\n🎯 RECOMMENDED: {best.opportunity.name}")
    print(f"   Score: {best.score.total_score}/120")
    print(f"   Efficiency: {best.score.efficiency_score}")
    print(f"   Action: {best.score.next_action}")
    
    print(f"\n📁 Detailed results saved to ./opportunities/")
    print(f"\n✅ Validation complete!")


if __name__ == "__main__":
    main()
