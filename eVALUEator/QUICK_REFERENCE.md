# Quick Reference

Essential commands for using the Opportunity Validator.

## Setup (One Time)

```bash
# 1. Navigate to project
cd opportunity-validator

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure API key
cp .env.example .env
nano .env  # Add your ANTHROPIC_API_KEY
```

## Daily Usage

```bash
# Activate environment (do this each time)
source venv/bin/activate

# Run quick start example
python examples/quick_start.py

# Run your own validation
python my_opportunities.py

# Run tests
pytest tests/ -v

# Deactivate when done
deactivate
```

## Git Commands

```bash
# See what changed
git status
git diff

# Save changes
git add .
git commit -m "Description"
git push

# Undo changes (before commit)
git checkout .

# Undo specific file
git checkout -- path/to/file.py

# Go back to previous commit
git log --oneline          # Find commit hash
git reset --hard <hash>    # Reset to that commit
```

## Python Usage

```python
from src.validator import OpportunityValidator

# Initialize
validator = OpportunityValidator()

# Single opportunity
result = validator.validate_opportunity({
    "name": "My Idea",
    "description": "What it does",
    "icp": "Who it's for",
    "problem": "What problem it solves"
})

# Multiple opportunities (parallel)
results = validator.validate_opportunities([opp1, opp2, opp3])

# Compare and rank
comparison = validator.compare_opportunities(results)

# Get top recommendation
best = validator.recommend_next(results)
print(f"Pursue: {best.opportunity.name}")
```

## File Locations

```bash
# Your opportunities and results
./opportunities/

# Example opportunities
./examples/sample_opportunities.json

# Validation framework docs
./docs/validation_framework.md

# Main validator code
./src/validator.py

# Data models
./src/models/opportunity.py

# Agent prompts
./src/prompts/orchestrator.md
```

## Troubleshooting

```bash
# Can't find deepagents module
source venv/bin/activate
pip install -r requirements.txt

# API key error
cat .env  # Check if key is there
nano .env # Add ANTHROPIC_API_KEY=your-key

# Permission error
chmod +x examples/quick_start.py
# OR
python examples/quick_start.py

# Tests failing
pytest tests/ -v  # See detailed errors
```

## Costs

- Single opportunity: ~$0.50
- 5 opportunities (parallel): ~$2.50
- Sequential validation: Slower but same cost

## Next Steps

1. Run `python examples/quick_start.py`
2. Edit `examples/sample_opportunities.json` with your ideas
3. Run validation on your opportunities
4. Review results in `./opportunities/` folder
5. Pick top opportunity and move to Step 1

## Resources

- Setup guide: `SETUP.md`
- Git guide: `GIT_SETUP.md`
- Framework docs: `docs/validation_framework.md`
- Main README: `README.md`
