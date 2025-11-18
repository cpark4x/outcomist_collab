# Outcomist User Guide

Complete guide to using Outcomist for AI-powered project creation and management.

## Table of Contents

- [Getting Started](#getting-started)
- [Interface Overview](#interface-overview)
- [Creating Projects](#creating-projects)
- [Working with AI Agents](#working-with-ai-agents)
- [Managing Files](#managing-files)
- [Project Types](#project-types)
- [Tips and Best Practices](#tips-and-best-practices)
- [Troubleshooting](#troubleshooting)

## Getting Started

### First Time Setup

1. **Launch Outcomist**
   - Open http://localhost:3000 in your browser
   - You'll see the onboarding welcome screen

2. **Complete Onboarding**
   - Read through the introduction
   - Learn about the interface layout
   - Understand the three views (Agent, Preview, Files)
   - Click "Get Started" when ready

3. **Create Your First Project**
   - Click the "+" button in the top-right corner
   - Choose a project type
   - Add a name and description
   - Start chatting with your AI agent

### System Requirements

- **Browser**: Modern browser (Chrome, Firefox, Safari, Edge)
- **Internet**: Active connection for AI responses
- **Screen**: Minimum 1280x720 resolution recommended
- **JavaScript**: Must be enabled

## Interface Overview

### Main Layout

The Outcomist interface consists of:

```
┌─────────────────────────────────────────────┐
│  Header: [Onboarding] [+]                  │
├─────────────────────────────────────────────┤
│                                             │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐    │
│  │ Project │  │ Project │  │ Project │    │
│  │   #1    │  │   #2    │  │   #3    │    │
│  │         │  │         │  │         │    │
│  └─────────┘  └─────────┘  └─────────┘    │
│                                             │
│  ┌─────────┐  ┌─────────┐                 │
│  │ Project │  │   Add   │                 │
│  │   #4    │  │   New   │                 │
│  │         │  │         │                 │
│  └─────────┘  └─────────┘                 │
│                                             │
└─────────────────────────────────────────────┘
```

### Project Card

Each project card shows:

```
┌───────────────────────────────┐
│ Project Name           [View] │  ← View selector
├───────────────────────────────┤
│                               │
│   Content area                │  ← Chat, preview, or files
│   (Agent/Preview/Files)       │
│                               │
├───────────────────────────────┤
│ [Message input...]      [Send]│  ← Message input (Agent view)
└───────────────────────────────┘
```

### View Selector

Three views available for each project:

- **Agent** 💬 - Chat interface with AI
- **Preview** 👁️ - Generated content display
- **Files** 📁 - File list and management

Click the view selector to switch between views.

## Creating Projects

### Step-by-Step

1. **Click the "+" button** in the top-right corner

2. **Choose project type:**
   - 🎮 **Game** - For game design and development
   - ✈️ **Trip** - For trip planning and itineraries
   - ✍️ **Content** - For blog posts, articles, marketing copy
   - 📊 **Presentation** - For slide decks and presentations

3. **Enter project details:**
   - **Name**: Clear, descriptive name (e.g., "Paris Vacation 2024")
   - **Description**: What you want to create (e.g., "7-day itinerary for family trip to Paris")

4. **Click "Create Project"**
   - Project card appears in the grid
   - AI agent is ready to chat
   - Initial session is automatically created

### Project Naming Tips

**Good names:**
- "Productivity App Prototype"
- "Blog Post: AI in Healthcare"
- "Tokyo 2024 Trip"
- "Sales Pitch Deck Q3"

**Avoid:**
- Generic names ("Project 1", "Test")
- Too long (keep under 40 characters)
- Special characters (stick to letters, numbers, spaces)

## Working with AI Agents

### Starting a Conversation

1. **Select Agent view** (💬 tab)

2. **Type your message** in the input box

3. **Click "Send"** or press Enter

4. **Watch the AI respond** in real-time
   - Messages stream in character by character
   - Files are generated automatically
   - System messages show file creation

### Message Types

**User Messages** (you):
- Appear on the right side
- Blue background
- Your instructions and questions

**Assistant Messages** (AI):
- Appear on the left side
- Gray background
- AI responses and suggestions

**System Messages** (automatic):
- Yellow background
- File creation notifications
- Status updates

### Conversation Flow

**Example conversation for a game:**

```
You: Create a simple maze game in JavaScript

AI: I'll create a browser-based maze game for you.
    Let me start with the HTML structure...

    [Creates: index.html]
    [Creates: game.js]
    [Creates: styles.css]

    I've created three files for your maze game:
    1. index.html - Main game page
    2. game.js - Game logic with collision detection
    3. styles.css - Styling for the maze

    To run it, open index.html in a browser...

You: Can you add a timer?

AI: I'll add a timer to track how long it takes
    to complete the maze...

    [Updates: game.js]

    I've updated game.js with a timer that starts
    when the player first moves...
```

### Best Practices for Prompts

**Be specific:**
- ❌ "Make a website"
- ✅ "Create a personal portfolio website with a hero section, about section, and project gallery"

**Provide context:**
- ❌ "Add a button"
- ✅ "Add a 'Download' button next to each project in the gallery"

**Ask for iterations:**
- "Can you make the text bigger?"
- "Change the color scheme to blue and white"
- "Add error handling for invalid input"

**Request explanations:**
- "Explain how the collision detection works"
- "What libraries are you using here?"
- "Walk me through the file structure"

## Managing Files

### Viewing Files

1. **Switch to Files view** (📁 tab)

2. **See all generated files:**
   - File name
   - File type (extension)
   - Creation date
   - File size

3. **Files are organized by:**
   - Newest first (by default)
   - All files for this project

### File Display

```
┌─────────────────────────────────┐
│ Files (4)                        │
├─────────────────────────────────┤
│ 📄 index.html                   │
│    Created: 2 minutes ago        │
│    Size: 2.4 KB                  │
├─────────────────────────────────┤
│ 📄 game.js                      │
│    Created: 2 minutes ago        │
│    Size: 5.1 KB                  │
├─────────────────────────────────┤
│ 📄 styles.css                   │
│    Created: 3 minutes ago        │
│    Size: 1.2 KB                  │
└─────────────────────────────────┘
```

### File Operations

Currently available:
- **View**: Switch to Preview view to see file content
- **List**: See all files in Files view

Coming soon:
- Download individual files
- Download all files as ZIP
- Edit files directly
- Delete files

### File Storage

- All files are saved to disk automatically
- Location: `backend/data/projects/[project-id]/`
- Files persist between sessions
- Backed up with database backups

## Project Types

Each project type has a specialized AI agent with specific expertise.

### 🎮 Game Projects

**Best for:**
- Browser-based games
- Game prototypes
- Interactive experiences
- Educational games

**Example prompts:**
- "Create a simple platformer game"
- "Make a memory card matching game"
- "Build a text-based adventure game"
- "Design a space shooter with levels"

**Typical outputs:**
- HTML structure
- JavaScript game logic
- CSS styling
- Asset placeholders
- README with instructions

### ✈️ Trip Projects

**Best for:**
- Vacation planning
- Multi-city itineraries
- Travel guides
- Budget planning

**Example prompts:**
- "Plan a 7-day trip to Japan"
- "Create a weekend getaway itinerary for San Francisco"
- "Build a budget breakdown for a Europe trip"
- "Suggest activities for a family trip to Orlando"

**Typical outputs:**
- Day-by-day itinerary
- Restaurant recommendations
- Budget spreadsheet
- Packing list
- Transportation options

### ✍️ Content Projects

**Best for:**
- Blog posts
- Articles
- Marketing copy
- Social media content
- Email campaigns

**Example prompts:**
- "Write a blog post about remote work trends"
- "Create social media posts for a product launch"
- "Draft an email campaign for Black Friday"
- "Write landing page copy for a SaaS product"

**Typical outputs:**
- Markdown or HTML content
- Multiple versions/lengths
- SEO metadata
- Call-to-action suggestions
- Image placement recommendations

### 📊 Presentation Projects

**Best for:**
- Slide decks
- Pitch presentations
- Educational content
- Business reports

**Example prompts:**
- "Create a pitch deck for a startup"
- "Build a quarterly business review presentation"
- "Make a training presentation on Git"
- "Design a product launch slide deck"

**Typical outputs:**
- Reveal.js HTML presentation
- Slide-by-slide content
- Speaker notes
- Visual suggestions
- Timing recommendations

## Tips and Best Practices

### Getting the Best Results

1. **Start with a clear goal**
   - Define what you want before starting
   - Break large projects into smaller pieces
   - Focus on one aspect at a time

2. **Iterate gradually**
   - Don't expect perfection on first try
   - Make incremental improvements
   - Test and refine

3. **Provide feedback**
   - Tell the AI what works and what doesn't
   - Ask for specific changes
   - Request explanations when confused

4. **Use context effectively**
   - Reference previous messages
   - Build on what's been created
   - Connect related ideas

### Workflow Patterns

**Pattern 1: Rapid Prototyping**
```
1. Describe the concept
2. Get initial version
3. Test it (Preview view)
4. Request improvements
5. Iterate until satisfied
```

**Pattern 2: Detailed Planning**
```
1. Discuss requirements in detail
2. Get outline or structure
3. Approve approach
4. Build section by section
5. Review and refine
```

**Pattern 3: Learning Mode**
```
1. Ask for explanation
2. Request simple example
3. Ask "how does this work?"
4. Request variations
5. Experiment with changes
```

### Multi-Project Workflows

**Parallel projects:**
- Work on multiple projects simultaneously
- Each has independent AI context
- Switch between projects freely
- Copy ideas between projects

**Sequential phases:**
- Use one project per phase
- E.g., "Planning", "Design", "Development"
- Cleaner organization
- Easier to reference history

**Template projects:**
- Create a well-defined project
- Use as reference for similar projects
- Consistent structure across projects

## Troubleshooting

### Common Issues

**AI not responding:**
- Check internet connection
- Verify backend is running
- Look for error messages in chat
- Try refreshing the page

**Messages appear slowly:**
- This is normal - responses stream in real-time
- Wait for complete response
- Check network speed

**Files not appearing:**
- Switch to Files view to see all files
- Refresh the view if needed
- Check that AI mentioned creating files
- Look for system messages

**Preview view is empty:**
- AI may not have created previewable content yet
- Try switching to Files view
- Ask AI to create specific content
- Some files (like JS) may not preview well

**Cannot create new project:**
- Check that you have API key configured
- Verify backend is running
- Try refreshing the page
- Check browser console for errors

### Error Messages

**"Failed to connect to API"**
- Backend is not running
- Start backend: `docker-compose up` or `uvicorn src.main:app`
- Check that port 8000 is accessible

**"API key not configured"**
- ANTHROPIC_API_KEY not set in .env
- Add key to backend/.env file
- Restart backend

**"Rate limit exceeded"**
- You've hit Anthropic's API rate limits
- Wait a few minutes
- Consider upgrading API plan

**"Invalid project type"**
- Programming error (should not happen)
- Try creating a new project
- Report as a bug

### Performance Tips

**Slow responses:**
- Simpler prompts generate faster
- Complex files take longer
- Multiple file creation is sequential
- Be patient with large projects

**High memory usage:**
- Browser may use significant memory with many projects
- Close unused projects
- Refresh page periodically
- Use fewer concurrent projects

**Laggy interface:**
- Disable browser extensions
- Close other tabs
- Increase browser memory limit
- Use a more powerful device

### Getting Help

**Debug steps:**
1. Check browser console for errors (F12)
2. Review backend logs: `docker-compose logs backend`
3. Verify environment variables are set
4. Try creating a minimal test project
5. Test with a simple prompt first

**Report issues:**
- Open GitHub issue with:
  - Steps to reproduce
  - Expected vs actual behavior
  - Browser and OS version
  - Screenshots if applicable
  - Console logs if relevant

## Keyboard Shortcuts

**In Agent view:**
- `Enter` - Send message
- `Shift+Enter` - New line in message
- `Escape` - Clear message input

**In any view:**
- `Ctrl/Cmd + K` - Focus on new message input
- `Tab` - Cycle through views
- `Ctrl/Cmd + R` - Refresh view

## Best Use Cases

### Great for Outcomist:
✅ Rapid prototyping
✅ Content creation
✅ Learning and experimenting
✅ Trip planning
✅ Presentation creation
✅ Game prototypes
✅ Code generation
✅ Idea exploration

### Consider other tools for:
❌ Production applications (without review)
❌ Complex enterprise systems
❌ Real-time collaboration
❌ Version control (use Git separately)
❌ Testing and CI/CD
❌ Database management

## What's Next?

After mastering the basics:

1. **Explore all project types** - Each has unique capabilities
2. **Experiment with prompts** - Learn what works best
3. **Build progressively** - Start simple, add complexity
4. **Share your work** - Export files and deploy
5. **Provide feedback** - Help improve Outcomist

## Appendix

### File Types by Project Type

**Game projects:**
- `.html` - Game page structure
- `.js` - Game logic
- `.css` - Styling
- `.json` - Game data
- `.md` - Documentation

**Trip projects:**
- `.md` - Itinerary and guides
- `.csv` - Budget and expenses
- `.json` - Structured data
- `.html` - Formatted output

**Content projects:**
- `.md` - Blog posts and articles
- `.html` - Formatted content
- `.txt` - Plain text drafts
- `.json` - Metadata

**Presentation projects:**
- `.html` - Reveal.js slides
- `.md` - Slide content
- `.css` - Custom styling
- `.json` - Presentation config

### Example Project Ideas

**Games:**
- Snake game
- Tic-tac-toe
- Quiz app
- Memory game
- Platformer
- Puzzle game

**Trips:**
- Week in Paris
- Italy road trip
- Japan in 2 weeks
- Weekend getaway
- Honeymoon planning
- Budget backpacking

**Content:**
- Product launch announcement
- How-to guide
- Case study
- Newsletter
- Social media campaign
- Landing page copy

**Presentations:**
- Startup pitch deck
- Quarterly review
- Training materials
- Product demo
- Conference talk
- Project proposal

### Resources

- [API Documentation](API.md)
- [Deployment Guide](DEPLOYMENT.md)
- [GitHub Repository](https://github.com/your-repo)
- [Claude Documentation](https://docs.anthropic.com/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [React Docs](https://react.dev/)

---

**Happy creating with Outcomist! 🚀**
