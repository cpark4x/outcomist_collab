# Outcomist

AI-powered multi-project workspace for working on multiple projects simultaneously with specialized AI agents.

## ✨ Features

- 🎯 **Multi-Project Workspace** - Work on multiple projects simultaneously in a grid layout
- 🤖 **Specialized AI Agents** - Each project has a dedicated AI agent for specific tasks (game design, trip planning, content creation, presentations)
- 🔄 **Real-time Streaming** - See AI responses as they're generated with Server-Sent Events
- 👁️ **Dual Views** - Toggle between Agent (chat), Preview (output), and Files views
- 📁 **File Generation** - AI automatically creates and updates files in real-time
- 🎮 **Project Types** - Games, trips, content, presentations with specialized prompts
- 💾 **Persistent Storage** - All projects and conversations saved to SQLite database
- 🎨 **Modern UI** - Clean, responsive interface built with React and TailwindCSS

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Anthropic API key ([get one here](https://console.anthropic.com/))

### Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd outcomist
   ```

2. **Set up environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your ANTHROPIC_API_KEY
   ```

3. **Start the application**
   ```bash
   docker-compose up -d
   ```

4. **Open in browser**
   ```
   http://localhost:3000
   ```

5. **View logs** (optional)
   ```bash
   docker-compose logs -f
   ```

6. **Stop the application**
   ```bash
   docker-compose down
   ```

### Local Development

**Backend:**
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env
uvicorn src.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## 📖 Usage

1. **First Visit** - Complete the onboarding flow to understand the interface
2. **Create Projects** - Click "+" to add a new project with:
   - Project type (game, trip, content, presentation)
   - Name and description
3. **Chat with AI** - Send messages to your specialized agent
4. **Watch It Build** - AI generates files in real-time as you chat
5. **Preview Output** - Toggle to Preview view to see generated content
6. **Manage Files** - Switch to Files view to see all project files

## 🏗️ Architecture

- **Backend**: FastAPI + SQLAlchemy + SQLite + Claude API (Anthropic)
- **Frontend**: React + TypeScript + TailwindCSS + Vite
- **Real-time**: Server-Sent Events (SSE) for streaming
- **Storage**: SQLite database + file system for generated files

## 📂 Project Structure

```
outcomist/
├── backend/              # FastAPI backend
│   ├── src/
│   │   ├── api/         # REST API endpoints
│   │   ├── services/    # Business logic layer
│   │   ├── ai/          # Claude AI integration
│   │   ├── database/    # SQLAlchemy models
│   │   └── main.py      # FastAPI app entry
│   ├── data/            # SQLite DB + generated files
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/            # React frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── hooks/       # Custom hooks
│   │   ├── api/         # API client
│   │   └── App.tsx      # Main app component
│   ├── package.json
│   ├── Dockerfile
│   └── nginx.conf
├── docs/                # Documentation
│   ├── DEPLOYMENT.md
│   ├── USER_GUIDE.md
│   └── API.md
├── docker-compose.yml
└── README.md
```

## 📚 Documentation

- [Deployment Guide](docs/DEPLOYMENT.md) - Docker, cloud deployment, scaling
- [User Guide](docs/USER_GUIDE.md) - Complete usage instructions
- [API Documentation](docs/API.md) - REST API and SSE event reference
- [Backend README](backend/README.md) - Backend architecture details
- [Frontend README](frontend/README.md) - Frontend component structure

## 🔧 Configuration

Environment variables (in `.env` file):

- `ANTHROPIC_API_KEY` (required) - Your Claude API key
- `DATABASE_URL` (optional) - SQLite database path, defaults to `sqlite:///./data/database.sqlite`
- `DATA_DIR` (optional) - Project files directory, defaults to `./data/projects`
- `LOG_LEVEL` (optional) - Logging level (debug, info, warning, error), defaults to `info`

## 🗄️ Data Persistence

All data is stored in the `./data` directory:
- `database.sqlite` - All projects, sessions, messages, and files metadata
- `projects/` - Generated files organized by project

**Important**: Backup this directory regularly in production!

## 🚢 Deployment

### Quick Deploy with Docker

```bash
docker-compose up -d
```

### Cloud Deployment Options

- **Railway** - Deploy both services with automatic GitHub integration
- **Fly.io** - Deploy with `fly launch` and `fly deploy`
- **Vercel** (Frontend) + **Railway** (Backend) - Deploy services separately
- **AWS/GCP/Azure** - Deploy with container services (ECS, Cloud Run, Container Apps)

See [Deployment Guide](docs/DEPLOYMENT.md) for detailed instructions.

## 🧪 Development

**Run tests:**
```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm test
```

**Check types:**
```bash
# Frontend
cd frontend
npm run type-check
```

**Format code:**
```bash
# Backend
cd backend
black src/
isort src/

# Frontend
cd frontend
npm run format
```

## 🤝 Contributing

Contributions welcome! This is an MVP, so there's plenty of room for improvement:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- Built with [Claude](https://www.anthropic.com/claude) by Anthropic
- UI inspired by modern project management tools
- Special thanks to the FastAPI and React communities

## 📧 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check the [User Guide](docs/USER_GUIDE.md)
- Review the [API Documentation](docs/API.md)

---

**Made with ❤️ for building amazing things with AI**
