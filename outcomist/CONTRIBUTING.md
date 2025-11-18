# Contributing to Outcomist

Thank you for your interest in contributing to Outcomist! This is an MVP project with plenty of room for improvement.

## Getting Started

1. **Fork the repository**
2. **Clone your fork**
   ```bash
   git clone https://github.com/yourusername/outcomist.git
   cd outcomist
   ```

3. **Set up development environment**
   ```bash
   # Backend
   cd backend
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   cp .env.example .env
   # Add your ANTHROPIC_API_KEY

   # Frontend
   cd ../frontend
   npm install
   ```

4. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Workflow

### Backend

**Run the server:**
```bash
cd backend
source .venv/bin/activate
uvicorn src.main:app --reload
```

**Run tests:**
```bash
pytest
```

**Format code:**
```bash
black src/
isort src/
```

**Type checking:**
```bash
mypy src/
```

### Frontend

**Run dev server:**
```bash
cd frontend
npm run dev
```

**Run tests:**
```bash
npm test
```

**Type checking:**
```bash
npm run type-check
```

**Format code:**
```bash
npm run format
```

## Code Style

### Python
- Use Black for formatting (line length 88)
- Use isort for import sorting
- Type hints required
- Docstrings for all functions
- Follow PEP 8

### TypeScript/React
- Use Prettier for formatting
- Functional components with hooks
- TypeScript strict mode
- Props interfaces for all components

## Commit Messages

Use conventional commits:

```
feat: add user authentication
fix: resolve SSE connection issue
docs: update API documentation
refactor: simplify file service
test: add project creation tests
```

## Pull Request Process

1. **Update documentation** if needed
2. **Add tests** for new features
3. **Ensure all tests pass**
4. **Update CHANGELOG.md** (if exists)
5. **Create a pull request** with clear description

**PR template:**
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests added
- [ ] All tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-reviewed code
- [ ] Commented complex code
- [ ] Updated documentation
```

## Areas for Contribution

### High Priority

- [ ] **Authentication system** - JWT or session-based
- [ ] **Rate limiting** - Per-user API limits
- [ ] **Database migration** - SQLite to PostgreSQL
- [ ] **File download** - ZIP all project files
- [ ] **Project templates** - Pre-configured project starters
- [ ] **Search functionality** - Search projects and messages
- [ ] **Export/Import** - Project backup and restore

### Medium Priority

- [ ] **Dark mode** - Theme switching
- [ ] **Keyboard shortcuts** - Power user features
- [ ] **Mobile optimization** - Responsive improvements
- [ ] **Undo/Redo** - For file operations
- [ ] **Collaborative editing** - Multi-user projects
- [ ] **Project sharing** - Public project links
- [ ] **Analytics** - Usage statistics

### Nice to Have

- [ ] **Browser extension** - Quick access
- [ ] **Desktop app** - Electron wrapper
- [ ] **CLI tool** - Command-line interface
- [ ] **API client libraries** - Python, JS, etc.
- [ ] **Webhook integrations** - GitHub, Slack, etc.
- [ ] **Custom AI models** - Beyond Claude
- [ ] **Plugin system** - Extensibility

## Bug Reports

**Use GitHub Issues with this template:**

```markdown
**Describe the bug**
A clear description of the bug

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior**
What should happen

**Screenshots**
If applicable

**Environment**
- OS: [e.g. macOS 14.0]
- Browser: [e.g. Chrome 120]
- Version: [e.g. 0.1.0]

**Additional context**
Any other information
```

## Feature Requests

**Use GitHub Issues with this template:**

```markdown
**Feature Description**
Clear description of the feature

**Problem It Solves**
What problem does this address?

**Proposed Solution**
How should it work?

**Alternatives Considered**
Other approaches you've thought about

**Additional Context**
Screenshots, mockups, examples
```

## Code of Conduct

### Our Standards

- Be respectful and inclusive
- Accept constructive criticism
- Focus on what's best for the project
- Show empathy towards others

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or insulting comments
- Personal or political attacks
- Publishing others' private information

## Questions?

- Open a GitHub Discussion
- Check existing issues
- Review documentation

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to Outcomist! 🚀**
