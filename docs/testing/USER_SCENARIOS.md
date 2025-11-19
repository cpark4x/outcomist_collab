# User Scenarios - Outcomist Testing

**Purpose**: Test scenarios based on real user profiles with specific needs
**Status**: DRAFT
**Last Updated**: 2025-11-19

---

## Overview

Three distinct user profiles with different technical abilities, goals, and expectations. Each profile represents a different relationship with technology and different success criteria for Outcomist.

---

## User Profile 1: Charlotte (Age 9) - Instant Gratification Creator

### Profile Summary

**Demographics**:
- Age: 9 years old
- Tech Experience: Beginner (no mouse, limited computer knowledge)
- Input Method: Keyboard only, touch/trackpad
- Patience Level: Low - wants immediate results
- Learning Style: Learn by playing, not by troubleshooting

**Key Characteristics**:
- Creative and imaginative
- Wants to see creation process (build progress visibility)
- Needs time estimates (how long until done?)
- Zero tolerance for bugs - must work immediately
- Wants simple customizations through natural language
- "Fire and forget" approach - make it, play it, done

### Success Criteria

✅ **Must Have**:
- Game works 100% on first try (no debugging needed)
- Visible progress during creation ("Building your game: 2 of 5 steps...")
- Clear time estimate ("About 3 minutes remaining...")
- Simple, immediate results (can start playing right away)
- Easy customizations via chat ("Make the blocks bigger", "Change colors to pink")

❌ **Deal Breakers**:
- Any bugs or errors requiring troubleshooting
- Unclear progress or waiting without feedback
- Complex iteration process
- Technical error messages
- Need for mouse or complex controls

### Test Scenarios

#### Scenario C1: Simple Tetris Game - Happy Path

**Initial Request**:
```
"I want to make a Tetris game where I can play with colorful blocks"
```

**Expected Experience**:
1. **Immediate feedback**: "Great! I'm creating your Tetris game. This will take about 3 minutes."
2. **Progress visibility**: Progress bar showing "Building game board (1/5)", "Adding colorful blocks (2/5)", etc.
3. **Time updates**: "About 2 minutes remaining..."
4. **Completion**: "Your game is ready! Click 'Play Now' to start."
5. **It works**: Game loads, keyboard controls work (arrow keys), no errors

**Follow-up Customization**:
```
"Make the blocks bigger and change the colors to rainbow"
```

**Expected**: Quick update (< 1 minute), progress shown, game still works perfectly

**Success Metrics**:
- Game works on first try: ✅/❌
- Progress visible throughout: ✅/❌
- Time estimate accurate (within 30 seconds): ✅/❌
- Keyboard controls work: ✅/❌
- Customization applied correctly: ✅/❌
- No errors in console: ✅/❌

---

#### Scenario C2: Catching Dinosaurs Game

**Initial Request**:
```
"I want a game where I catch dinosaurs by clicking on them and get points"
```

**Expected Experience**:
1. Outcomist shows progress: "Creating your dinosaur game..."
2. Progress steps visible: "Drawing dinosaurs (1/4)", "Adding click detection (2/4)", etc.
3. Time estimate: "About 2 minutes remaining"
4. Completion: "Your dinosaur game is ready!"
5. Game works: Dinosaurs appear, clicking them adds points, score displays

**Follow-up Customization**:
```
"Make the dinosaurs move faster and add sound when I catch them"
```

**Expected**: Updates smoothly, sound added, game still works

**Success Metrics**:
- Dinosaurs clickable: ✅/❌
- Score increments correctly: ✅/❌
- No JavaScript errors: ✅/❌
- Sound customization works: ✅/❌
- Still playable after changes: ✅/❌

---

#### Scenario C3: Edge Case - Vague Request

**Initial Request**:
```
"Make me a fun game"
```

**Expected Experience**:
1. Outcomist asks clarifying questions: "What kind of game do you like? Do you want to catch things, stack things, or solve puzzles?"
2. Charlotte responds: "Catch things!"
3. Outcomist proceeds with specific game creation
4. Shows progress and time estimate
5. Game works immediately

**Success Metrics**:
- System handles vague request gracefully: ✅/❌
- Clarifying questions age-appropriate: ✅/❌
- Final game works: ✅/❌

---

## User Profile 2: Mason (Age 12) - Patient Builder

### Profile Summary

**Demographics**:
- Age: 12 years old
- Tech Experience: Intermediate (willing to learn)
- Input Method: Mouse + keyboard comfortable
- Patience Level: High - willing to work on projects over time
- Learning Style: Curious, asks questions, builds incrementally

**Key Characteristics**:
- Wants to show off complex projects to friends
- Willing to iterate and learn
- Interested in school-related functionality
- Comfortable with longer build times
- Wants to understand how things work
- Willing to troubleshoot with guidance

### Success Criteria

✅ **Must Have**:
- Support for complex, multi-feature apps
- Ability to build incrementally (add features over time)
- Educational explanations when asked
- Guidance for learning and improvement
- Can show progress to friends (shareable)

✨ **Nice to Have**:
- Suggestions for improvements
- "How does this work?" explanations
- Version history (see changes over time)
- Export options (share with friends)

### Test Scenarios

#### Scenario M1: T-Shirt Store - Multi-Session Build

**Initial Request**:
```
"I want to make an online store where I can sell t-shirts with cool designs"
```

**Expected Experience - Session 1**:
1. Outcomist: "Great project! An online store is complex. Let's start with the basics. Should we begin with the product gallery or the shopping cart?"
2. Mason: "Product gallery"
3. Outcomist builds gallery with sample t-shirts
4. Shows progress, takes ~5 minutes
5. Mason plays with it, discovers limitations

**Expected Experience - Session 2** (same day or later):
```
Mason: "Can we add a shopping cart so people can buy shirts?"
```
1. Outcomist: "Sure! I'll add a cart that stores selected items. This will take about 4 minutes."
2. Builds cart functionality
3. Integrates with existing gallery
4. Mason tests, everything still works

**Expected Experience - Session 3**:
```
Mason: "How do I add my own t-shirt designs?"
```
1. Outcomist explains: "You can add images by uploading them. Let me add an admin section where you can manage products."
2. Builds admin interface
3. Shows Mason how to use it
4. Mason successfully adds custom designs

**Success Metrics**:
- Handles complex request appropriately: ✅/❌
- Breaks project into manageable pieces: ✅/❌
- Previous work preserved between sessions: ✅/❌
- New features integrate smoothly: ✅/❌
- Educational explanations provided: ✅/❌
- Mason can customize independently: ✅/❌

---

#### Scenario M2: Homework Helper App

**Initial Request**:
```
"I need an app to help me track my homework assignments and due dates"
```

**Expected Experience**:
1. Outcomist: "Let's build a homework tracker! Should it include calendar view, reminders, or just a simple list?"
2. Mason: "Start with a list, but I want to add reminders later"
3. Outcomist builds task list with due dates
4. Mason uses it, finds it helpful
5. Later asks: "Can you add notifications for when homework is due soon?"
6. Outcomist adds notification feature
7. Mason asks: "How does the notification system work?"
8. Outcomist explains in age-appropriate detail

**Success Metrics**:
- Practical functionality works: ✅/❌
- Iterative development supported: ✅/❌
- Educational explanations clear: ✅/❌
- Mason understands the concepts: ✅/❌

---

#### Scenario M3: Edge Case - Overly Ambitious Request

**Initial Request**:
```
"I want to build a multiplayer online game like Fortnite where players can battle each other"
```

**Expected Experience**:
1. Outcomist: "That's an ambitious project! A full multiplayer game would take professional teams months to build. Let's start with something simpler that has similar elements. How about a turn-based battle game where two players can play on the same computer?"
2. Mason: "Okay, that sounds good"
3. Outcomist builds turn-based battle game
4. Works well, Mason enjoys it
5. Mason: "Can we make it so my friend can play from their computer?"
6. Outcomist: "That requires a server, which is more advanced. Let's work toward that goal. First, let me explain what we'd need..."

**Success Metrics**:
- Manages expectations appropriately: ✅/❌
- Offers achievable alternative: ✅/❌
- Builds working foundation: ✅/❌
- Explains limitations clearly: ✅/❌
- Provides learning path: ✅/❌

---

## User Profile 3: Laura (Age 46) - Social Media Manager

### Profile Summary

**Demographics**:
- Age: 46 years old
- Tech Experience: Intermediate (comfortable with apps, not coding)
- Use Case: Social media content management
- Patience Level: Medium - wants efficiency, not perfection
- Work Style: Collaborative brainstorming and automation

**Key Characteristics**:
- Uses social media heavily (knows platforms well)
- Wants to brainstorm content ideas with AI
- Needs organization and scheduling tools
- Values automation for repetitive tasks
- Wants a "durable" place to manage everything
- Willing to learn new tools if they save time

### Success Criteria

✅ **Must Have**:
- Content brainstorming assistant
- Organization system (calendar, drafts, categories)
- Automation for posting/scheduling
- Platform-specific formatting
- Persistent workspace (not losing work)

✨ **Nice to Have**:
- Analytics and insights
- Content library (reuse past content)
- A/B testing ideas
- Multi-platform support

### Test Scenarios

#### Scenario L1: Content Calendar Creation

**Initial Request**:
```
"I want to create a content calendar for my social media accounts where I can plan posts and schedule them"
```

**Expected Experience**:
1. Outcomist: "I'll create a content calendar for you! Which platforms do you use? (Instagram, Facebook, Twitter/X, LinkedIn, TikTok)"
2. Laura: "Instagram and Facebook"
3. Outcomist builds calendar interface with:
   - Monthly/weekly views
   - Platform-specific fields (image, caption, hashtags)
   - Draft/scheduled/published states
   - Visual preview
4. Takes ~4 minutes
5. Laura starts planning posts

**Follow-up Session**:
```
Laura: "Can you help me brainstorm content ideas for next week?"
```
1. Outcomist: "Sure! What topics or themes are you focusing on?"
2. Laura: "Healthy recipes and meal prep tips"
3. Outcomist suggests 10 post ideas with captions
4. Laura selects 3, adds them to calendar
5. Works smoothly

**Success Metrics**:
- Calendar functional and intuitive: ✅/❌
- Platform-specific features work: ✅/❌
- Brainstorming generates useful ideas: ✅/❌
- Content saved persistently: ✅/❌
- Easy to edit and update: ✅/❌

---

#### Scenario L2: Automated Posting Assistant

**Initial Request**:
```
"I want to automate my posting schedule so I don't have to manually post every day"
```

**Expected Experience**:
1. Outcomist explains: "I can help you prepare posts, but actual automation to social platforms requires their APIs. Let's build a system that helps you manage and track posts efficiently."
2. Laura: "That works. Can it remind me when posts are due?"
3. Outcomist builds:
   - Scheduling system with reminders
   - "Post now" quick actions
   - Copy-to-clipboard for captions
   - Image download links
4. Laura uses it, finds it saves time

**Follow-up**:
```
Laura: "Can you add hashtag suggestions based on my content?"
```
1. Outcomist adds hashtag generator
2. Analyzes post content, suggests relevant hashtags
3. Laura can accept/modify/reject suggestions
4. Works smoothly

**Success Metrics**:
- Automation within realistic limits: ✅/❌
- Reminders work reliably: ✅/❌
- Workflow more efficient than before: ✅/❌
- Hashtag suggestions relevant: ✅/❌
- Laura uses it consistently: ✅/❌

---

#### Scenario L3: Content Analytics Dashboard

**Initial Request**:
```
"I want to see which of my posts perform best so I can make better content"
```

**Expected Experience**:
1. Outcomist: "I can create a dashboard where you track post performance! You'll need to input metrics manually from your platforms, or we can set up automatic tracking if you have access to their APIs."
2. Laura: "I'll input manually for now"
3. Outcomist builds:
   - Post performance tracker
   - Charts (likes, comments, shares over time)
   - Top-performing content highlights
   - Content type analysis (videos vs images vs text)
4. Laura tracks posts, sees patterns

**Follow-up**:
```
Laura: "Based on my data, can you suggest what types of posts I should focus on?"
```
1. Outcomist analyzes data
2. Provides insights: "Your video posts get 3x more engagement than images. Posts on Tuesdays perform 40% better than weekends."
3. Suggests strategy adjustments
4. Laura implements recommendations

**Success Metrics**:
- Dashboard visually clear: ✅/❌
- Data input straightforward: ✅/❌
- Analytics insights actionable: ✅/❌
- Recommendations data-driven: ✅/❌
- Helps Laura improve results: ✅/❌

---

## Cross-Cutting Test Scenarios

These scenarios test behaviors across all user types:

### Scenario X1: System Failure Recovery

**Situation**: Backend crashes mid-build

**Charlotte's Experience**:
- Shows clear error: "Oops! Something went wrong. Let me try again."
- Automatically retries
- If retry fails: "I'm having trouble. Let's try a simpler version."
- Charlotte never sees technical errors

**Mason's Experience**:
- Shows error with context: "Build interrupted. I've saved your progress."
- Offers options: "Resume build" or "Start fresh"
- Mason can choose, work is preserved

**Laura's Experience**:
- Shows error with save confirmation: "Connection lost. Your work is saved."
- Auto-resumes on reconnection
- No data loss, continues smoothly

---

### Scenario X2: Unclear Request

**Charlotte**: "Make something cool"
- System asks: "What's your favorite game? Do you like catching things, building things, or solving puzzles?"

**Mason**: "I want to build an app"
- System asks: "What should the app do? Who will use it? What problem does it solve?"

**Laura**: "Help me with social media"
- System asks: "What aspect of social media? Content creation, scheduling, analytics, or brainstorming?"

---

### Scenario X3: Performance Under Load

**Test**: All three users using Outcomist simultaneously

**Expected**:
- Each user's progress tracked independently
- No interference between sessions
- Response times remain reasonable
- No one loses work or experiences errors

---

## Testing Matrix Summary

| User | Total Scenarios | Must Pass | Priority |
|------|----------------|-----------|----------|
| Charlotte (Age 9) | 3 | 3 (100% success rate required) | HIGH |
| Mason (Age 12) | 3 | 2 (flexibility on ambitious requests) | MEDIUM |
| Laura (Age 46) | 3 | 3 (workflow efficiency critical) | HIGH |
| Cross-cutting | 3 | 3 (system reliability) | CRITICAL |

**Total Test Scenarios**: 12

---

## Success Criteria by User

### Charlotte (Zero-Tolerance Profile)
- **100% success rate** on happy path scenarios
- **Zero errors** visible to user
- **Progress visibility** always present
- **Time estimates** within 30 seconds of actual
- **Keyboard-only** controls work perfectly

### Mason (Learning Profile)
- **80%+ success rate** (some failures acceptable with good error handling)
- **Educational value** in interactions
- **Incremental progress** preserved between sessions
- **Complex requests** handled with appropriate guidance

### Laura (Efficiency Profile)
- **90%+ workflow efficiency** improvement over manual methods
- **Data persistence** guaranteed
- **Brainstorming quality** meets professional standards
- **Time-saving** automation works reliably

---

## Next Steps

1. **User approval** on scenario design
2. **Execute Charlotte scenarios first** (highest priority, strictest requirements)
3. **Document results** with video/screenshots
4. **Iterate based on findings**
5. **Execute Mason and Laura scenarios**
6. **Validate cross-cutting behaviors**

**Awaiting approval to proceed with testing...**
