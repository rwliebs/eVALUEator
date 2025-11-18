# eVALUEator

A systematic framework for validating business opportunities using AI agents to avoid wasted time on bad ideas.

## What It Does

Validates multiple business opportunities **in parallel** by:
- 🔍 Researching target audience, budget, and communities
- 📊 Scoring based on 12 validation dimensions
- ⚖️ Comparing opportunities side-by-side
- 🎯 Recommending which to pursue

Built with [Deep Agents](https://github.com/langchain-ai/deepagents) - orchestrates Claude-powered sub-agents for research, scoring, and decision-making.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up API Key

```bash
# Copy example env file
cp .env.example .env

# Add your Anthropic API key to .env
echo "ANTHROPIC_API_KEY=your_key_here" >> .env
```

### 3. Run Example

```bash
python examples/quick_start.py
```

## Usage

### Basic Validation

```python
from src.validator import OpportunityValidator

validator = OpportunityValidator()

opportunities = [
    {
        "name": "ESL Teacher Feedback Tool",
        "description": "Helps VIPKid teachers manage student feedback",
        "icp": "Online ESL teachers on VIPKid platform",
        "problem": "Managing feedback is time-consuming"
    },
    {
        "name": "ENM Calendar API", 
        "description": "Shared calendar for polyamorous relationships",
        "icp": "People in ethical non-monogamous relationships",
        "problem": "Coordinating schedules across multiple partners"
    }
]

# Validate all opportunities in parallel
results = validator.validate_opportunities(opportunities)

# View comparison
validator.compare_opportunities(results)

# Get recommendation
best = validator.recommend_next(results)
print(f"Pursue: {best['name']} (Score: {best['score']}/120)")
```

### Advanced: Custom Research

```python
# Validate with specific research focus
result = validator.validate_opportunity(
    opportunity={
        "name": "AI Song Generator",
        "description": "Generate custom songs from prompts",
        "icp": "Content creators and musicians",
        "problem": "Creating original music is expensive"
    },
    research_focus=[
        "Find evidence of budget for music tools",
        "Identify online communities of content creators",
        "Look for AI music tool competitors and pricing"
    ]
)
```

## How It Works

### Architecture

```
Orchestrator Agent
    ├── Research Sub-Agent #1 (Opportunity A)
    ├── Research Sub-Agent #2 (Opportunity B)  [parallel]
    ├── Research Sub-Agent #3 (Opportunity C)
    └── Scorer Sub-Agent
            └── Compares all findings
            └── Generates rankings
```

### Validation Framework (Step 0: Discovery)

Each opportunity is scored on 12 dimensions (0-10 each):

**Problem-Solution Fit:**
- Aspiration clarity
- Workaround pain  
- Stuck pattern

**Market Signals:**
- Market size
- Budget confirmed
- Competition gap

**Founder-Market Fit:**
- Domain expertise
- Audience access
- Passion level

**Execution:**
- Technical capability
- Reachability
- Virality potential

**Total Score:** 0-120
**Efficiency Score:** Total / (Market Size + 1)

### Research Process

For each opportunity, the system:

1. **Community Discovery** - Finds where ICP hangs out (Reddit, Discord, forums)
2. **Budget Research** - Looks for evidence they pay for similar tools
3. **Pain Validation** - Analyzes discussions for problem intensity
4. **Competition Analysis** - Identifies existing solutions and gaps

All findings are saved to `/opportunities/{name}/` for review.

## File Structure

```
opportunity-validator/
├── src/
│   ├── validator.py          # Main OpportunityValidator class
│   ├── models/
│   │   └── opportunity.py    # Data models
│   └── prompts/
│       ├── orchestrator.md   # Main agent prompt
│       ├── researcher.md     # Research sub-agent
│       └── scorer.md         # Scoring sub-agent
├── examples/
│   ├── quick_start.py
│   └── sample_opportunities.json
├── tests/
│   └── test_validator.py
└── docs/
    └── validation_framework.md
```

## Configuration

### Environment Variables

- `ANTHROPIC_API_KEY` - Your Anthropic API key (required)
- `VALIDATION_MODEL` - Claude model to use (default: `claude-sonnet-4-20250514`)

### Custom Prompts

Edit prompts in `src/prompts/` to customize validation logic:
- `orchestrator.md` - Main coordination logic
- `researcher.md` - Research methodology  
- `scorer.md` - Scoring criteria

## Cost Estimates

Per opportunity validation:
- Research: ~10,000 tokens (~$0.30)
- Scoring: ~5,000 tokens (~$0.15)
- **Total: ~$0.45 per opportunity**

Validating 5 opportunities in parallel: ~$2.25

## Roadmap

- [ ] Step 1 validation (community discussion analysis)
- [ ] Step 2 validation (landing page testing)
- [ ] Step 3 validation (conversation testing)
- [ ] Web dashboard for results
- [ ] Integration with Google Sheets for opportunity tracking
- [ ] Slack notifications for completed validations

## Why This Exists

After spending 7 months building something that didn't gain traction, I needed a systematic way to validate ideas BEFORE investing months of work. This system:

- Validates 5 ideas in parallel (not sequentially)
- Provides evidence-based scoring (not gut feel)
- Works while you do other things (async research)
- Helps you say "no" faster to bad ideas

## License

MIT

## Credits

Built with:
- [Deep Agents](https://github.com/langchain-ai/deepagents) by LangChain
- [Claude](https://anthropic.com/claude) by Anthropic
- Validation framework inspired by product discovery methodologies
