# ORRA Referee Review System - Setup Guide

This repository contains everything needed to build and distribute the ORRA Referee Review application for Windows, Mac, and Linux.

## 📦 What's Included

```
orra-referee-review/
├── .github/
│   └── workflows/
│       └── build-releases.yml          # GitHub Actions workflow for builds
├── docs/
│   ├── GITHUB_SETUP.md                 # Detailed GitHub setup instructions
│   ├── RELEASE_QUICK_REF.md            # Quick reference for releases
│   ├── WORKFLOW_DIAGRAM.md             # Visual workflow explanation
│   ├── GFA_DESCRIPTIONS.md             # GFA scoring details
│   └── PLACEHOLDER_FEATURE.md          # UI feature documentation
├── referee_review_app.py               # Main application
├── launch_review_app.bat               # Windows launcher
├── launch_review_app.sh                # Mac/Linux launcher
├── requirements.txt                     # Python dependencies
├── .gitignore                          # Git ignore rules
├── README.md                           # User documentation
├── QUICK_START.md                      # Quick start guide
├── PROJECT_OVERVIEW.md                 # Development overview
├── ORRA_Referee_Review_System_Documentation.docx  # Word documentation
└── SETUP.md                            # This file
```

## 🚀 Quick Start (3 Options)

### Option 1: Use Pre-Built Releases (Recommended for Users)

1. Go to the [Releases page](../../releases)
2. Download the latest version for your operating system
3. Extract and run - no Python needed!

### Option 2: Run from Source (For Development)

1. Install Python 3.7+ from https://python.org
2. Clone this repository
3. Run the launcher:
   - Windows: Double-click `launch_review_app.bat`
   - Mac/Linux: Double-click `launch_review_app.sh`

### Option 3: Set Up GitHub Actions (For Maintainers)

Follow the detailed guide in [`docs/GITHUB_SETUP.md`](docs/GITHUB_SETUP.md)

## 📋 For Repository Maintainers

### Initial Setup

1. **Create GitHub repository** (if not already done)
   ```bash
   # On GitHub: Create new repository named 'orra-referee-review'
   ```

2. **Clone and add files**
   ```bash
   git clone https://github.com/YOUR-USERNAME/orra-referee-review.git
   cd orra-referee-review
   # Copy all files from this package into the repository
   ```

3. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit - ORRA Referee Review System"
   git push origin main
   ```

4. **Verify GitHub Actions**
   - Go to repository → Actions tab
   - Confirm workflow file is recognized

### Creating Releases

#### Method 1: Tag-Based Release (Automatic)

```bash
# Update version and push
git add .
git commit -m "Version 1.0.0"
git push

# Create and push tag
git tag v1.0.0
git push origin v1.0.0
```

GitHub Actions automatically:
- Builds for Windows, Mac, Linux
- Creates release with downloads
- Takes 5-10 minutes

#### Method 2: Manual Trigger

1. Go to repository → Actions
2. Select "Build Releases" workflow
3. Click "Run workflow"
4. Select branch and run

### Release Checklist

Before creating a new release:

- [ ] Test application locally
- [ ] Update version number in code comments
- [ ] Update README.md if features changed
- [ ] Update QUICK_START.md if needed
- [ ] Commit all changes
- [ ] Create descriptive tag (v1.0.0, v1.1.0, etc.)
- [ ] Wait for builds to complete (~10 minutes)
- [ ] Test downloaded executables
- [ ] Announce to ORRA members

## 📝 Version Numbering

Use semantic versioning: `vMAJOR.MINOR.PATCH`

- **v1.0.0** - Initial release
- **v1.0.1** - Bug fixes, small updates
- **v1.1.0** - New features, backwards compatible
- **v2.0.0** - Major changes, breaking updates

## 🔧 Customization

### Modifying the Application

Edit `referee_review_app.py`:

**Add Questions:**
```python
CRRDF_QUESTIONS = {
    "technical": {
        "questions": [
            # Add your questions here
        ]
    }
}
```

**Modify GFA Categories:**
```python
GFA_CATEGORIES = {
    "Category Name": [
        ("Aspect", "Description"),
    ]
}
```

**Change Rating Scale:**
```python
RATING_SCALE = {
    1: "Your description",
    # etc.
}
```

### Modifying the Build Process

Edit `.github/workflows/build-releases.yml`:

**Add dependencies:**
```yaml
- name: Install dependencies
  run: |
    pip install pyinstaller openpyxl your-new-library
```

**Include additional files:**
```yaml
copy YourFile.txt release\\  # Windows
cp YourFile.txt release/     # Mac/Linux
```

**Add an icon:**
```yaml
pyinstaller --onefile --windowed --icon=icon.ico --name="ORRA Referee Review" referee_review_app.py
```

## 📖 Documentation

- **For Users:**
  - [`README.md`](README.md) - Complete user guide
  - [`QUICK_START.md`](QUICK_START.md) - Fast-track guide
  - [`ORRA_Referee_Review_System_Documentation.docx`](ORRA_Referee_Review_System_Documentation.docx) - Printable guide

- **For Developers:**
  - [`PROJECT_OVERVIEW.md`](PROJECT_OVERVIEW.md) - Technical overview
  - [`docs/GITHUB_SETUP.md`](docs/GITHUB_SETUP.md) - GitHub Actions setup
  - [`docs/WORKFLOW_DIAGRAM.md`](docs/WORKFLOW_DIAGRAM.md) - Build process
  - [`docs/GFA_DESCRIPTIONS.md`](docs/GFA_DESCRIPTIONS.md) - GFA details

- **Quick Reference:**
  - [`docs/RELEASE_QUICK_REF.md`](docs/RELEASE_QUICK_REF.md) - One-page release guide

## 🐛 Troubleshooting

### GitHub Actions Issues

**Build fails:**
1. Go to Actions tab
2. Click failed workflow
3. Check error logs
4. Common issues:
   - Syntax error in Python code
   - Missing dependencies in requirements.txt
   - Incorrect file paths in workflow

**Release not created:**
- Check if tag starts with 'v' (v1.0.0, not 1.0.0)
- Verify GITHUB_TOKEN permissions
- Ensure workflow completed successfully

### Local Testing Issues

**Application won't start:**
```bash
# Check Python version
python --version  # or python3 --version

# Install dependencies
pip install -r requirements.txt

# Run with error output
python referee_review_app.py
```

**Module not found:**
```bash
pip install openpyxl
```

## 💡 Tips

### For ORRA Administrators

1. **Keep releases clean**: Only create releases for tested versions
2. **Use pre-releases**: Mark beta versions as "pre-release"
3. **Write clear release notes**: Users appreciate knowing what changed
4. **Archive old releases**: Keep history but highlight current version

### For Developers

1. **Test locally first**: Run app before creating release
2. **Use branches**: Develop in branches, merge to main for releases
3. **Document changes**: Update docs when adding features
4. **Version consistently**: Follow semantic versioning

### For Users

1. **Always download latest**: Check releases page for updates
2. **Keep reviews**: Save Excel files for your records
3. **Provide feedback**: Report issues to help improve the app
4. **Share successes**: Tell others about useful features

## 📞 Support

### Technical Issues
- Check [`docs/GITHUB_SETUP.md`](docs/GITHUB_SETUP.md) for setup help
- Review GitHub Actions logs for build errors
- Consult Python error messages for runtime issues

### Questions
- Contact ORRA technical team
- Review documentation in `docs/` folder
- Check GitHub Issues for similar problems

### Contributing
- Fork the repository
- Create feature branch
- Submit pull request with description

## 📜 License

Developed for Otago Rugby Referees Association (ORRA)

Based on:
- Community Rugby Referee Development Framework (NZR, Feb 2025)
- ORRA Premier Review Document Master template
- World Rugby match official development principles

## 🎯 Next Steps

1. [ ] Read [`docs/GITHUB_SETUP.md`](docs/GITHUB_SETUP.md) for detailed setup
2. [ ] Create first release (v1.0.0)
3. [ ] Test all three platform downloads
4. [ ] Share with ORRA members
5. [ ] Collect feedback for v1.1.0

---

**Everything is ready! Just push to GitHub and create your first release.** 🚀

For detailed instructions, see [`docs/GITHUB_SETUP.md`](docs/GITHUB_SETUP.md)
