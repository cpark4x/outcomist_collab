#!/bin/bash
# Outcomist Directory Reorganization Script
# Date: 2025-11-19

set -e  # Exit on any error

echo "🧹 Starting Outcomist directory reorganization..."
echo ""

# Step 1: Create new directory structure
echo "📁 Creating new directories..."
mkdir -p docs/user
mkdir -p docs/development
mkdir -p docs/project
mkdir -p docs/testing
mkdir -p sessions
mkdir -p logs

echo "✅ Directories created"
echo ""

# Step 2: Move user documentation
echo "📚 Moving user documentation..."
if [ -f "docs/USER_GUIDE.md" ]; then
    mv docs/USER_GUIDE.md docs/user/README.md
    echo "  ✓ USER_GUIDE.md -> docs/user/README.md"
fi

if [ -f "docs/API.md" ]; then
    mv docs/API.md docs/user/
    echo "  ✓ API.md -> docs/user/"
fi

if [ -f "backend/QUICKSTART.md" ]; then
    mv backend/QUICKSTART.md docs/user/
    echo "  ✓ QUICKSTART.md -> docs/user/"
fi

echo ""

# Step 3: Move development documentation
echo "🔧 Moving development documentation..."
if [ -f "CONTRIBUTING.md" ]; then
    mv CONTRIBUTING.md docs/development/
    echo "  ✓ CONTRIBUTING.md -> docs/development/"
fi

if [ -f "docs/DEPLOYMENT.md" ]; then
    mv docs/DEPLOYMENT.md docs/development/
    echo "  ✓ DEPLOYMENT.md -> docs/development/"
fi

if [ -f "backend/STREAMING.md" ]; then
    mv backend/STREAMING.md docs/development/
    echo "  ✓ STREAMING.md -> docs/development/"
fi

echo ""

# Step 4: Move project documentation
echo "📋 Moving project documentation..."
if [ -f "CHANGELOG.md" ]; then
    mv CHANGELOG.md docs/project/
    echo "  ✓ CHANGELOG.md -> docs/project/"
fi

if [ -f "PHASE1_COMPLETE.md" ]; then
    mv PHASE1_COMPLETE.md docs/project/
    echo "  ✓ PHASE1_COMPLETE.md -> docs/project/"
fi

if [ -f "PROJECT_COMPLETE.md" ]; then
    mv PROJECT_COMPLETE.md docs/project/
    echo "  ✓ PROJECT_COMPLETE.md -> docs/project/"
fi

if [ -f "DEPLOYMENT_SUMMARY.md" ]; then
    mv DEPLOYMENT_SUMMARY.md docs/project/
    echo "  ✓ DEPLOYMENT_SUMMARY.md -> docs/project/"
fi

if [ -f "DOCKER_DEPLOYMENT_COMPLETE.md" ]; then
    mv DOCKER_DEPLOYMENT_COMPLETE.md docs/project/
    echo "  ✓ DOCKER_DEPLOYMENT_COMPLETE.md -> docs/project/"
fi

if [ -f "frontend/PHASE3_COMPLETE.md" ]; then
    mv frontend/PHASE3_COMPLETE.md docs/project/
    echo "  ✓ frontend/PHASE3_COMPLETE.md -> docs/project/"
fi

echo ""

# Step 5: Move testing documentation
echo "🧪 Moving testing documentation..."
if [ -f "E2E_TEST_MATRIX.md" ]; then
    mv E2E_TEST_MATRIX.md docs/testing/
    echo "  ✓ E2E_TEST_MATRIX.md -> docs/testing/"
fi

echo ""

# Step 6: Move session summaries
echo "📝 Moving session summaries..."
if [ -f "SESSION_SUMMARY.md" ]; then
    mv SESSION_SUMMARY.md sessions/2025-11-19-verification-attempt.md
    echo "  ✓ SESSION_SUMMARY.md -> sessions/2025-11-19-verification-attempt.md"
fi

if [ -f "DEBUGGING_SESSION_SUMMARY.md" ]; then
    mv DEBUGGING_SESSION_SUMMARY.md sessions/2025-11-19-verification-debug.md
    echo "  ✓ DEBUGGING_SESSION_SUMMARY.md -> sessions/2025-11-19-verification-debug.md"
fi

if [ -f "backend/IMAGE_MIME_FIX_SUMMARY.md" ]; then
    mv backend/IMAGE_MIME_FIX_SUMMARY.md sessions/2025-11-18-image-validation.md
    echo "  ✓ IMAGE_MIME_FIX_SUMMARY.md -> sessions/2025-11-18-image-validation.md"
fi

echo ""

# Step 7: Move logs
echo "📋 Moving logs..."
if [ -f "frontend.log" ]; then
    mv frontend.log logs/
    echo "  ✓ frontend.log -> logs/"
fi

if [ -f "backend/backend.log" ]; then
    mv backend/backend.log logs/
    echo "  ✓ backend/backend.log -> logs/"
fi

if [ -f "backend/backend_fresh.log" ]; then
    mv backend/backend_fresh.log logs/
    echo "  ✓ backend/backend_fresh.log -> logs/"
fi

# Create logs .gitignore
cat > logs/.gitignore << 'EOF'
# Ignore all log files
*.log
*.log.*

# Keep this .gitignore
!.gitignore
EOF
echo "  ✓ Created logs/.gitignore"

echo ""

# Step 8: Create index README files
echo "📄 Creating index files..."

# docs/README.md
cat > docs/README.md << 'EOF'
# Outcomist Documentation

## User Documentation
- [User Guide](user/README.md) - Getting started and usage
- [API Reference](user/API.md) - API endpoints and usage
- [Quickstart](user/QUICKSTART.md) - Quick setup guide

## Development Documentation
- [Contributing](development/CONTRIBUTING.md) - How to contribute
- [Deployment](development/DEPLOYMENT.md) - Deployment guide
- [Streaming](development/STREAMING.md) - Streaming architecture

## Project Documentation
- [Changelog](project/CHANGELOG.md) - Version history
- [Project Completion](project/PROJECT_COMPLETE.md) - Completion status
- [Deployment Summary](project/DEPLOYMENT_SUMMARY.md) - Deployment notes

## Testing Documentation
- [E2E Test Matrix](testing/E2E_TEST_MATRIX.md) - End-to-end test plan
EOF
echo "  ✓ Created docs/README.md"

# sessions/README.md
cat > sessions/README.md << 'EOF'
# AI Session History

This directory contains summaries of AI-assisted development sessions.

## Sessions

### 2025-11-19
- [Verification Debug](2025-11-19-verification-debug.md) - Fixed verification integration issues
- [Verification Attempt](2025-11-19-verification-attempt.md) - Initial verification implementation

### 2025-11-18
- [Image Validation](2025-11-18-image-validation.md) - Added image MIME type validation

## Format

Each session file includes:
- Date and goal
- What was attempted
- What succeeded/failed
- Test evidence
- Lessons learned
- Quality assessment
EOF
echo "  ✓ Created sessions/README.md"

# logs/README.md
cat > logs/README.md << 'EOF'
# Application Logs

This directory contains runtime logs from the backend and frontend services.

## Log Files

- `backend.log` - Backend API server logs
- `frontend.log` - Frontend development server logs

## Log Rotation

Logs are rotated automatically by the application. Old logs are compressed and archived.

## Viewing Logs

```bash
# View recent backend logs
tail -f logs/backend.log

# View recent frontend logs
tail -f logs/frontend.log

# Search logs
grep "ERROR" logs/backend.log
```

## Note

All `.log` files are gitignored. Logs are for local development only.
EOF
echo "  ✓ Created logs/README.md"

echo ""

# Step 9: Move the reorganization proposal and script to docs
echo "🗂️ Archiving reorganization files..."
if [ -f "PROPOSED_REORGANIZATION.md" ]; then
    mv PROPOSED_REORGANIZATION.md docs/project/REORGANIZATION_PLAN.md
    echo "  ✓ PROPOSED_REORGANIZATION.md -> docs/project/REORGANIZATION_PLAN.md"
fi

echo ""

# Step 10: Summary
echo "✅ Reorganization complete!"
echo ""
echo "📊 Summary:"
echo "  - Created 7 new directories"
echo "  - Moved ~15 documentation files"
echo "  - Moved 3 session summaries"
echo "  - Moved 3 log files"
echo "  - Created 3 index README files"
echo ""
echo "📁 New structure:"
echo "  docs/"
echo "    ├── user/           (3 files)"
echo "    ├── development/    (3 files)"
echo "    ├── project/        (6 files)"
echo "    └── testing/        (1 file)"
echo "  sessions/             (3 files)"
echo "  logs/                 (3 files + .gitignore)"
echo ""
echo "🎉 Ready for clean E2E testing!"
