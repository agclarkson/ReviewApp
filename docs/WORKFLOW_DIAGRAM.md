# GitHub Actions Build Workflow

## Visual Overview

```
┌─────────────────────────────────────────────────────────────┐
│  YOU: Update Code & Create Version Tag                     │
│  Example: git tag v1.0.0 && git push origin v1.0.0        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  GITHUB: Detects new tag, triggers workflow                │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
┌──────────────┐          ┌──────────────┐
│   Windows    │          │    macOS     │
│    Build     │          │    Build     │
│              │          │              │
│  - Setup     │          │  - Setup     │
│  - Install   │          │  - Install   │
│  - PyInst.   │          │  - PyInst.   │
│  - Package   │          │  - Package   │
│    as .zip   │          │    as .zip   │
└──────┬───────┘          └──────┬───────┘
       │                         │
       └──────────┬──────────────┘
                  │
                  ▼
         ┌──────────────┐
         │    Linux     │
         │    Build     │
         │              │
         │  - Setup     │
         │  - Install   │
         │  - PyInst.   │
         │  - Package   │
         │    as .tar.gz│
         └──────┬───────┘
                │
                ▼
┌─────────────────────────────────────────────────────────────┐
│  GITHUB: Creates Release with 3 Download Files             │
│                                                              │
│  ✓ orra-referee-review-windows.zip                         │
│  ✓ orra-referee-review-macos.zip                           │
│  ✓ orra-referee-review-linux.tar.gz                        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  USERS: Download & Run - No Python Needed!                 │
│                                                              │
│  Windows: Unzip → Double-click .exe                        │
│  macOS:   Unzip → Right-click → Open                       │
│  Linux:   Extract → chmod +x → Run                         │
└─────────────────────────────────────────────────────────────┘
```

## Timeline

```
T+0 min:  You push version tag
T+1 min:  GitHub starts building all 3 platforms in parallel
T+5 min:  Builds complete
T+6 min:  Release created with downloadable files
T+7 min:  Users can download and run!
```

## What Happens Under the Hood

### On Each Platform

1. **Checkout Code** - Downloads your repository files
2. **Setup Python** - Installs Python 3.11
3. **Install Dependencies** - Installs openpyxl and PyInstaller
4. **Run PyInstaller** - Bundles app + Python + libraries into single file
5. **Package** - Creates zip/tar.gz with exe + documentation
6. **Upload** - Sends to GitHub Releases

### PyInstaller Magic

```
Your Python Code (referee_review_app.py)
         +
Python Interpreter
         +
All Libraries (openpyxl, tkinter, etc.)
         +
All Dependencies
         ↓
   [PyInstaller]
         ↓
Single Executable File
```

**Result**: Users don't need Python installed. Everything is bundled!

## File Sizes (Approximate)

- Windows: ~15-20 MB
- macOS: ~20-25 MB
- Linux: ~15-20 MB

These files are larger because they include:
- Python interpreter
- tkinter GUI library
- openpyxl Excel library
- All standard library modules

## Security & Trust

### Code Signing (Optional Advanced Feature)

GitHub Actions can code-sign your apps:
- **Windows**: Requires code signing certificate ($)
- **macOS**: Requires Apple Developer account ($99/year)
- **Linux**: Generally not required

**Without signing**: Users see security warnings but can still run the app.

**With signing**: Apps run without warnings, looks more professional.

For ORRA internal use, code signing is optional.

## Updating Your App

```
┌─────────────────────────────┐
│ 1. Edit Python file         │
│    (fix bug, add feature)   │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ 2. Test locally             │
│    python referee_review... │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ 3. Commit & push to GitHub  │
│    git add .                │
│    git commit -m "Fix bug"  │
│    git push                 │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ 4. Create new version tag   │
│    git tag v1.0.1           │
│    git push origin v1.0.1   │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ 5. Wait 5-10 minutes        │
│    GitHub Actions builds    │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ 6. New release available!   │
│    Share with users         │
└─────────────────────────────┘
```

## Cost

**FREE!** 🎉

GitHub provides:
- Free Actions minutes: 2,000/month for free accounts
- Free storage for releases
- Free bandwidth for downloads

Your builds use approximately:
- 5-10 minutes per release × 3 platforms = 15-30 minutes
- You can do ~60+ releases per month on free tier

## Distribution Strategy

### Option 1: Direct GitHub Downloads
```
Users → GitHub Releases → Download → Run
```
✅ Always up to date
✅ Free hosting
✅ Version history
❌ Requires GitHub account to access (if private repo)

### Option 2: ORRA Website
```
You → Download from GitHub → Upload to orra.co.nz → Users download
```
✅ Direct ORRA branding
✅ No GitHub needed
❌ Manual update process

### Option 3: Hybrid
```
- Latest version on GitHub
- Stable release on ORRA website
- Best of both worlds!
```

## Automation Benefits

**Before GitHub Actions:**
- Install Python on 3 computers (Windows, Mac, Linux)
- Install PyInstaller on each
- Build manually on each
- Test each build
- Upload each to hosting
- **Time: 2-3 hours**

**With GitHub Actions:**
- Push code
- Create tag
- Wait 10 minutes
- **Done! All 3 platforms built and ready**

**Time saved: 2+ hours per release!**

---

This automation makes professional distribution accessible to everyone! 🚀
