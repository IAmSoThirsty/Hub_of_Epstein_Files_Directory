# Staff Tasks and Calendar Guide

## Overview

This guide covers the two new features added to the staff portal:
1. **Task Assignment System** - Assign specific tasks to AI agents in their category
2. **Calendar Availability** - Mark your availability on the team calendar

---

## Task Assignment System

### Purpose
Allow staff members to assign specific tasks to AI agents based on their work category. Tasks queue up and are processed by agents in order based on priority.

### How to Assign Tasks

1. **Navigate to Task Assignment**
   - Go to `/staff/tasks.html`
   - Or click "Tasks" in the staff navigation menu

2. **Select an Agent**
   - Browse agents by category (Document, Image, Search, QC, Organization)
   - Click on the agent you want to assign the task to
   - The agent card will highlight in red when selected

3. **Fill Task Details**
   - **Task Title**: Brief description (e.g., "Process FBI Vault PDFs")
   - **Task Description**: Detailed instructions, file paths, requirements
   - **Priority Level**: Choose Low, Medium, or High
     - **Low**: Process when capacity available
     - **Medium**: Normal queue processing (default)
     - **High**: Process as soon as possible
   - **Estimated Volume**: Optional (e.g., 100 documents)
   - **Target Completion**: Optional deadline date

4. **Submit Task**
   - Click "Submit Task" button
   - Task is added to agent's queue
   - You'll receive confirmation
   - Task appears in "Your Recent Tasks" section

### Agent Categories

#### Document Agents (7 agents)
- **Document Indexing** (6,000/day) - Index new documents
- **OCR Processing** (5,000/day) - Convert scanned PDFs to text
- **Document Analysis** (3,000/day) - Extract metadata and entities
- **Document Verification** (2,000/day) - Verify authenticity
- **Summarization** (10,000/day) - Generate summaries
- **Cross-Reference** (15,000/day) - Find related documents
- **Classification** (10,000/day) - Auto-categorize documents

#### Image Agents (5 agents)
- **Image Indexing** (10,000/day) - Catalog images
- **Image Analysis** (5,000/day) - Extract visual information
- **Image Verification** (3,000/day) - Verify authenticity
- **Image Organization** (15,000/day) - Organize library
- **Image Maintenance** (5,000/day) - Quality control

#### Search Agents (3 agents)
- **Web Search** - External search (Google, Bing, DuckDuckGo)
- **Image Search** - Reverse image search
- **Internal Search** - Site search system

#### Quality Control Agents (3 agents)
- **Fact-Checking** - Verify claims
- **Source Verification** - Check sources
- **Content Moderation** - Review content

#### Organization Agents (4 agents)
- **Collection Management** - Organize collections
- **Timeline Generation** - Create timelines
- **Relationship Mapping** - Map connections
- **Auto-Tagging** - Apply tags

### Task Queue System

**How it works:**
- Each agent has its own task queue
- Tasks are processed in priority order:
  1. High priority tasks first
  2. Medium priority tasks second
  3. Low priority tasks last
- Within same priority, tasks are processed FIFO (first in, first out)
- Agent capacity is displayed (operations per day)
- Current queue size is shown for each agent

**Task Statuses:**
- **Queued**: Waiting in queue
- **In Progress**: Currently processing
- **Completed**: Successfully finished
- **Failed**: Error occurred (will retry)

### Monitoring Your Tasks

**Recent Tasks View:**
- Shows your last 10 assigned tasks
- Displays current status
- Shows position in queue (if queued)
- Provides ETA for completion

**To see all your tasks:**
- Go to Dashboard
- Check "My Assigned Tasks" widget
- Filter by status, agent, or date range

---

## Calendar Availability (Coming Soon)

### Purpose
Allow staff members to mark their availability on the team calendar for better coordination.

### How to Set Availability

1. **Navigate to Calendar**
   - Go to `/staff/calendar.html`
   - Or click "Calendar" in the staff navigation menu

2. **Click on a Day**
   - Click any day in the calendar view
   - Availability modal will open

3. **Set Your Status**
   - **Available** (Green) - Fully available for work
   - **Partially Available** (Yellow) - Available for limited hours
   - **Busy** (Red) - Unavailable, in meetings/tasks
   - **Off** (Gray) - Not working (day off, vacation)

4. **Add Details (Optional)**
   - Start time and end time (for partial availability)
   - Notes (e.g., "Available 9 AM - 1 PM", "Conference call 2-4 PM")

5. **Save Availability**
   - Click "Save" to update your status
   - Green dot appears on calendar day
   - Other staff can see your availability

### Availability Features

**Calendar Display:**
- Color-coded availability indicators on each day
- Green dot = Available
- Yellow dot = Partially Available
- Red dot = Busy
- Gray dot = Off

**Staff Availability List:**
- View all staff availability for selected day
- See who's available for collaboration
- Check team capacity for planning

**Recurring Availability:**
- Set weekly recurring patterns
- Example: "Every Monday, Busy 9-11 AM" (for team meetings)
- Save time by not repeating entries

### Use Cases

1. **Shift Scheduling**
   - Mark your available shifts
   - Coordinators can see coverage
   - Plan volunteer schedules

2. **Meeting Planning**
   - Find when most team members are available
   - Avoid scheduling conflicts
   - Coordinate across time zones

3. **Task Assignment**
   - See who's available for urgent tasks
   - Balance workload across team
   - Plan project timelines

4. **Time Off Tracking**
   - Mark vacation days
   - Team sees when you're out
   - Helps with project planning

---

## Integration with AI Agents

### Agent Dashboard Connection

The task assignment system integrates with the AI Agent Dashboard (`/staff/agents.html`):

1. **Real-time Queue Updates**
   - Agent dashboard shows live queue counts
   - Tasks you assign appear immediately
   - Progress updates in real-time

2. **Performance Metrics**
   - See how fast agents process tasks
   - Average completion times
   - Success rates

3. **Admin Controls (Admin Only)**
   - Admins can pause/resume agents
   - Adjust agent priorities
   - Configure processing parameters

4. **Staff View**
   - Staff see task-oriented information
   - Current task being processed
   - Queue position and ETA
   - **Cannot control agents** (admin only)

---

## Best Practices

### Task Assignment

**✅ DO:**
- Be specific in task descriptions
- Include file paths or identifiers
- Set realistic deadlines
- Use appropriate priority levels
- Check agent capacity before assigning large volumes

**❌ DON'T:**
- Assign duplicate tasks
- Set all tasks to high priority (defeats the purpose)
- Assign tasks to wrong agent type
- Forget to check queue status

### Calendar Availability

**✅ DO:**
- Update availability regularly
- Be honest about availability status
- Add notes for context
- Set recurring patterns for regular schedules
- Check team availability before planning

**❌ DON'T:**
- Forget to mark time off
- Leave availability outdated
- Mark as "available" when you're not
- Ignore team coordination

---

## Troubleshooting

### Task Assignment Issues

**Problem: Can't submit task**
- **Solution**: Ensure agent is selected and all required fields are filled

**Problem: Task not appearing in queue**
- **Solution**: Refresh the page, check agent dashboard

**Problem: Task failed**
- **Solution**: Check error log, reassign if needed, contact admin

### Calendar Issues

**Problem: Can't save availability**
- **Solution**: Check date is in the future, try refreshing

**Problem: Others can't see my availability**
- **Solution**: Ensure privacy settings allow team view

---

## Technical Details

### Data Storage

**Tasks:**
- Stored in: `data/staff/tasks.json`
- Also creates GitHub Issues for tracking
- Synced with agent queue system

**Calendar:**
- Stored in: `data/staff/calendar.json`
- Backed up in GitHub repository
- Accessible to all staff (read-only for non-owners)

### API Endpoints (For Developers)

**Task Assignment:**
```
POST /api/tasks/assign
GET /api/tasks/my-tasks
GET /api/tasks/status/{task-id}
DELETE /api/tasks/{task-id}
```

**Calendar:**
```
POST /api/calendar/availability
GET /api/calendar/day/{date}
GET /api/calendar/staff/{user-id}
PUT /api/calendar/availability/{id}
```

---

## Support

**Questions?**
- Check Staff Portal documentation
- Contact admin via staff chat
- Submit issue on GitHub

**Feature Requests:**
- Use bulletin board to suggest improvements
- Discuss in staff chat (General room)

---

**Last Updated:** December 20, 2024
**Version:** 1.0
