# Deploying Quiz Master to Render.com

Complete step-by-step guide to deploy your Flask app on Render.com (free tier).

---

## Prerequisites

✅ GitHub account (you have this)  
✅ Project on GitHub (you have this: https://github.com/KD-kaustubh/Quizmaster_Application)  
✅ Render account (free - we'll create it)

---

## Step 1: Create a Render Account

1. Go to https://render.com
2. Click **"Sign Up"**
3. Choose **"Sign up with GitHub"** (easiest)
4. Authorize Render to access your GitHub
5. Click **"Create account"**

**Done!** ✅

---

## Step 2: Prepare Your Project (IMPORTANT!)

Your project needs a few files for Render to work. Let me explain what's needed:

### Check your current files:
```
app.py                    ← Your main app
requirements.txt          ← Package list (should exist)
.gitignore               ← Git ignore (exists)
README.md                ← Documentation (exists)
```

---

## Step 3: Create `render.yaml` (Configuration File)

This tells Render how to run your app.

**Create a new file in your project root:** `render.yaml`

```yaml
services:
  - type: web
    name: quizmaster
    env: python
    plan: free
    
    # Python version
    pythonVersion: 3.12
    
    # Install dependencies
    buildCommand: pip install -r requirements.txt
    
    # Start the app
    startCommand: gunicorn app:app
    
    # Environment variables
    envVars:
      - key: FLASK_ENV
        value: production
      - key: FLASK_SECRET_KEY
        generateValue: true
      - key: WTF_CSRF_ENABLED
        value: true
      - key: SESSION_COOKIE_SECURE
        value: true
      - key: SESSION_COOKIE_SAMESITE
        value: Lax
```

---

## Step 4: Update `requirements.txt`

Your requirements.txt must include `gunicorn` (the server).

Current packages needed:

```
Flask==3.1.0
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Flask-Bcrypt==1.0.1
Flask-WTF==1.2.2
WTForms==3.2.1
Flask-Limiter==4.1.1
python-dotenv==1.0.1
SQLAlchemy==2.0.37
Werkzeug==3.1.3
gunicorn==22.0.0
```

**Make sure `gunicorn` is in there!**

---

## Step 5: Update Your Flask App Settings

Edit your `app.py` and update the app configuration for production:

**Add these lines after creating the Flask app:**

```python
import os

app = Flask(__name__)

# Production settings
if os.getenv('FLASK_ENV') == 'production':
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
else:
    # Development
    app.config['SESSION_COOKIE_SECURE'] = False

# Secret key from environment or fallback
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-key-change-in-production')

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'SQLALCHEMY_DATABASE_URI',
    'sqlite:///quizmaster.sqlite3'
)
```

---

## Step 6: Push Changes to GitHub

```bash
cd "d:\IITM\MAD1 PROJECT\APP_DEV_1-PROJECT"

# Check what changed
git status

# Add files
git add .

# Commit
git commit -m "Add: Render deployment configuration"

# Push to GitHub
git push origin main
```

---

## Step 7: Deploy on Render

1. Go to https://render.com
2. **Login** with your GitHub account
3. Click **"New +"** (top right)
4. Select **"Web Service"**
5. Click **"Connect a repository"**
6. Find and select: **"Quizmaster_Application"**
7. Click **"Connect"**

### Fill in the details:

| Field | Value |
|-------|-------|
| Name | `quizmaster` |
| Environment | `Python 3` |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn app:app` |
| Plan | **Free** ✅ |

8. Click **"Advanced"** and add environment variables:

| Key | Value |
|-----|-------|
| `FLASK_ENV` | `production` |
| `WTF_CSRF_ENABLED` | `true` |
| `SESSION_COOKIE_SECURE` | `true` |

9. Click **"Create Web Service"**

**Render will deploy automatically!** 🚀

---

## Step 8: Wait for Deployment

The deployment will take 3-5 minutes. You'll see:

```
Building your service...
Installing dependencies...
Running your app...
```

When you see a green checkmark and a URL like:
```
https://quizmaster-xxxxx.onrender.com
```

**Your app is LIVE!** 🎉

---

## Step 9: Test Your App

1. Visit the URL: `https://quizmaster-xxxxx.onrender.com`
2. You should see your home page
3. Try logging in with: `admin@gmail.com / Admin123`

---

## Common Issues & Solutions

### Issue: "ModuleNotFoundError: No module named 'app'"
**Fix:** Make sure your main file is named `app.py` (not `main.py` or `server.py`)

### Issue: "gunicorn: command not found"
**Fix:** Add `gunicorn==22.0.0` to requirements.txt

### Issue: Database not working
**Fix:** The database will be created fresh on Render (first time only)

### Issue: "502 Bad Gateway"
**Fix:** Check the logs in Render dashboard → Logs tab

### Issue: Static files not loading
**Fix:** Make sure your `static/` and `templates/` folders are in the project root

---

## After Deployment: Useful Commands

### View logs:
- Go to Render dashboard
- Click your service
- Click "Logs" tab

### Redeploy:
- Push to GitHub: `git push origin main`
- Render auto-deploys within 1-2 minutes

### Update environment variables:
- Render dashboard → "Environment"
- Edit and save (auto-redeploys)

### Custom domain (optional):
- Render dashboard → "Settings"
- Add your own domain (paid feature)

---

## Deployment Summary

| Step | Status |
|------|--------|
| GitHub repo ready | ✅ Done |
| Render account | 👈 Create now |
| render.yaml config | 👈 Create now |
| requirements.txt updated | 👈 Update now |
| Push to GitHub | 👈 Do now |
| Deploy on Render | 👈 Deploy now |
| App live online | 🎉 Success! |

---

## Your App URLs

- **GitHub:** https://github.com/KD-kaustubh/Quizmaster_Application
- **Live App:** https://quizmaster-xxxxx.onrender.com (after deployment)

---

## Free Tier Limitations

- **Sleep after 15 minutes of inactivity** (wakes up when accessed)
- **512 MB RAM** (enough for your app)
- **100 GB bandwidth/month** (plenty)
- **SQLite database** (limited - max 100MB)

If you need more, upgrade to Paid ($7/month).

---

## Need Help?

1. Check Render logs for errors
2. Verify `render.yaml` syntax
3. Ensure `gunicorn` is in requirements.txt
4. Make sure `app.py` is in project root

---

**Ready? Let's do this!** 🚀

Start with Step 1: Create Render account at https://render.com
