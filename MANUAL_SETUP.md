# 📋 Manual Setup Instructions

## ✅ All Code Changes Are Complete!

Your Frontend now has:
- ✅ Landing page with "Get Started" button at `/`
- ✅ Auth pages at `/auth`, `/login`, `/signup`
- ✅ Modern dashboard at `/dashboard` (requires login)
- ✅ All UI components adapted for FastAPI backend

## 🔧 Setup Steps

### Step 1: Install Backend Dependencies

Open a **new PowerShell terminal** and run:

```powershell
cd backend
pip install fastapi sqlmodel uvicorn python-jose passlib bcrypt python-multipart
```

**Note:** If this is slow, you can install one by one or wait for it to complete.

### Step 2: Initialize Database

```powershell
python init_db.py
```

You should see: "Database initialized successfully!"

### Step 3: Start Backend Server

```powershell
uvicorn src.main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

**Keep this terminal open!**

### Step 4: Install Frontend Dependencies

Open a **second PowerShell terminal** and run:

```powershell
cd Frontend
npm install
```

### Step 5: Start Frontend

```powershell
npm run dev
```

You should see:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
```

**Keep this terminal open too!**

## 🎯 Testing the App

1. **Open browser:** http://localhost:5173
2. You'll see the **Landing Page** with "Get Started" button
3. Click **"Get Started"** → Takes you to `/auth`
4. Click **"Sign Up"** tab
5. Enter:
   - Email: `test@example.com`
   - Password: `password123`
   - Full Name: `Test User`
6. Click **"Create Account"**
7. You'll be redirected to the **Dashboard**!
8. Create some tasks and enjoy the modern UI! 🎉

## 🔄 Complete User Flow

```
Landing (/) 
    ↓ [Click "Get Started"]
Auth (/auth)
    ↓ [Sign Up or Login]
Dashboard (/dashboard)
    ↓ [Create, manage tasks]
    ↓ [Logout button in header]
Landing (/) - Logged out
```

## 🐛 If You See "Network Error"

This means the backend isn't running. Make sure:
1. Backend terminal shows: `Uvicorn running on http://127.0.0.1:8000`
2. No errors in the backend terminal
3. Port 8000 is not used by another app

## 🎨 What You'll See

### Landing Page
- Matrix-style background animation
- "TaskFlow" title with neon green glow
- 6 feature cards
- Big "Get Started" button

### Auth Page (/auth)
- Modern glassmorphism design
- Toggle between Login/Sign Up
- Dark theme with green accents
- Back button to landing

### Dashboard
- Header with "TaskFlow" logo and "New Task" button
- Stats sidebar (Total, Completed, Pending, Overdue)
- Search and filter toolbar
- Task cards with checkboxes, priority badges
- Floating chat button
- Logout button

## 📁 Alternatively: Use Batch Files

Once dependencies are installed, you can use:

**Terminal 1:**
```cmd
START_BACKEND.bat
```

**Terminal 2:**
```cmd
START_FRONTEND.bat
```

## ✨ That's It!

Your app is ready to use. The UI from the `UI/` folder is now fully integrated into your `Frontend/` folder and works with your FastAPI backend!

If you have any issues with installation, just let me know! 🚀
