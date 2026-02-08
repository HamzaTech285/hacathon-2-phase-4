# 🚀 TaskFlow - Quick Start Guide

## ✅ What's Fixed

Your app now has the complete flow:
1. **Landing Page** (`/`) - Shows "Get Started" button
2. **Auth Pages** (`/auth`, `/login`, `/signup`) - Login/signup forms
3. **Dashboard** (`/dashboard`) - Modern UI with tasks (requires login)

## 🏃 How to Start

### Option 1: Using Batch Files (Easiest)

**Terminal 1 - Backend:**
```cmd
START_BACKEND.bat
```

**Terminal 2 - Frontend:**
```cmd
START_FRONTEND.bat
```

### Option 2: Manual Start

**Terminal 1 - Backend:**
```powershell
cd backend
pip install -r requirements.txt
python init_db.py
uvicorn src.main:app --reload
```

**Terminal 2 - Frontend:**
```powershell
cd Frontend
npm install
npm run dev
```

## 📝 Usage Flow

1. **Open browser** → http://localhost:5173
2. **Landing page** appears with "Get Started" button
3. **Click "Get Started"** → Goes to `/auth` (modern auth page)
4. **Choose Sign Up** → Create account or use existing credentials
5. **Login** → Redirects to `/dashboard`
6. **Dashboard** → Create and manage your tasks!

## 🔑 Test Flow

1. Click "Get Started" on landing page
2. Switch to "Sign Up" tab
3. Enter:
   - Email: `test@example.com`
   - Password: `password123`
   - Full Name: `Test User`
4. Click "Create Account"
5. You'll be redirected to the dashboard!

## 🎯 Available Routes

- `/` - Landing page with features
- `/auth` - Modern auth page (login/signup toggle)
- `/login` - Dedicated login page (old style)
- `/signup` - Dedicated signup page (old style)  
- `/dashboard` - Task management dashboard (protected)

**Note:** All three auth pages work! The landing page goes to `/auth` by default.

## 🐛 Troubleshooting

**Backend Connection Refused:**
- Make sure backend is running on port 8000
- Run: `START_BACKEND.bat` or manually start it

**Can't see tasks:**
- Backend must be running first
- Check browser console for errors
- Make sure you're logged in

**Dependencies not installing:**
- Backend: Make sure Python 3.8+ is installed
- Frontend: Make sure Node.js 16+ is installed

## 🎨 Features Available

✅ Landing page with "Get Started"
✅ Auth pages (modern + old style)
✅ Login redirects to dashboard
✅ Dashboard requires authentication
✅ Create, edit, delete tasks
✅ Filter and search tasks
✅ Beautiful modern UI with neon effects
✅ Stats sidebar
✅ Chat panel (demo mode)

## 🔗 Quick Links

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

Enjoy your TaskFlow app! 🎉
