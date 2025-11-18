# Git Setup Instructions

Follow these steps to initialize the repository and push to GitHub.

## 1. Navigate to Project

```bash
cd /path/to/opportunity-validator
```

## 2. Initialize Git

```bash
git init
```

## 3. Create Initial Commit

```bash
# Add all files
git add .

# Make first commit
git commit -m "Initial commit: Opportunity Validator with Deep Agents"
```

## 4. Create GitHub Repository

1. Go to https://github.com/new
2. Name it: `opportunity-validator`
3. Description: "AI-powered system for validating business opportunities"
4. Choose: Public or Private
5. **DO NOT** initialize with README (we already have one)
6. Click "Create repository"

## 5. Push to GitHub

```bash
# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/opportunity-validator.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## 6. Verify

Visit your repository at:
`https://github.com/YOUR_USERNAME/opportunity-validator`

---

## Common Git Commands for AI Coding

### Before Making Changes

```bash
# Check current status
git status

# Create a branch for experiments
git checkout -b experiment-feature
```

### After AI Generates Code

```bash
# See what changed
git diff

# If good, commit
git add .
git commit -m "Add feature X"

# If bad, undo ALL changes
git checkout .

# If partially good, undo specific file
git checkout -- path/to/file.py
```

### Working with AI Iterations

```bash
# Save working version
git add .
git commit -m "Working version before trying X"

# Try AI suggestion
# ... make changes ...

# If breaks, undo
git reset --hard HEAD

# If works, commit
git add .
git commit -m "Successfully added X"
```

### Viewing History

```bash
# See all commits
git log --oneline

# Go back to specific commit
git checkout <commit-hash>

# Return to latest
git checkout main
```

### Branches for Safety

```bash
# Create branch for risky changes
git checkout -b risky-refactor

# Make changes, commit
git add .
git commit -m "Try new approach"

# If works, merge back
git checkout main
git merge risky-refactor

# If fails, just delete branch
git checkout main
git branch -D risky-refactor
```

---

## Safety Rules

1. **Commit often** - after each working change
2. **Test before committing** - make sure it runs
3. **Use branches** - for experiments and AI suggestions
4. **Never commit .env** - already in .gitignore
5. **Push regularly** - backs up to cloud

---

## Undo Everything (Nuclear Option)

If everything is broken:

```bash
# See all commits
git log --oneline

# Find last working commit
# Then reset to it
git reset --hard <commit-hash>

# Or reset to last commit
git reset --hard HEAD
```

This is why Git is essential for AI coding - you can always undo.
