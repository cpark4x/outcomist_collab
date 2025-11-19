# E2E User Experience Tests - What Users Actually See and Do

**Purpose**: Test the actual user experience - what they see, click, and experience
**Focus**: UI/UX validation, not just API testing
**Last Updated**: 2025-11-19

---

## Testing Philosophy

❌ **NOT THIS**: "API returns 200, test passes"
✅ **THIS**: "Charlotte clicks the button, sees her game, plays it, and it works"

**Every test must**:
1. **Open the actual UI** in a browser (http://localhost:5173)
2. **Click real buttons** that users click
3. **See real feedback** that users see
4. **Verify it actually works** from user perspective

---

## Test Execution Template

For each scenario:

```markdown
### Test: [User] - [What They Want to Do]

**User opens**: http://localhost:3000
**User sees**: [screenshot or description of what's on screen]
**User clicks**: [exact button/element they click]
**User types**: [exact text they type]
**User sees feedback**: [what appears on screen]
**User verifies**: [how they know it worked]

**PASS if**: User successfully accomplished their goal
**FAIL if**: User got stuck, confused, or saw errors
```

---

## Charlotte (Age 9) - Zero Tolerance Tests

### Test C1: Create Simple Tetris Game

**Goal**: Charlotte wants to make a Tetris game and play it immediately

#### Step-by-Step User Journey

**1. Charlotte opens Outcomist**
- Opens: http://localhost:3000 in browser
- **SEES**: Welcome screen or project list
- **VERIFIES**: Page loads, no errors visible

**2. Charlotte creates new project**
- **CLICKS**: "New Project" or "Create Game" button
- **SEES**: Modal/form asking for details
- **TYPES**: Project name: "My Tetris Game"
- **TYPES**: Prompt: "I want to make a Tetris game where I can play with colorful blocks"
- **CLICKS**: "Create" or "Start Building" button
- **VERIFIES**: Modal closes, taken to project view

**3. Charlotte watches it build**
- **SEES**: Progress indicator showing:
  - "Creating your Tetris game..."
  - Progress bar moving
  - Steps like "Building game board (1/5)"
  - Time estimate: "About 3 minutes remaining..."
- **VERIFIES**:
  - Progress updates visible (not stuck)
  - Time counts down
  - No error messages
  - Can see it's doing something

**4. Charlotte sees completion**
- **SEES**:
  - "Your game is ready!" message
  - "Play Now" button appears
  - Preview thumbnail (if available)
- **VERIFIES**: Status changed from building to complete

**5. Charlotte plays the game**
- **CLICKS**: "Play Now" or "Open Game" button
- **SEES**: Game opens (new tab or iframe)
- **VERIFIES**:
  - Game loads (not blank page)
  - No error messages in game
  - Game board visible
  - Colorful blocks visible

**6. Charlotte interacts with game**
- **PRESSES**: Arrow keys on keyboard
- **SEES**: Blocks move in response
- **PRESSES**: Down arrow (or spacebar)
- **SEES**: Block drops
- **VERIFIES**:
  - Keyboard controls work
  - Blocks move correctly
  - Game is actually playable
  - No freezing or glitches

**7. Charlotte customizes**
- **GOES BACK**: To Outcomist (closes game tab/iframe)
- **TYPES**: In chat: "Make the blocks bigger and change the colors to rainbow"
- **CLICKS**: Send button
- **SEES**:
  - "Updating your game..." message
  - Progress indicator (shorter this time)
  - "Done! Your game is updated" message
- **CLICKS**: "Play Now" again
- **SEES**: Game with bigger blocks and rainbow colors
- **VERIFIES**: Changes actually applied

#### Pass/Fail Criteria

**✅ PASS if ALL of these are true**:
- [ ] Charlotte successfully created project through UI
- [ ] Charlotte saw progress updates (not stuck waiting)
- [ ] Charlotte saw time estimate that made sense
- [ ] Charlotte's game loaded when clicking "Play Now"
- [ ] Charlotte could play game with keyboard (arrow keys worked)
- [ ] Charlotte saw NO error messages at any point
- [ ] Charlotte's customization request worked
- [ ] Whole process felt smooth and clear

**❌ FAIL if ANY of these happen**:
- [ ] UI button didn't work or did nothing
- [ ] Progress got stuck with no updates
- [ ] Game didn't load (blank page, 404, error)
- [ ] Keyboard controls didn't work in game
- [ ] Charlotte saw technical error messages
- [ ] Customization didn't apply or broke game
- [ ] Charlotte got confused about what to do next

---

### Test C2: Dinosaur Catching Game

**Goal**: Charlotte wants to make a game where she catches dinosaurs

#### Step-by-Step User Journey

**1-2. [Same as C1 steps 1-2, but different prompt]**
- **TYPES**: "I want a game where I catch dinosaurs by clicking on them and get points"

**3-4. [Same as C1 steps 3-4]**
- Watches build, sees completion

**5. Charlotte plays dinosaur game**
- **CLICKS**: "Play Now"
- **SEES**:
  - Game with dinosaurs on screen
  - Score display showing "Score: 0" or similar
  - Dinosaurs moving or stationary

**6. Charlotte catches dinosaurs**
- **CLICKS**: On a dinosaur
- **SEES**:
  - Dinosaur disappears or reacts
  - Score increases: "Score: 1"
  - New dinosaur appears (or next one)
- **CLICKS**: Several more dinosaurs
- **VERIFIES**:
  - Each click registers
  - Score increases each time
  - Game is fun/playable

**7. Charlotte adds sound**
- **TYPES**: "Make the dinosaurs move faster and add sound when I catch them"
- **SEES**: Update in progress
- **CLICKS**: "Play Now" after update
- **CLICKS**: On dinosaur
- **HEARS**: Sound plays (if audio working)
- **SEES**: Dinosaurs move faster than before
- **VERIFIES**: Both changes applied

#### Pass/Fail Criteria

**✅ PASS if**:
- [ ] Dinosaurs appeared on screen
- [ ] Clicking dinosaurs worked (detected clicks)
- [ ] Score increased with each catch
- [ ] Game was actually playable and fun
- [ ] Updates applied correctly (faster movement, sound)
- [ ] Charlotte never saw errors

**❌ FAIL if**:
- [ ] Dinosaurs didn't appear or render incorrectly
- [ ] Clicks didn't register
- [ ] Score didn't update
- [ ] Game crashed or froze
- [ ] Updates broke the game

---

### Test C3: Vague Request Handling

**Goal**: Charlotte says "Make me a fun game" (unclear request)

#### Step-by-Step User Journey

**1-2. [Same as C1 steps 1-2]**
- **TYPES**: "Make me a fun game"
- **CLICKS**: Create

**3. Charlotte gets clarifying questions**
- **SEES**: Instead of immediate building, sees questions:
  - "What kind of game do you like?"
  - Options shown: "Catch things" | "Stack things" | "Solve puzzles"
  - OR: Text suggestions in chat
- **VERIFIES**: System recognized unclear request and asked for help

**4. Charlotte clarifies**
- **CLICKS**: "Catch things" option
  - OR **TYPES**: "Catch things!"
- **SEES**: System confirms: "Great! I'll make a catching game for you"
- **SEES**: Now proceeds with building

**5-7. [Same as C1 steps 3-6]**
- Watches build, sees completion, plays game, verifies it works

#### Pass/Fail Criteria

**✅ PASS if**:
- [ ] System detected vague request
- [ ] Charlotte saw clear, simple questions
- [ ] Questions were age-appropriate (not technical)
- [ ] Charlotte could easily respond
- [ ] After clarification, game built successfully
- [ ] Final game matched what Charlotte wanted

**❌ FAIL if**:
- [ ] System built random game without asking
- [ ] Questions were confusing or technical
- [ ] Charlotte got stuck not knowing how to answer
- [ ] Final game didn't match Charlotte's choice

---

## Mason (Age 12) - Patient Builder Tests

### Test M1: T-Shirt Store (Multi-Session)

**Goal**: Mason wants to build an online store, working on it over time

#### Session 1: Initial Build

**1-2. [Same setup as Charlotte]**
- **TYPES**: "I want to make an online store where I can sell t-shirts with cool designs"

**3. Mason gets guidance**
- **SEES**: Message like:
  - "An online store is complex! Let's start with the basics."
  - "Should we begin with the product gallery or shopping cart?"
  - Options presented clearly
- **VERIFIES**: System breaks down complex request

**4. Mason chooses starting point**
- **CLICKS**: "Product gallery" option OR **TYPES**: "Product gallery"
- **SEES**: "I'll build a product gallery for your t-shirts"

**5-6. [Watches build and sees completion]**

**7. Mason explores the store**
- **CLICKS**: "Open Store"
- **SEES**:
  - Grid of sample t-shirts
  - Product images
  - Prices
  - "Add to Cart" buttons (maybe grayed out/non-functional yet)
- **CLICKS**: Around the interface
- **VERIFIES**: Gallery works, looks like a store

**8. Mason closes for today**
- **CLOSES**: Store preview
- **VERIFIES**: Can leave and come back later

#### Session 2: Adding Shopping Cart (Later That Day or Next Day)

**1. Mason returns**
- **OPENS**: http://localhost:3000
- **SEES**: Project list with "My T-Shirt Store"
- **CLICKS**: On project to open it
- **VERIFIES**: Previous work still there

**2. Mason adds feature**
- **TYPES**: "Can we add a shopping cart so people can buy shirts?"
- **SEES**: "Sure! I'll add a cart. This will take about 4 minutes."

**3-4. [Watches build]**

**5. Mason tests cart**
- **CLICKS**: "Open Store"
- **SEES**: Cart icon or section now visible
- **CLICKS**: "Add to Cart" on a t-shirt
- **SEES**:
  - Item appears in cart
  - Cart count increases
  - Can view cart
- **CLICKS**: "Checkout" or "View Cart"
- **SEES**: Selected items listed
- **VERIFIES**: Cart functionality works, integrates with existing gallery

#### Session 3: Admin Features

**1. Mason asks question**
- **TYPES**: "How do I add my own t-shirt designs?"

**2. Mason gets explanation + implementation**
- **SEES**:
  - Explanation: "You can upload images. I'll add an admin section for you."
  - Building starts

**3. Mason uses admin section**
- **CLICKS**: "Admin" link/button in store
- **SEES**:
  - File upload interface
  - Form for product details (name, price, description)
  - List of current products
- **CLICKS**: "Upload Image"
- **UPLOADS**: A sample image file
- **FILLS**: Product form (name, price)
- **CLICKS**: "Add Product"
- **SEES**: New product appears in admin list

**4. Mason verifies in store**
- **CLICKS**: Back to store front
- **SEES**: His custom t-shirt in gallery
- **VERIFIES**: Custom product actually works

#### Pass/Fail Criteria

**✅ PASS if**:
- [ ] Mason successfully started complex project with guidance
- [ ] System broke down request into manageable pieces
- [ ] Mason could return to project later (persistence works)
- [ ] New features integrated with existing work (nothing broke)
- [ ] Mason could add custom content through UI
- [ ] Mason received educational explanations when asked
- [ ] Multi-session workflow felt natural

**❌ FAIL if**:
- [ ] System tried to build everything at once (overwhelming)
- [ ] Mason lost work between sessions
- [ ] Adding new features broke existing ones
- [ ] Admin interface was confusing or broken
- [ ] Custom content didn't appear in store
- [ ] Mason got stuck without guidance

---

### Test M2: Homework Tracker

**Goal**: Mason wants to track homework, iterate over time

#### Initial Build

**1-2. [Standard setup]**
- **TYPES**: "I need an app to help me track my homework assignments and due dates"

**3. Mason gets clarification**
- **SEES**: "Let's build a homework tracker! Should it include calendar view, reminders, or just a simple list?"
- **TYPES**: "Start with a list, but I want to add reminders later"

**4-6. [Watches build, completion]**

**7. Mason uses tracker**
- **CLICKS**: "Open App"
- **SEES**:
  - List interface
  - "Add Assignment" button
  - Empty state or sample data
- **CLICKS**: "Add Assignment"
- **SEES**: Form with fields:
  - Assignment name
  - Subject/class
  - Due date picker
  - Notes (optional)
- **FILLS**: Form:
  - Name: "Math Chapter 5 homework"
  - Subject: "Math"
  - Due: Tomorrow's date
- **CLICKS**: "Add" or "Save"
- **SEES**: Assignment appears in list with due date

**8. Mason adds more assignments**
- **ADDS**: 3-4 more assignments with different dates
- **SEES**: List grows, sorted by due date
- **VERIFIES**: Can see all homework in one place

#### Iteration: Adding Reminders

**1. Mason requests feature**
- **TYPES**: "Can you add notifications for when homework is due soon?"

**2-3. [Watches build]**

**4. Mason tests reminders**
- **SEES**: New UI for reminder settings
- **CLICKS**: On an assignment
- **SEES**: Option to set reminder ("1 day before", "2 hours before", etc.)
- **SELECTS**: "1 day before"
- **SAVES**: Assignment
- **VERIFIES**: Reminder setting saved

**5. Mason asks educational question**
- **TYPES**: "How does the notification system work?"
- **SEES**: Age-appropriate explanation in chat:
  - "The app checks your homework due dates"
  - "When a due date is close, it shows a notification"
  - "You can customize when you want reminders"
- **VERIFIES**: Explanation was clear and helpful

#### Pass/Fail Criteria

**✅ PASS if**:
- [ ] Tracker interface was intuitive to use
- [ ] Mason could add/edit/delete assignments easily
- [ ] Due dates displayed clearly
- [ ] Iterative feature addition worked smoothly
- [ ] New features integrated without breaking existing
- [ ] Educational explanations were clear and helpful
- [ ] Mason felt he understood the app better

**❌ FAIL if**:
- [ ] Interface was confusing or hard to use
- [ ] Adding assignments was cumbersome
- [ ] Due dates didn't save or display correctly
- [ ] New features broke existing functionality
- [ ] Explanations were too technical or unclear
- [ ] Mason felt lost or frustrated

---

### Test M3: Overly Ambitious Request

**Goal**: Mason asks for something unrealistic, system guides appropriately

#### User Journey

**1-2. [Standard setup]**
- **TYPES**: "I want to build a multiplayer online game like Fortnite where players can battle each other"

**3. Mason gets realistic guidance**
- **SEES**: Message like:
  - "That's an ambitious project! Full multiplayer games take professional teams months."
  - "Let's start with something simpler that has similar elements."
  - "How about a turn-based battle game where two players can play on the same computer?"
  - Options: "Yes, let's try that" | "Tell me more" | "Different idea"
- **VERIFIES**: System didn't just say "no", but offered alternative

**4. Mason accepts alternative**
- **CLICKS**: "Yes, let's try that" OR **TYPES**: "Okay, that sounds good"

**5-7. [Watches build, plays game]**
- Game builds successfully
- Two-player turn-based battle works
- Mason enjoys it despite being simpler than original request

**8. Mason asks about multiplayer**
- **TYPES**: "Can we make it so my friend can play from their computer?"
- **SEES**: Educational explanation:
  - "That requires a server, which is more advanced."
  - "Here's what we'd need: [simple explanation]"
  - "Let me know if you want to learn more about that!"
- **VERIFIES**: System explained limitation without shutting down curiosity

#### Pass/Fail Criteria

**✅ PASS if**:
- [ ] System recognized unrealistic request
- [ ] System offered achievable alternative
- [ ] Alternative was genuinely similar/appealing
- [ ] Mason understood why and wasn't frustrated
- [ ] Simpler game still worked and was fun
- [ ] System provided learning opportunity
- [ ] Mason felt respected, not dismissed

**❌ FAIL if**:
- [ ] System tried to build impossible request (set false expectations)
- [ ] System just said "no" without alternative
- [ ] Alternative was too different from request
- [ ] Mason felt talked down to or discouraged
- [ ] Explanations were too technical
- [ ] Mason lost interest or trust

---

## Laura (Age 46) - Social Media Manager Tests

### Test L1: Content Calendar

**Goal**: Laura wants to plan and organize social media posts

#### Initial Build

**1-2. [Standard setup]**
- **TYPES**: "I want to create a content calendar for my social media accounts where I can plan posts and schedule them"

**3. Laura chooses platforms**
- **SEES**: "I'll create a content calendar! Which platforms do you use?"
- **SEES**: Checkboxes or buttons: Instagram | Facebook | Twitter/X | LinkedIn | TikTok
- **CLICKS**: Instagram and Facebook checkboxes
- **CLICKS**: "Continue" or "Create Calendar"

**4-6. [Watches build]**

**7. Laura uses calendar**
- **CLICKS**: "Open Calendar"
- **SEES**:
  - Month/week view toggle
  - Days of the month
  - Empty slots for posts
  - "Add Post" button
- **CLICKS**: On a future date (e.g., next Tuesday)
- **SEES**: Post creation modal with:
  - Platform selector (Instagram/Facebook)
  - Image upload area
  - Caption field
  - Hashtag field
  - Save as draft / Schedule options

**8. Laura creates a post**
- **SELECTS**: Instagram
- **UPLOADS**: Sample image
- **TYPES**: Caption: "Healthy breakfast bowl 🥗 #healthyeating #breakfast"
- **CLICKS**: "Save as Draft"
- **SEES**:
  - Modal closes
  - Post appears on calendar on selected date
  - Visual preview of post
- **VERIFIES**: Post saved to calendar

**9. Laura views post details**
- **CLICKS**: On saved post in calendar
- **SEES**:
  - Full post preview
  - Edit / Delete options
  - Platform indicator
  - Scheduled time
- **CLICKS**: "Edit"
- **CHANGES**: Caption slightly
- **SAVES**: Changes
- **VERIFIES**: Changes saved

#### Brainstorming Session

**1. Laura asks for help**
- **TYPES**: "Can you help me brainstorm content ideas for next week?"

**2. Laura provides context**
- **SEES**: "Sure! What topics or themes are you focusing on?"
- **TYPES**: "Healthy recipes and meal prep tips"
- **SEES**: Thinking indicator (if applicable)

**3. Laura gets suggestions**
- **SEES**: List of 8-10 post ideas like:
  - "Monday meal prep: 5 breakfasts in 30 minutes"
  - "Budget-friendly healthy lunch ideas"
  - "Healthy snack alternatives for busy professionals"
  - [etc.]
- Each idea is clickable or has "Add to Calendar" button

**4. Laura adds ideas**
- **CLICKS**: "Add to Calendar" on 3 ideas she likes
- **SEES**: Date picker for each
- **SELECTS**: Dates (Mon, Wed, Fri)
- **CONFIRMS**: Selections
- **SEES**: Ideas now appear on calendar as drafts
- **VERIFIES**: Brainstormed ideas successfully added

#### Pass/Fail Criteria

**✅ PASS if**:
- [ ] Calendar interface was intuitive and professional
- [ ] Laura could easily create posts through UI
- [ ] Image uploads worked
- [ ] Posts appeared correctly on calendar
- [ ] Editing posts worked smoothly
- [ ] Brainstorming suggestions were relevant and useful
- [ ] Suggestions could be added to calendar easily
- [ ] Laura felt the tool saved time vs manual planning

**❌ FAIL if**:
- [ ] Calendar was confusing or cluttered
- [ ] Creating posts was tedious or unclear
- [ ] Image uploads failed or broken
- [ ] Posts didn't save or display correctly
- [ ] Brainstorming suggestions were generic or unhelpful
- [ ] Couldn't easily add suggestions to calendar
- [ ] Laura felt tool was more work than benefit

---

### Test L2: Posting Workflow

**Goal**: Laura wants efficient posting workflow with reminders

#### Setup Automation

**1-2. [Standard setup, Laura has existing calendar]**
- **TYPES**: "I want to automate my posting schedule so I don't have to manually post every day"

**3. Laura gets realistic explanation**
- **SEES**:
  - "I can help you prepare posts efficiently! Actual automation to social platforms requires their APIs."
  - "Let's build a system that helps you manage and track posts efficiently."
  - "It can remind you when posts are due and make copying/posting super quick."
- **TYPES**: "That works. Can it remind me when posts are due?"
- **SEES**: "Yes! I'll add reminders and quick-post features."

**4-6. [Watches build]**

**7. Laura sees new features**
- **OPENS**: Calendar
- **SEES**:
  - Posts now have "Reminder" toggle
  - "Post Now" button on each scheduled post
  - Notification bell icon (if reminders enabled)

**8. Laura sets up reminder**
- **CLICKS**: On tomorrow's post
- **TOGGLES**: "Remind me" switch on
- **SELECTS**: Reminder time: "9:00 AM" (morning of post day)
- **SAVES**: Settings
- **VERIFIES**: Reminder indicator on post

**9. Laura uses quick-post feature**
- **CLICKS**: "Post Now" on a drafted post
- **SEES**: Modal with:
  - Post preview
  - "Copy Caption" button
  - "Download Image" button
  - Checklist: "✓ Image downloaded" "✓ Caption copied" "☐ Posted"
- **CLICKS**: "Copy Caption"
- **SEES**: "Caption copied to clipboard!" confirmation
- **CLICKS**: "Download Image"
- **SEES**: Image downloads to computer
- **VERIFIES**: Has everything needed to post to social media

**10. Laura marks as posted**
- **GOES TO**: Instagram (separate tab/app)
- **PASTES**: Caption
- **UPLOADS**: Image
- **POSTS**: On Instagram
- **RETURNS TO**: Calendar
- **CLICKS**: Checkbox "Posted" on the post
- **SEES**: Post marked as completed/published
- **VERIFIES**: Tracking works

#### Hashtag Suggestions

**1. Laura requests feature**
- **TYPES**: "Can you add hashtag suggestions based on my content?"

**2-3. [Watches build]**

**4. Laura tests hashtags**
- **CREATES**: New post about "smoothie recipes"
- **TYPES**: Caption: "Easy green smoothie recipe for busy mornings"
- **CLICKS**: "Suggest Hashtags" button (or happens automatically)
- **SEES**: Suggested hashtags:
  - #smoothierecipe
  - #healthysmoothie
  - #morningroutine
  - #healthybreakfast
  - [etc. - 8-12 suggestions]
- **CLICKS**: Checkboxes next to hashtags she likes
- **CLICKS**: "Add Selected"
- **SEES**: Hashtags appended to caption
- **VERIFIES**: Hashtag suggestions relevant and useful

#### Pass/Fail Criteria

**✅ PASS if**:
- [ ] Laura understood automation limitations clearly
- [ ] Reminder system worked reliably
- [ ] Quick-post workflow felt efficient
- [ ] Copy/download features worked smoothly
- [ ] Tracking posted content worked
- [ ] Hashtag suggestions were relevant
- [ ] Laura felt workflow was faster than before
- [ ] Laura would actually use this daily

**❌ FAIL if**:
- [ ] Reminders didn't work or were confusing
- [ ] Quick-post features were buggy
- [ ] Copy/download didn't work
- [ ] Hashtag suggestions were irrelevant or poor
- [ ] Workflow felt clunky or slow
- [ ] Laura felt it wasn't saving time

---

### Test L3: Analytics Dashboard

**Goal**: Laura wants to track post performance

#### Dashboard Creation

**1-2. [Standard setup]**
- **TYPES**: "I want to see which of my posts perform best so I can make better content"

**3. Laura chooses approach**
- **SEES**:
  - "I can create a dashboard where you track post performance!"
  - "You'll need to input metrics manually from your platforms, or we can set up automatic tracking if you have API access."
- **TYPES**: "I'll input manually for now"

**4-6. [Watches build]**

**7. Laura uses dashboard**
- **CLICKS**: "Open Dashboard"
- **SEES**:
  - List of posted content from calendar
  - For each post: Input fields for "Likes" "Comments" "Shares"
  - "Update Stats" button
  - Empty charts/graphs (no data yet)

**8. Laura inputs data**
- **FINDS**: Post from last week
- **CLICKS**: On post or "Edit Stats"
- **TYPES**:
  - Likes: 245
  - Comments: 18
  - Shares: 12
- **CLICKS**: "Save Stats"
- **SEES**: Stats saved, post shows metrics

**9. Laura inputs more data**
- **REPEATS**: For 5-10 posts
- **SEES**: Charts start populating:
  - Line graph: Engagement over time
  - Bar chart: Top performing posts
  - Pie chart: Content type breakdown (if categorized)

**10. Laura analyzes**
- **LOOKS AT**: Charts and insights
- **SEES**: Automatically generated insights like:
  - "Your video posts get 3x more engagement than images"
  - "Posts on Tuesdays perform 40% better than weekends"
  - "Hashtag #healthyrecipes appears in your top 5 posts"
- **VERIFIES**: Insights make sense based on data

#### Getting Recommendations

**1. Laura asks for guidance**
- **TYPES**: "Based on my data, can you suggest what types of posts I should focus on?"

**2. Laura gets recommendations**
- **SEES**: Analysis and recommendations:
  - "Your video content performs best - consider making more"
  - "Tuesday and Thursday posts get highest engagement"
  - "Recipes and meal prep content resonates most with your audience"
  - "Try posting between 9-11 AM for best reach"
- **VERIFIES**: Recommendations are data-driven and actionable

**3. Laura implements**
- **GOES TO**: Calendar
- **SCHEDULES**: New posts based on recommendations
  - More videos
  - Tuesday/Thursday slots
  - Recipe-focused content
  - 9-10 AM timing
- **VERIFIES**: Can apply learnings immediately

#### Pass/Fail Criteria

**✅ PASS if**:
- [ ] Dashboard interface was clear and professional
- [ ] Inputting metrics was straightforward
- [ ] Charts updated in real-time as data added
- [ ] Visualizations were clear and useful
- [ ] Automated insights were accurate and relevant
- [ ] Recommendations were actionable
- [ ] Laura could apply learnings to improve strategy
- [ ] Dashboard provided real value

**❌ FAIL if**:
- [ ] Dashboard was confusing or cluttered
- [ ] Inputting data was tedious
- [ ] Charts didn't display correctly
- [ ] Insights were generic or wrong
- [ ] Recommendations weren't helpful
- [ ] Laura couldn't see how to use the data
- [ ] Dashboard felt like busywork, not value

---

## Cross-Cutting Tests (All Users)

### Test X1: System Recovery from Failure

**Scenario**: Backend crashes during build, verify graceful recovery

#### Charlotte's Experience

**Setup**: Charlotte is building a game

**1. Charlotte watches build**
- Progress at "Step 3/5"
- Backend crashes (simulated by killing process)

**2. Charlotte sees recovery**
- **SEES**: Message appears within 5 seconds:
  - "Oops! Something went wrong. Let me try again..."
  - OR: "Connection lost. Reconnecting..."
- **VERIFIES**: No technical error shown

**3. System auto-recovers**
- Backend restarted
- **SEES**: "Back online! Continuing where we left off..."
- Progress resumes: "Step 3/5" continues
- **VERIFIES**: Build completes successfully

**✅ PASS if**: Charlotte never saw scary technical errors, system recovered automatically
**❌ FAIL if**: Charlotte saw error messages, build failed, or required manual intervention

#### Mason's Experience

**Same scenario, different expectations**

**2. Mason sees error with context**
- **SEES**:
  - "Build interrupted. Your progress is saved."
  - Options: "Resume build" | "Start fresh"
- **CLICKS**: "Resume build"
- **SEES**: Build continues from saved point

**✅ PASS if**: Mason had control, work preserved, could make informed choice
**❌ FAIL if**: Lost work, no options, confusing error

#### Laura's Experience

**Same scenario, professional context**

**2. Laura sees professional error**
- **SEES**:
  - "Connection lost. Your work is saved."
  - "Reconnecting automatically..."
- **SEES**: Auto-reconnects when backend returns
- **SEES**: "Reconnected. Continuing work."

**✅ PASS if**: Laura's work preserved, professional communication, minimal disruption
**❌ FAIL if**: Lost work, unprofessional errors, couldn't continue

---

### Test X2: Unclear Request Handling

**Scenario**: Each user gives vague request, system adapts response to user level

#### Charlotte: "Make something cool"

**SEES**:
- "What's your favorite kind of game?"
- Big buttons with emojis: "🦕 Catch things" "🧩 Solve puzzles" "🎨 Make art"
- Clear, simple, visual

**✅ PASS if**: Age-appropriate, visual, simple choices
**❌ FAIL if**: Too wordy, technical, or confusing

#### Mason: "I want to build an app"

**SEES**:
- "What should the app do?"
- "Who will use it?"
- "What problem does it solve?"
- Examples provided for each

**✅ PASS if**: Educational questions that make Mason think
**❌ FAIL if**: Too simple (talking down) or too complex

#### Laura: "Help me with social media"

**SEES**:
- "What aspect of social media can I help with?"
- Options: "Content creation" | "Scheduling" | "Analytics" | "Brainstorming"
- Professional, efficient

**✅ PASS if**: Professional options, gets to point quickly
**❌ FAIL if**: Too casual or wastes Laura's time

---

### Test X3: Performance Under Load

**Scenario**: All three users working simultaneously

**Setup**:
1. Charlotte starts building Tetris
2. Mason starts building store
3. Laura starts building calendar

**Verification (each user independently)**:

**Charlotte**:
- [ ] Her game builds normally
- [ ] Progress updates as expected
- [ ] No slowdowns or errors
- [ ] Completes successfully

**Mason**:
- [ ] His store builds independently
- [ ] No interference from other users
- [ ] His work persists correctly

**Laura**:
- [ ] Her calendar builds without issues
- [ ] Performance feels responsive
- [ ] No cross-contamination of data

**System verification**:
- [ ] Three separate projects in database
- [ ] Three separate file directories
- [ ] No mixed-up data
- [ ] All three users satisfied

**✅ PASS if**: All three users had normal, independent experiences
**❌ FAIL if**: Any interference, slowdowns, or data mixing

---

## Test Execution Checklist

Before running any test:

- [ ] Backend running (http://localhost:8000)
- [ ] Frontend running (http://localhost:3000)
- [ ] Browser open (Chrome/Firefox/Safari)
- [ ] Screen recording started (to capture evidence)
- [ ] Database clean (no test pollution)

During test:

- [ ] Actually click buttons (don't just call APIs)
- [ ] Watch what user would see
- [ ] Try to break it (click rapidly, go back, refresh)
- [ ] Take screenshots at key moments
- [ ] Note any confusion or friction

After test:

- [ ] Did user accomplish goal? (binary yes/no)
- [ ] Would they use this again?
- [ ] Where did they get stuck or confused?
- [ ] What would make it better?

---

## What "PASS" Really Means

**PASS ≠ "API returned 200"**

**PASS = User successfully did what they wanted to do**

Examples:
- Charlotte played her game and had fun ✅
- Mason built his store and can customize it ✅
- Laura planned her content and saved time ✅

If the user got frustrated, confused, or gave up → **FAIL**, even if technically working

---

## Next Step

**I recommend starting with Test C1** (Charlotte's Tetris):
- Simplest scenario
- Highest priority (zero-tolerance user)
- Validates core flow
- Fast to execute (~5 minutes)

**I will**:
1. Open http://localhost:3000 in actual browser
2. Click actual buttons
3. Watch actual UI
4. Verify actual user experience
5. Report what actually happened

**Ready to run Test C1 when you are.**
