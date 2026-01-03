# Quick Reference: Creating Releases

## One-Time Setup

1. Create GitHub repository
2. Upload files:
   - `referee_review_app.py`
   - `README.md`
   - `QUICK_START.md`
   - `requirements.txt`
   - `.gitignore`
3. Create `.github/workflows/build-releases.yml`

## Every Time You Want to Release

### Method 1: Via GitHub Website

1. Go to your repository
2. Click "Releases" → "Create a new release"
3. Click "Choose a tag" → Type version (e.g., `v1.0.0`)
4. Title: "Version 1.0.0"
5. Describe what's new
6. Click "Publish release"
7. Wait 5-10 minutes for builds to complete
8. Download files from Releases page

### Method 2: Via Git Command Line

```bash
# Make your code changes first, then:
git add .
git commit -m "Description of changes"
git push

# Create and push tag
git tag v1.0.0
git push origin v1.0.0

# Wait for builds, then check Releases page
```

## What You Get

After 5-10 minutes, your Releases page will have:

- ✅ `orra-referee-review-windows.zip` - For Windows users
- ✅ `orra-referee-review-macos.zip` - For Mac users  
- ✅ `orra-referee-review-linux.tar.gz` - For Linux users

All ready to download and use - **no Python installation required!**

## Sharing with ORRA

Give members this URL:
```
https://github.com/YOUR-USERNAME/orra-referee-review/releases
```

They click the latest release and download for their OS.

## Version Numbers

- `v1.0.0` - First release
- `v1.0.1` - Bug fix
- `v1.1.0` - New feature
- `v2.0.0` - Major update

## Troubleshooting

**Build failed?**
→ Actions tab → Click failed workflow → Read error log

**Mac security warning?**
→ Right-click app → Open → Click "Open" in dialog

**Windows security warning?**
→ Click "More info" → "Run anyway"

---

**That's it! Push tag → Wait 10 mins → Share downloads** 🚀
