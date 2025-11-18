"""
Main Opportunity Validator using Deep Agents
"""

import json
import os
from typing import List, Dict, Optional
from pathlib import Path
from dotenv import load_dotenv

from deepagents import create_deep_agent
from deepagents.backends import StateBackend, CompositeBackend, StoreBackend
from deepagents.middleware import FilesystemMiddleware
from langchain_anthropic import ChatAnthropic

from .models.opportunity import Opportunity, ValidationResult, OpportunityScore, ResearchFindings


class OpportunityValidator:
    """
    Validates business opportunities using AI agents
    
    Spawns specialized sub-agents for:
    - Research (community discovery, budget validation, pain analysis)
    - Scoring (systematic evaluation against validation framework)
    - Comparison (ranking multiple opportunities)
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = None):
        """
        Initialize the validator
        
        Args:
            api_key: Anthropic API key (or set ANTHROPIC_API_KEY env var)
            model: Claude model to use (default: claude-sonnet-4-20250514)
        """
        # Load environment variables
        load_dotenv()
        
        if api_key:
            os.environ["ANTHROPIC_API_KEY"] = api_key
        
        if not os.getenv("ANTHROPIC_API_KEY"):
            raise ValueError(
                "ANTHROPIC_API_KEY not found. Set it in .env file or pass as argument"
            )
        
        # Set model
        model_name = model or os.getenv("VALIDATION_MODEL", "claude-sonnet-4-20250514")
        
        # Create hybrid storage backend
        # /opportunities/ directory persists across runs
        backend = CompositeBackend(
            default=StateBackend(),  # Ephemeral for working memory
            routes={
                "/opportunities/": StoreBackend()  # Persistent for results
            }
        )
        
        # Load system prompt
        prompt_path = Path(__file__).parent / "prompts" / "orchestrator.md"
        with open(prompt_path, "r") as f:
            system_prompt = f.read()
        
        # Create the orchestrator agent
        self.agent = create_deep_agent(
            model=ChatAnthropic(model=model_name),
            system_prompt=system_prompt,
            middleware=[FilesystemMiddleware(backend=backend)]
        )
        
        print(f"✓ OpportunityValidator initialized with {model_name}")
    
    def validate_opportunity(
        self, 
        opportunity: Dict,
        research_focus: Optional[List[str]] = None
    ) -> ValidationResult:
        """
        Validate a single opportunity
        
        Args:
            opportunity: Dict with name, description, icp, problem
            research_focus: Optional list of specific research questions
            
        Returns:
            ValidationResult with research findings and score
        """
        opp = Opportunity(**opportunity)
        
        print(f"\n🔍 Validating: {opp.name}")
        print(f"   ICP: {opp.icp}")
        print(f"   Problem: {opp.problem}")
        
        # Build validation request
        request = self._build_validation_request(opp, research_focus)
        
        # Run agent
        result = self.agent.invoke({
            "messages": [{"role": "user", "content": request}]
        })
        
        # Parse results
        validation_result = self._parse_validation_result(opp, result)
        
        # Save to file system
        self._save_result(validation_result)
        
        print(f"✓ Validation complete for {opp.name}")
        print(f"   Score: {validation_result.score.total_score}/120")
        print(f"   Recommendation: {validation_result.score.recommendation}")
        
        return validation_result
    
    def validate_opportunities(
        self, 
        opportunities: List[Dict],
        parallel: bool = True
    ) -> List[ValidationResult]:
        """
        Validate multiple opportunities
        
        Args:
            opportunities: List of opportunity dicts
            parallel: Whether to validate in parallel (default: True)
            
        Returns:
            List of ValidationResults
        """
        print(f"\n📊 Validating {len(opportunities)} opportunities{'in parallel' if parallel else 'sequentially'}...")
        
        if parallel:
            # Build batch request for parallel processing
            request = self._build_batch_request(opportunities)
            
            result = self.agent.invoke({
                "messages": [{"role": "user", "content": request}]
            })
            
            # Parse results for all opportunities
            results = self._parse_batch_results(opportunities, result)
        else:
            # Sequential validation
            results = [
                self.validate_opportunity(opp) 
                for opp in opportunities
            ]
        
        print(f"\n✓ All validations complete")
        return results
    
    def compare_opportunities(self, results: List[ValidationResult]) -> Dict:
        """
        Compare multiple validated opportunities
        
        Args:
            results: List of ValidationResults to compare
            
        Returns:
            Dict with comparison analysis and rankings
        """
        print(f"\n⚖️  Comparing {len(results)} opportunities...")
        
        # Build comparison request
        request = self._build_comparison_request(results)
        
        result = self.agent.invoke({
            "messages": [{"role": "user", "content": request}]
        })
        
        # Extract comparison from result
        comparison = self._parse_comparison_result(result)
        
        # Print summary
        print("\n" + "="*60)
        print("OPPORTUNITY RANKINGS")
        print("="*60)
        for rank, opp in enumerate(comparison["rankings"], 1):
            print(f"\n#{rank}: {opp['name']} - Score: {opp['score']}/120")
            print(f"    Efficiency: {opp['efficiency_score']}")
            print(f"    {opp['summary']}")
        
        print("\n" + "="*60)
        print(f"RECOMMENDATION: {comparison['recommendation']}")
        print("="*60)
        
        return comparison
    
    def recommend_next(self, results: List[ValidationResult]) -> ValidationResult:
        """
        Get recommendation for which opportunity to pursue next
        
        Args:
            results: List of ValidationResults
            
        Returns:
            The recommended ValidationResult
        """
        comparison = self.compare_opportunities(results)
        top_opportunity_name = comparison["rankings"][0]["name"]
        
        return next(r for r in results if r.opportunity.name == top_opportunity_name)
    
    def _build_validation_request(self, opp: Opportunity, focus: Optional[List[str]]) -> str:
        """Build the validation request for an opportunity"""
        request = f"""
Validate this business opportunity:

**Opportunity**: {opp.name}
**Description**: {opp.description}
**Target ICP**: {opp.icp}
**Problem**: {opp.problem}
"""
        
        if opp.aspiration:
            request += f"\n**Aspiration**: {opp.aspiration}"
        if opp.workaround:
            request += f"\n**Current Workaround**: {opp.workaround}"
        if opp.communities:
            request += f"\n**Known Communities**: {', '.join(opp.communities)}"
        
        request += """

Please:
1. Spawn a research sub-agent to find:
   - Where this ICP hangs out online (communities)
   - Evidence they pay for similar tools (budget validation)
   - Discussions showing pain intensity
   - Existing competitors and gaps

2. Once research is complete, spawn a scoring sub-agent to evaluate on all 12 dimensions

3. Save findings to /opportunities/{name}/

4. Return structured results as JSON
"""
        
        if focus:
            request += f"\n\nResearch focus areas:\n" + "\n".join(f"- {f}" for f in focus)
        
        return request
    
    def _build_batch_request(self, opportunities: List[Dict]) -> str:
        """Build request for batch validation"""
        opps = [Opportunity(**o) for o in opportunities]
        
        request = f"""
Validate these {len(opps)} business opportunities IN PARALLEL:

"""
        for i, opp in enumerate(opps, 1):
            request += f"""
{i}. **{opp.name}**
   - Description: {opp.description}
   - ICP: {opp.icp}
   - Problem: {opp.problem}
"""
        
        request += """

For EACH opportunity:
1. Spawn a dedicated research sub-agent (so contexts don't mix)
2. Research: communities, budget evidence, pain discussions, competition
3. Spawn a scoring sub-agent to evaluate
4. Save to /opportunities/{name}/

Return all results as a JSON array.
"""
        
        return request
    
    def _build_comparison_request(self, results: List[ValidationResult]) -> str:
        """Build request for comparing opportunities"""
        request = "Compare these validated opportunities and provide rankings:\n\n"
        
        for i, result in enumerate(results, 1):
            score = result.score
            request += f"""
{i}. {result.opportunity.name} (Score: {score.total_score}/120, Efficiency: {score.efficiency_score})
   - ICP: {result.opportunity.icp}
   - Key strengths: Market Size={score.market_size}, Budget={score.budget_confirmed}
   - Recommendation: {score.recommendation}
   - Research confidence: {result.research.confidence}
"""
        
        request += """

Analyze and return:
1. Rankings (best to worst)
2. Comparison of strengths/weaknesses
3. Which to pursue first and why
4. Any that should be rejected outright

Return as JSON.
"""
        
        return request
    
    def _parse_validation_result(self, opp: Opportunity, agent_result) -> ValidationResult:
        """Parse agent result into ValidationResult"""
        # Extract text from agent response
        messages = agent_result.get("messages", [])
        response_text = ""
        for msg in messages:
            if isinstance(msg, dict) and msg.get("type") == "ai":
                response_text += msg.get("content", "")
        
        # Try to extract JSON from response
        # For now, create a placeholder result
        # TODO: Parse actual JSON from agent response
        
        research = ResearchFindings(
            opportunity_name=opp.name,
            confidence=0.7,
            notes="Research in progress"
        )
        
        score = OpportunityScore(
            opportunity_name=opp.name,
            aspiration_clarity=7,
            workaround_pain=6,
            stuck_pattern=5,
            market_size=8,
            budget_confirmed=6,
            competition_gap=7,
            domain_expertise=8,
            audience_access=7,
            passion_level=9,
            technical_capability=8,
            reachability=7,
            virality_potential=6,
            reasoning="Scores based on initial research",
            recommendation="proceed",
            next_action="Continue to Step 1 validation"
        )
        score.calculate_totals()
        
        return ValidationResult(
            opportunity=opp,
            research=research,
            score=score,
            status="completed"
        )
    
    def _parse_batch_results(self, opportunities: List[Dict], agent_result) -> List[ValidationResult]:
        """Parse batch validation results"""
        # For now, run individual validations
        # TODO: Parse batch JSON response
        return [
            self.validate_opportunity(opp)
            for opp in opportunities
        ]
    
    def _parse_comparison_result(self, agent_result) -> Dict:
        """Parse comparison analysis"""
        # TODO: Parse JSON from agent
        return {
            "rankings": [
                {
                    "name": "Opportunity 1",
                    "score": 85,
                    "efficiency_score": 9.4,
                    "summary": "Strong market signals"
                }
            ],
            "recommendation": "Pursue Opportunity 1 first"
        }
    
    def _save_result(self, result: ValidationResult):
        """Save validation result to filesystem"""
        output_dir = Path("opportunities") / result.opportunity.name.replace(" ", "_")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / "validation_result.json"
        with open(output_file, "w") as f:
            json.dump(result.to_dict(), f, indent=2)
        
        print(f"   Saved to {output_file}")
