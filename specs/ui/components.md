# UI Components Specification

## Overview
The frontend provides a modern, responsive interface for task management and AI chat.

## Pages

### Auth Page (`/auth`)
**Purpose:** User authentication (login/signup)

**Components:**
- LoginForm - Email/password login
- SignupForm - New user registration
- Navigation links between login/signup

**State:**
- Email, password inputs
- Loading state during API calls
- Error messages for invalid credentials

---

### Dashboard Page (`/dashboard`)
**Purpose:** Main task management interface

**Components:**
- Header with branding and logout
- Stats sidebar (total, completed, pending, overdue)
- Task filters (search, status, priority, sorting)
- Task list with cards
- Task form modal (create/edit)
- Chat panel toggle button

**Features:**
- Real-time task updates
- Filter and search functionality
- Task completion toggle
- Edit and delete actions
- Responsive design

---

### Chat Panel
**Purpose:** AI-powered task management via natural language

**Components:**
- Chat message list
- Message input field
- Send button
- Conversation history

**Features:**
- Persistent conversations
- Tool call visualization
- Error handling
- Loading states

---

## Component Library

### UI Components (shadcn/ui)
Located in `Frontend/src/components/ui/`:
- accordion, alert, alert-dialog, aspect-ratio
- avatar, badge, breadcrumb, button
- calendar, card, carousel, chart
- checkbox, collapsible, command, context-menu
- dialog, drawer, dropdown-menu
- form, hover-card, input, input-otp, label
- menubar, navigation-menu, pagination, popover
- progress, radio-group, resizable
- scroll-area, select, separator, sheet, sidebar
- skeleton, slider, sonner, switch
- table, tabs, textarea, toast, toaster, toggle
- tooltip

---

## Task Components

### TodoItem
**Purpose:** Display individual task card

**Props:**
- todo: Task data
- onToggle: Complete toggle handler
- onEdit: Edit handler
- onDelete: Delete handler

**Features:**
- Priority badge (high/medium/low)
- Category badge
- Due date display
- Completion checkbox
- Edit/delete buttons
- Hover animations

---

### TodoForm
**Purpose:** Create/edit task modal

**Fields:**
- Title (required)
- Description (optional)
- Priority (high/medium/low)
- Category (select)
- Due date (date picker)
- Due time (time picker)
- Recurring toggle
- Reminder toggle

---

### TodoFilters
**Purpose:** Task filtering and sorting toolbar

**Filters:**
- Search bar (keyword search)
- Status filter (all/pending/completed)
- Priority filter (multi-select)
- Category filter (multi-select)
- Sort by (date/priority/title)
- Sort order (ascending/descending)

---

### TodoStats
**Purpose:** Task statistics dashboard

**Metrics:**
- Total tasks
- Completed tasks
- Pending tasks
- Overdue tasks
- Completion percentage (progress bar)

---

## Styling

### Theme
- Dark theme optimized
- Green primary color
- Glassmorphism effects
- Neon glow accents

### Tailwind Utilities
- Custom utilities in `index.css`
- `.neon-glow` - Glowing box shadow
- `.neon-text` - Glowing text shadow
- `.glass` - Glassmorphism effect

---

## Implementation Status
✅ Complete - All components implemented in `Frontend/src/`
