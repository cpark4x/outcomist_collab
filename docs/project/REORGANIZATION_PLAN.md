# Outcomist Directory Reorganization Proposal

## Current Problems

1. **Documentation scattered**: Root has 10+ .md files mixed together
2. **Session summaries at root**: Should be in dedicated folder
3. **Logs at root**: `frontend.log` shouldn't be at project root
4. **Unclear hierarchy**: Hard to find what you need

## Proposed Structure

```
outcomist/
├── README.md                          # Main entry point
├── LICENSE
├── Makefile                          # Top-level commands
├── docker-compose.yml
├── docker-test.sh
│
├── docs/                             # All documentation
│   ├── user/                         # User-facing docs
│   │   ├── README.md                 # User guide
│   │   ├── API.md
│   │   └── QUICKSTART.md
│   │
│   ├── development/                  # Developer docs
│   │   ├── CONTRIBUTING.md
│   │   ├── DEPLOYMENT.md
│   │   └── STREAMING.md
│   │
│   ├── project/                      # Project management
│   │   ├── CHANGELOG.md
│   │   ├── PHASE1_COMPLETE.md
│   │   ├── PROJECT_COMPLETE.md
│   │   └── DEPLOYMENT_SUMMARY.md
│   │
│   └── testing/                      # Testing documentation
│       ├── E2E_TEST_MATRIX.md
│       └── test-scenarios/           # Individual test scenarios
│
├── sessions/                         # AI/debugging sessions
│   ├── 2025-11-19-verification-debug.md
│   ├── 2025-11-18-image-validation.md
│   └── README.md                     # Index of sessions
│
├── data/                             # Runtime data
│   ├── projects/                     # User project files
│   └── .gitkeep
│
├── logs/                             # Application logs
│   ├── backend.log
│   ├── frontend.log
│   ├── .gitignore                    # Ignore all logs
│   └── README.md                     # Log rotation info
│
├── backend/                          # Backend application
│   ├── src/
│   ├── tests/
│   ├── data/
│   ├── README.md
│   ├── pyproject.toml
│   └── ...
│
└── frontend/                         # Frontend application
    ├── src/
    ├── public/
    ├── README.md
    ├── package.json
    └── ...
```

## Migration Plan

### Step 1: Create new directories
```bash
mkdir -p docs/{user,development,project,testing}
mkdir -p sessions
mkdir -p logs
```

### Step 2: Move documentation files

**User docs**:
```bash
mv docs/USER_GUIDE.md docs/user/README.md
mv docs/API.md docs/user/
mv backend/QUICKSTART.md docs/user/
```

**Development docs**:
```bash
mv CONTRIBUTING.md docs/development/
mv docs/DEPLOYMENT.md docs/development/
mv backend/STREAMING.md docs/development/
```

**Project docs**:
```bash
mv CHANGELOG.md docs/project/
mv PHASE1_COMPLETE.md docs/project/
mv PROJECT_COMPLETE.md docs/project/
mv DEPLOYMENT_SUMMARY.md docs/project/
mv DOCKER_DEPLOYMENT_COMPLETE.md docs/project/
mv frontend/PHASE3_COMPLETE.md docs/project/
```

**Testing docs**:
```bash
mv E2E_TEST_MATRIX.md docs/testing/
```

### Step 3: Move session summaries
```bash
mv SESSION_SUMMARY.md sessions/2025-11-19-verification-attempt.md
mv DEBUGGING_SESSION_SUMMARY.md sessions/2025-11-19-verification-debug.md
mv backend/IMAGE_MIME_FIX_SUMMARY.md sessions/2025-11-18-image-validation.md
```

### Step 4: Organize logs
```bash
mv frontend.log logs/
mv backend/backend.log logs/
mv backend/backend_fresh.log logs/
echo "*.log" > logs/.gitignore
```

### Step 5: Update README files

Create index files:
- `docs/README.md` - Documentation index
- `sessions/README.md` - Session history index
- `logs/README.md` - Log information

### Step 6: Update references

Search and update any hardcoded paths in:
- docker-compose.yml
- Makefile
- README.md files
- Import statements (if any reference docs)

## Benefits

1. **Clear hierarchy**: Easy to find user docs vs dev docs vs sessions
2. **Clean root**: Only essential files at root level
3. **Searchable history**: All sessions in one place with dates
4. **Git-friendly**: Logs directory properly ignored
5. **Scalable**: Easy to add new categories

## Questions for You

1. **Approve this structure?** Any changes you want?
2. **Execute the migration?** Should I run these commands?
3. **Timing**: Do this now or after E2E testing is done?

## Automated Migration Script

I can create a script that:
```bash
#!/bin/bash
# reorganize.sh - Automate the reorganization

# Step 1: Create directories
mkdir -p docs/{user,development,project,testing}
mkdir -p sessions
mkdir -p logs

# Step 2-4: Move files with verification
# (detailed script with each mv command and validation)

# Step 5: Create index files
# (generate README.md files)

# Step 6: Update references
# (sed commands to update paths)

echo "✅ Reorganization complete"
```

**Want me to create this script and execute it?**
