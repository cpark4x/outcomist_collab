#!/bin/bash
# Rename outcomist/ to webapp/ and consolidate docs
# Date: 2025-11-19

set -e  # Exit on any error

echo "🔄 Renaming outcomist/ to webapp/ for multi-platform clarity..."
echo ""

# Step 1: Verify we're in the right place
if [ ! -d "outcomist" ]; then
    echo "❌ Error: outcomist/ directory not found"
    echo "   Make sure you're running this from outcomist_collab/"
    exit 1
fi

if [ -d "webapp" ]; then
    echo "❌ Error: webapp/ directory already exists"
    exit 1
fi

echo "✅ Pre-flight checks passed"
echo ""

# Step 2: Rename the directory
echo "📁 Renaming outcomist/ → webapp/..."
mv outcomist webapp
echo "  ✓ Directory renamed"
echo ""

# Step 3: Consolidate docs
echo "📚 Consolidating documentation..."

# Move webapp-specific docs into main docs/
if [ -d "webapp/docs/user" ]; then
    mv webapp/docs/user docs/
    echo "  ✓ Moved docs/user/"
fi

if [ -d "webapp/docs/development" ]; then
    mv webapp/docs/development docs/
    echo "  ✓ Moved docs/development/"
fi

if [ -d "webapp/docs/project" ]; then
    # Merge with existing docs/planning or docs/specs if they exist
    if [ -d "docs/project" ]; then
        # Already exists from previous reorg, merge
        cp -r webapp/docs/project/* docs/project/ 2>/dev/null || true
        echo "  ✓ Merged docs/project/"
    else
        mv webapp/docs/project docs/
        echo "  ✓ Moved docs/project/"
    fi
fi

if [ -d "webapp/docs/testing" ]; then
    mv webapp/docs/testing docs/
    echo "  ✓ Moved docs/testing/"
fi

# Remove now-empty webapp/docs if it exists
if [ -d "webapp/docs" ]; then
    rm webapp/docs/README.md 2>/dev/null || true
    rmdir webapp/docs 2>/dev/null || true
    echo "  ✓ Cleaned up webapp/docs/"
fi

echo ""

# Step 4: Update file references
echo "🔧 Updating file references..."

# Update docker-compose.yml if it references "outcomist"
if [ -f "webapp/docker-compose.yml" ]; then
    if grep -q "outcomist" webapp/docker-compose.yml; then
        sed -i '' 's/outcomist/webapp/g' webapp/docker-compose.yml
        echo "  ✓ Updated webapp/docker-compose.yml"
    fi
fi

# Update Makefile if it exists
if [ -f "webapp/Makefile" ]; then
    if grep -q "outcomist" webapp/Makefile; then
        sed -i '' 's/outcomist/webapp/g' webapp/Makefile
        echo "  ✓ Updated webapp/Makefile"
    fi
fi

# Update README files
for readme in webapp/README.md webapp/*/README.md; do
    if [ -f "$readme" ] && grep -q "outcomist" "$readme"; then
        sed -i '' 's/outcomist/webapp/g' "$readme"
        echo "  ✓ Updated $readme"
    fi
done

# Update backend .env.example if it references paths
if [ -f "webapp/backend/.env.example" ]; then
    if grep -q "/outcomist/" webapp/backend/.env.example; then
        sed -i '' 's/\/outcomist\//\/webapp\//g' webapp/backend/.env.example
        echo "  ✓ Updated webapp/backend/.env.example"
    fi
fi

echo ""

# Step 5: Create main docs index
echo "📄 Creating unified docs index..."

cat > docs/README.md << 'EOF'
# Outcomist Documentation

Welcome to Outcomist documentation. This covers all platforms and components.

## 📱 For Users
- [User Guide](user/README.md) - Getting started with Outcomist
- [API Reference](user/API.md) - API documentation
- [Quickstart](user/QUICKSTART.md) - Quick setup guide

## 🛠 For Developers
- [Contributing](development/CONTRIBUTING.md) - How to contribute
- [Deployment](development/DEPLOYMENT.md) - Deployment guide
- [Streaming Architecture](development/STREAMING.md) - Real-time features

## 📋 Project Documentation
- [Vision](VISION.md) - Project vision and goals
- [Planning](planning/) - Project planning documents
- [Specs](specs/) - Technical specifications
- [Design Mockups](design-mockups/) - UI/UX designs
- [Changelog](project/CHANGELOG.md) - Version history
- [Project Status](project/PROJECT_COMPLETE.md) - Current status

## 🧪 Testing
- [E2E Test Matrix](testing/E2E_TEST_MATRIX.md) - End-to-end test plan

## 🏗 Architecture

### Current Platform: Web Application
Located in `/webapp/` - Full-stack web application with React frontend and Python backend.

### Future Platforms
- `/iosapp/` - Native iOS application (planned)
- `/desktopapp/` - Desktop application (Electron/Tauri) (planned)
- `/shared/` - Shared code and components (planned)

## 📝 Session History
See `/webapp/sessions/` for AI-assisted development session summaries.
EOF

echo "  ✓ Created unified docs/README.md"
echo ""

# Step 6: Create placeholder directories for future platforms
echo "🏗️ Creating placeholder directories for future platforms..."

mkdir -p shared/README.md
cat > shared/README.md << 'EOF'
# Shared Components

This directory will contain code shared across multiple Outcomist platforms:
- API client libraries
- Shared TypeScript types
- Reusable UI components
- Common utilities

## Structure (Planned)

```
shared/
├── api-client/     # API client for all platforms
├── types/          # TypeScript type definitions
├── components/     # Cross-platform UI components
└── utils/          # Common utilities
```

Status: Placeholder - will be populated as multi-platform development begins.
EOF

echo "  ✓ Created shared/ placeholder"
echo ""

# Step 7: Update root README if it exists
if [ -f "README.md" ]; then
    echo "📝 Updating root README..."
    if grep -q "outcomist/" README.md; then
        sed -i '' 's/outcomist\//webapp\//g' README.md
        echo "  ✓ Updated root README.md"
    fi
fi

echo ""

# Summary
echo "✅ Rename complete!"
echo ""
echo "📊 Changes made:"
echo "  - Renamed outcomist/ → webapp/"
echo "  - Consolidated all docs into /docs/"
echo "  - Updated file references"
echo "  - Created unified docs index"
echo "  - Created /shared/ placeholder"
echo ""
echo "📁 New structure:"
echo "  outcomist_collab/"
echo "    ├── docs/              (consolidated documentation)"
echo "    ├── webapp/            (web application)"
echo "    │   ├── backend/"
echo "    │   ├── frontend/"
echo "    │   ├── data/"
echo "    │   ├── logs/"
echo "    │   └── sessions/"
echo "    ├── shared/            (future: shared components)"
echo "    └── archive/"
echo ""
echo "🎯 Ready for:"
echo "  - Multi-platform development (iosapp/, desktopapp/)"
echo "  - Shared component library"
echo "  - E2E testing"
echo ""
echo "🚀 Next steps:"
echo "  1. Verify everything still works"
echo "  2. Run E2E tests"
echo "  3. Update any CI/CD configs if needed"
