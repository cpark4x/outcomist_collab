#!/bin/bash
# Autonomous Agent Web App - Quick Start Script
# Run this to set up the entire frontend in one command

set -e  # Exit on error

echo "🚀 Setting up Autonomous Agent Web App..."

# 1. Install dependencies
echo "📦 Installing dependencies..."
npm install

# 2. Install additional dependencies
echo "📦 Installing UI libraries..."
npm install @tanstack/react-query zustand react-router-dom
npm install -D tailwindcss postcss autoprefixer
npm install lucide-react class-variance-authority clsx tailwind-merge

# 3. Initialize Tailwind
echo "🎨 Setting up Tailwind CSS..."
npx tailwindcss init -p

# 4. Install Shadcn/ui components (will be added manually)
echo "✨ Shadcn/ui will be configured in tsconfig and components will be added manually"

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Review the component files in src/"
echo "  2. Run: npm run dev"
echo "  3. Open: http://localhost:5173"
echo ""
