#!/bin/bash
# Quick test script for Docker deployment

set -e

echo "🧪 Testing Outcomist Docker Deployment"
echo "======================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found"
    echo "   Creating from .env.example..."
    cp .env.example .env
    echo "   ⚠️  Please add your ANTHROPIC_API_KEY to .env file"
    echo "   Then run this script again"
    exit 1
fi

# Check if ANTHROPIC_API_KEY is set
if ! grep -q "ANTHROPIC_API_KEY=sk-" .env; then
    echo "⚠️  ANTHROPIC_API_KEY not configured in .env"
    echo "   Please add your API key and run again"
    exit 1
fi

echo "✅ Environment file configured"
echo ""

# Build images
echo "🔨 Building Docker images..."
docker-compose build

echo ""
echo "✅ Images built successfully"
echo ""

# Start services
echo "🚀 Starting services..."
docker-compose up -d

echo ""
echo "⏳ Waiting for services to be healthy..."
sleep 5

# Check backend health
echo "🏥 Checking backend health..."
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend is healthy"
else
    echo "❌ Backend health check failed"
    echo "   Check logs: docker-compose logs backend"
    docker-compose down
    exit 1
fi

# Check frontend
echo "🏥 Checking frontend..."
if curl -f http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ Frontend is accessible"
else
    echo "❌ Frontend check failed"
    echo "   Check logs: docker-compose logs frontend"
    docker-compose down
    exit 1
fi

echo ""
echo "🎉 All tests passed!"
echo ""
echo "📍 Outcomist is running at:"
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "📝 Useful commands:"
echo "   View logs:  docker-compose logs -f"
echo "   Stop:       docker-compose down"
echo "   Restart:    docker-compose restart"
echo ""
echo "✨ Ready to create amazing projects!"
