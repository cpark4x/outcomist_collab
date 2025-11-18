# Outcomist Collab

**Exploration:** Solving the hard parts of AI-first collaboration

---

## What This Is

An exploration of how to fix fundamental collaboration breakdowns between humans and AI. This may become:
- A separate product
- A feature of Outcomist
- A set of conventions for the Amplifier project
- A methodology we document and share

**Status:** Research and design phase (as of 2025-11-12)

---

## The Problem

We identified **19 collaboration breakdowns** that occur when humans work with AI, grouped into **4 root causes:**

1. **No Persistent Context Layer** - AI forgets everything between sessions
2. **No Shared Thinking Workspace** - AI's reasoning is invisible
3. **Late Discovery of Constraints** - Problems surface during execution, not planning
4. **Unclear Collaboration Protocol** - Implicit expectations cause friction

**Read the human story:** [docs/product_story.md](docs/product_story.md)

---

## The Solution Hypothesis

**Simple file-based architecture** that provides:

1. **Persistent Context** - Files that remember across sessions
2. **Visible Thinking** - Workspaces where AI documents reasoning
3. **Discovery Protocol** - Checklist for upfront constraint exploration
4. **Collaboration Contract** - Explicit modes and expectations

**Key insight:** This is NOT a tooling problem requiring CLI infrastructure. It's a convention and context management problem solvable with files + protocols.

---

## Research Foundation

Solution informed by leading AI-first teams:
- **Anthropic:** 2-10x productivity gains with persistent context
- **Amplifier:** 25+ specialized sub-agents with pre-loaded context
- **Manus:** Planning → Execution → Verification separation
- **Claude-Flow:** 84.8% SWE-Bench solve rate with specialized modes

**Full research:** `outcomist/ai_working/research_synthesizer/output/ai_first_teams_comprehensive_research.md`

---

## Current Status

### Completed
✅ Problem analysis (19 breakdowns identified)
✅ Root cause analysis (reduced to 4 core issues)
✅ Research synthesis (10 web searches, 6+ companies analyzed)
✅ Architecture design (minimal 4-component solution)
✅ Product story (humanized the pain points)
✅ Agent consultation (zen-architect, amplifier-cli-architect)

### Next Steps
🔲 Decision: Separate product vs. Outcomist feature?
🔲 Phase 1 implementation (file structure + templates)
🔲 Test with 5 real sessions
🔲 Capture learnings and iterate

---

## Project Structure

```
outcomist_collab/
├── README.md                          # This file
├── docs/
│   └── product_story.md               # Narrative humanizing the problems
├── ai_working/
│   └── session_2025_11_12_analysis.md # Today's analysis and decisions
├── .claude/                           # (Future) Context files
└── templates/                         # (Future) Template files
```

---

## Key Documents

1. **[Product Story](docs/product_story.md)** - Read this first to understand the human impact
2. **[Session Analysis](ai_working/session_2025_11_12_analysis.md)** - Complete breakdown of today's research and decisions
3. **[AI-First Teams Research](../outcomist/ai_working/research_synthesizer/output/ai_first_teams_comprehensive_research.md)** - Full research synthesis

---

## Philosophy Alignment

This exploration follows Amplifier principles:

✅ **Ruthless Simplicity** - Files not infrastructure, conventions not tools
✅ **Trust in Emergence** - Start minimal, let patterns reveal themselves
✅ **Present-Moment Focus** - Solve current problems, not hypothetical futures
✅ **Research-Backed** - Leverage proven patterns from leading teams

---

## Open Questions

1. **Product vs. Feature?**
   - Standalone collaboration tool?
   - Outcomist enhancement?
   - General methodology for Amplifier projects?

2. **Scope**
   - Just conventions and files?
   - Eventually CLI tools?
   - Integration with Claude Code features?

3. **Testing Strategy**
   - Internal use first?
   - Public beta?
   - Documentation-first approach?

4. **Relationship to Existing Patterns**
   - How does this relate to CLAUDE.md, AGENTS.md, DISCOVERIES.md?
   - Project-specific vs. global conventions?
   - Per-user customization?

---

## What Makes This Different

**vs. Just Using AI:**
- ✅ Context persists between sessions
- ✅ Reasoning is visible and reviewable
- ✅ Constraints discovered before building
- ✅ Collaboration expectations explicit

**vs. Building Complex Tools:**
- ✅ Start with files (no infrastructure)
- ✅ Conventions over automation
- ✅ Progressive enhancement path
- ✅ Leverages existing Claude Code features

**vs. Industry Solutions:**
- ✅ Combines patterns from multiple leading teams
- ✅ Addresses gaps research doesn't cover (cross-session persistence)
- ✅ Human-centric design (read the product story first)
- ✅ Ruthlessly simple starting point

---

## Success Criteria

After 5-10 sessions using this approach:

**Quantitative:**
- Fewer misunderstandings about expectations
- Earlier discovery of constraints (planning vs. execution)
- Reduced rework from missed context
- Less time explaining background

**Qualitative:**
- Context feels continuous across sessions
- AI reasoning visible when needed
- Collaboration expectations clear
- Discoveries compound over time

---

## Timeline

- **Week 1:** Decision on approach + Phase 1 implementation
- **Weeks 2-3:** Real-world testing + iteration
- **Week 4+:** Evaluate if CLI tools are needed

---

## Contributing

This is currently a solo exploration by Chris Park with AI assistance. As the approach solidifies, contribution guidelines will be added.

---

## Contact

Chris Park - [GitHub](https://github.com/chrispark) (if applicable)

---

**Last Updated:** 2025-11-12
**Status:** Research & Design Phase
**Next Milestone:** Decision on implementation approach
