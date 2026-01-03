# GitHub Release Setup Guide

This guide will help you set up automatic builds for Windows, Mac, and Linux using GitHub Actions.

## Prerequisites

- GitHub account
- Git installed on your computer

## Step 1: Create GitHub Repository

1. Go to https://github.com and log in
2. Click the "+" icon in top right → "New repository"
3. Repository name: `orra-referee-review` (or your choice)
4. Description: "ORRA Referee Review System - Post-game review app based on CRRDF"
5. Choose "Public" or "Private"
6. Click "Create repository"

## Step 2: Upload Your Code

### Option A: Using GitHub Web Interface (Easier)

1. On your new repository page, click "uploading an existing file"
2. Drag and drop these files:
   ```
   referee_review_app.py
   README.md
   QUICK_START.md
   requirements.txt
   .gitignore
   ```
3. Click "Commit changes"

4. Create the workflow folder:
   - Click "Add file" → "Create new file"
   - Type `.github/workflows/build-releases.yml` as the filename
   - Paste the contents from the `build-releases.yml` file
   - Click "Commit changes"

### Option B: Using Git Command Line (Advanced)

```bash
# Navigate to your project folder
cd /path/to/referee-review-files

# Initialize git repository
git init

# Add all files
git add .

# Commit files
git commit -m "Initial commit - ORRA Referee Review System"

# Add remote repository (replace USERNAME with your GitHub username)
git remote add origin https://github.com/USERNAME/orra-referee-review.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 3: Create Your First Release

### Trigger a Build

You have two options:

#### Option A: Create a Version Tag (Recommended)

```bash
# Using Git command line
git tag v1.0.0
git push origin v1.0.0
```

Or via GitHub web interface:
1. Go to your repository
2. Click "Releases" (right sidebar)
3. Click "Create a new release"
4. Click "Choose a tag"
5. Type `v1.0.0` and click "Create new tag"
6. Release title: "Version 1.0.0"
7. Click "Publish release"

#### Option B: Manual Trigger

1. Go to your repository on GitHub
2. Click "Actions" tab
3. Click "Build Releases" workflow
4. Click "Run workflow" button
5. Select branch (main)
6. Click "Run workflow"

## Step 4: Monitor the Build

1. Go to "Actions" tab in your repository
2. Click on the running workflow
3. Watch the build process for all three platforms:
   - 🪟 Windows (builds .exe)
   - 🍎 macOS (builds app)
   - 🐧 Linux (builds executable)

Build takes approximately 5-10 minutes.

## Step 5: Download Your Releases

Once the build completes:

1. Go to "Releases" section of your repository
2. You'll see your new release with three downloadable files:
   - `orra-referee-review-windows.zip` (Windows)
   - `orra-referee-review-macos.zip` (macOS)
   - `orra-referee-review-linux.tar.gz` (Linux)

3. Download and test on your platform

## What Gets Built

### Windows (orra-referee-review-windows.zip)
```
📦 orra-referee-review-windows.zip
  ├── ORRA Referee Review.exe  ← Double-click to run!
  ├── README.md
  └── QUICK_START.md
```

### macOS (orra-referee-review-macos.zip)
```
📦 orra-referee-review-macos.zip
  ├── ORRA Referee Review  ← Right-click → Open
  ├── README.md
  └── QUICK_START.md
```

### Linux (orra-referee-review-linux.tar.gz)
```
📦 orra-referee-review-linux.tar.gz
  ├── orra-referee-review  ← Make executable and run
  ├── README.md
  └── QUICK_START.md
```

## Creating New Releases

When you update the app:

1. **Update your code** on GitHub (upload new files or use git)

2. **Create a new version tag**:
   ```bash
   git tag v1.1.0
   git push origin v1.1.0
   ```
   
   Or via GitHub web interface:
   - Releases → Create new release
   - Tag: `v1.1.0`
   - Title: "Version 1.1.0 - Bug fixes and improvements"
   - Describe what's new
   - Publish

3. **GitHub Actions automatically builds** all three versions

4. **New release appears** with updated downloads

## Version Numbering

Use semantic versioning: `vMAJOR.MINOR.PATCH`

- **MAJOR** (v2.0.0): Breaking changes, major new features
- **MINOR** (v1.1.0): New features, backwards compatible
- **PATCH** (v1.0.1): Bug fixes, small improvements

Examples:
- `v1.0.0` - Initial release
- `v1.0.1` - Fixed Excel export bug
- `v1.1.0` - Added new CRRDF questions
- `v2.0.0` - Complete UI redesign

## Sharing Releases

### For ORRA Members

1. Share the GitHub repository URL:
   ```
   https://github.com/USERNAME/orra-referee-review
   ```

2. Direct them to Releases page:
   ```
   https://github.com/USERNAME/orra-referee-review/releases
   ```

3. They download the file for their operating system

4. No Python installation needed - it's a standalone app!

### Distribution Options

**Option 1: GitHub Releases (Recommended)**
- Free hosting
- Version history
- Easy updates
- Professional appearance

**Option 2: ORRA Website**
- Download the built files from GitHub
- Upload to ORRA website
- Members download from orra.co.nz

**Option 3: Google Drive**
- Download built files
- Upload to Google Drive
- Share folder link with ORRA members

## Troubleshooting

### Build Fails

**Check the Actions log:**
1. Actions tab → Click failed workflow
2. Click the failed job (Windows/macOS/Linux)
3. Read error messages

**Common issues:**
- Python syntax errors in the code
- Missing dependencies in requirements.txt
- File path issues

### macOS Security Warning

Users may see "Cannot open because developer cannot be verified"

**Solution:**
1. Right-click the app
2. Select "Open"
3. Click "Open" in the dialog
4. This only needs to be done once

### Windows Security Warning

Users may see "Windows protected your PC"

**Solution:**
1. Click "More info"
2. Click "Run anyway"
3. This only needs to be done once

## Advanced: Customizing the Build

### Add an Icon

1. Create an icon file:
   - Windows: `icon.ico`
   - macOS: `icon.icns`
   - Linux: `icon.png`

2. Update the workflow file:
   ```yaml
   pyinstaller --onefile --windowed --icon=icon.ico --name="ORRA Referee Review" referee_review_app.py
   ```

3. Add icon file to repository

### Include Additional Files

In the workflow, add files to the release folder:

```yaml
- name: Build executable with PyInstaller (Windows)
  run: |
    pyinstaller --onefile --windowed --name="ORRA Referee Review" referee_review_app.py
    mkdir release
    copy dist\\"ORRA Referee Review.exe" release\\
    copy README.md release\\
    copy QUICK_START.md release\\
    copy ORRA_Referee_Review_System_Documentation.docx release\\  # Add this
```

## Benefits of This Setup

✅ **Automatic builds** - Push code, get executables
✅ **Multi-platform** - One workflow builds for all OSes
✅ **No Python needed** - Users just download and run
✅ **Professional** - GitHub releases page looks official
✅ **Version control** - Track all releases and changes
✅ **Easy updates** - Tag new version, automatic rebuild
✅ **Free hosting** - GitHub hosts your releases

## File Structure in Repository

```
orra-referee-review/
├── .github/
│   └── workflows/
│       └── build-releases.yml
├── .gitignore
├── referee_review_app.py
├── requirements.txt
├── README.md
├── QUICK_START.md
└── (optional) icon.ico
```

## Next Steps

1. ✅ Create GitHub repository
2. ✅ Upload files
3. ✅ Create first release (v1.0.0)
4. ✅ Test downloads on each platform
5. ✅ Share with ORRA members
6. 📝 Collect feedback
7. 🔄 Update and release v1.1.0

## Support

If you have issues with GitHub Actions:
- Check the Actions tab for error logs
- Google the error message
- Ask in ORRA technical group
- GitHub has excellent documentation

---

**You're now set up to automatically build and distribute professional referee review applications for all platforms!** 🎉
