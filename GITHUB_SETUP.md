# Hosting Quiz Master on GitHub - Complete Guide

Follow these steps to host your Quiz Master project on GitHub.

## Step 1: Install Git

### Windows
Download from: https://git-scm.com/download/win
- Run the installer
- Accept default options
- Restart your computer

### macOS
```bash
brew install git
```

### Linux (Ubuntu/Debian)
```bash
sudo apt-get install git
```

**Verify installation:**
```bash
git --version
```

---

## Step 2: Configure Git

Open PowerShell/Terminal and run:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

Example:
```bash
git config --global user.name "John Doe"
git config --global user.email "john.doe@gmail.com"
```

**Verify configuration:**
```bash
git config --global --list
```

---

## Step 3: Initialize Git Repository

Navigate to your project folder:

```bash
cd "d:\IITM\MAD1 PROJECT\APP_DEV_1-PROJECT"
```

Initialize git repository:
```bash
git init
```

Check status:
```bash
git status
```

---

## Step 4: Add Files to Git

Add all files:
```bash
git add .
```

Verify what will be committed:
```bash
git status
```

---

## Step 5: Create Initial Commit

```bash
git commit -m "Initial commit: Quiz Master application with security features"
```

---

## Step 6: Create GitHub Account

1. Go to https://github.com
2. Click "Sign up"
3. Enter email, password, and username
4. Verify email address
5. Complete setup

---

## Step 7: Create New Repository on GitHub

1. Log in to GitHub
2. Click "+" (top right) → "New repository"
3. Fill in:
   - **Repository name**: `quiz-master` or `QuizMaster`
   - **Description**: "A professional quiz platform with security features"
   - **Public/Private**: Choose (Public recommended for portfolio)
   - **Initialize**: Do NOT initialize with README/gitignore (we already have them)
4. Click "Create repository"

---

## Step 8: Connect Local Repository to GitHub

GitHub will show you commands. Run these in PowerShell:

### Add remote repository:
```bash
git remote add origin https://github.com/YOUR_USERNAME/quiz-master.git
```

Replace `YOUR_USERNAME` with your GitHub username.

### Rename branch to main (if needed):
```bash
git branch -M main
```

### Push to GitHub:
```bash
git push -u origin main
```

You may be prompted for authentication - use your GitHub credentials.

---

## Step 9: Verify on GitHub

1. Go to your repository on GitHub
2. You should see your project files
3. Your README.md should display automatically

---

## Step 10: Add GitHub-Specific Files (Optional but Recommended)

### Create `.github/workflows/python-app.yml` for CI/CD:

```bash
mkdir -p .github/workflows
```

Then create file: `.github/workflows/python-app.yml`

```yaml
name: Python application

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2
    - name: Set up Python 3.12
      uses: actions/setup-python@v2
      with:
        python-version: 3.12
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Run tests
      run: |
        python -m pytest --tb=short
```

---

## Future Commits (After Initial Push)

For future changes:

```bash
# Check what changed
git status

# Add changes
git add .

# Commit with meaningful message
git commit -m "Fix: Improve search functionality"

# Push to GitHub
git push origin main
```

---

## Commit Message Best Practices

Use clear, descriptive messages:

```
git commit -m "Feature: Add quiz timer functionality"
git commit -m "Fix: Resolve CSRF token validation error"
git commit -m "Docs: Update README with installation steps"
git commit -m "Refactor: Clean up admin controller code"
git commit -m "Security: Implement rate limiting on login"
```

---

## Useful Git Commands

```bash
# View commit history
git log --oneline

# View changes before committing
git diff

# Undo last commit (keeps changes)
git reset --soft HEAD~1

# Undo last commit (removes changes)
git reset --hard HEAD~1

# Create a new branch
git checkout -b feature-name

# Switch branches
git checkout main

# Merge branch
git merge feature-name

# Delete branch
git branch -d feature-name
```

---

## GitHub Repository Settings

After pushing, configure:

1. **Settings** → **General**
   - Description: "Professional quiz platform built with Flask"
   - Website: (if you host it)

2. **Settings** → **Branches**
   - Set `main` as default branch

3. **Settings** → **Collaborators** (if working with others)
   - Add team members' GitHub usernames

4. **Add Topics** (for discoverability)
   - `flask`, `quiz`, `python`, `education`, `security`

---

## Create GitHub Pages (Optional)

If you want to host documentation:

1. Go to **Settings** → **Pages**
2. Select source: `main` branch, `/docs` folder
3. Your documentation will be available at: `https://yourusername.github.io/quiz-master`

---

## Troubleshooting

### Authentication Failed
```bash
# Use GitHub Personal Access Token instead of password
# Generate at: https://github.com/settings/tokens

# Or use SSH key setup (recommended)
# https://docs.github.com/en/authentication/connecting-to-github-with-ssh
```

### Wrong Repository URL
```bash
# Check current remote
git remote -v

# Update remote
git remote set-url origin https://github.com/YOUR_USERNAME/quiz-master.git
```

### Files Not Showing
```bash
# Make sure .gitignore is not excluding them
git add -f filename.txt  # Force add

# Or update .gitignore
```

### Large Files
GitHub limits file sizes. If you get an error:
```bash
# Remove large files
git rm --cached instance/quizmaster.sqlite3
git commit -m "Remove database file"
```

---

## Security Tips for GitHub

⚠️ **Important**: Never commit these files:
- `.env` (database passwords, secret keys)
- `instance/quizmaster.sqlite3` (database with user data)
- `venv/` (virtual environment)

They are already in `.gitignore` ✅

---

## Share Your Repository

After pushing to GitHub, you can share:
- **GitHub URL**: `https://github.com/YOUR_USERNAME/quiz-master`
- **Clone command**: `git clone https://github.com/YOUR_USERNAME/quiz-master.git`

---

## Next Steps

After hosting on GitHub:

1. ✅ Add a LICENSE file
   - Go to your repo → Add file → `.github/LICENSE`
   - Choose a license (MIT recommended)

2. ✅ Add CONTRIBUTING.md
   - Instructions for other developers

3. ✅ Create Issues for features/bugs
   - Help track development

4. ✅ Add Releases
   - Create version tags (v1.0.0, v1.1.0, etc.)

5. ✅ Enable Discussions
   - Let others ask questions

---

## Example: Complete Commands for Your Project

```bash
# 1. Navigate to project
cd "d:\IITM\MAD1 PROJECT\APP_DEV_1-PROJECT"

# 2. Initialize git (if not done)
git init

# 3. Configure user
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# 4. Add all files
git add .

# 5. Initial commit
git commit -m "Initial commit: Quiz Master - Professional Quiz Platform"

# 6. Add remote (replace USERNAME)
git remote add origin https://github.com/USERNAME/quiz-master.git

# 7. Rename branch
git branch -M main

# 8. Push to GitHub
git push -u origin main
```

---

## Support

- GitHub Documentation: https://docs.github.com
- Git Documentation: https://git-scm.com/doc
- GitHub Community: https://github.community

---

**Ready to push? You're all set! 🚀**
