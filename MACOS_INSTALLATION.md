# Installing on macOS

## Two Ways to Install:

### Option 1: DMG (Recommended)
1. Download `rugby-referee-review-macos.dmg`
2. Double-click the DMG to mount it
3. Drag the app to your Applications folder
4. Follow security steps below

### Option 2: ZIP
1. Download `rugby-referee-review-macos.zip`
2. Extract the ZIP file
3. Drag "Rugby Referee Review.app" to Applications
4. Follow security steps below

---

## ⚠️ First Time Opening (Required)

macOS will show a security warning because this app isn't signed with an Apple Developer certificate.

### Method 1: System Settings (Easiest)

1. Try to open the app (it will be blocked)
2. A dialog will say "cannot be opened because the developer cannot be verified"
3. Click **"OK"**
4. Go to **System Settings** → **Privacy & Security**
5. Scroll down to the **Security** section
6. You'll see a message about the blocked app
7. Click **"Open Anyway"**
8. Click **"Open"** in the confirmation dialog
9. The app will now open and work normally!

### Method 2: Right-Click (Alternative)

1. Find the app in Finder
2. **Right-click** (or Control+click) on the app
3. Select **"Open"** from the menu
4. Click **"Open"** in the security dialog
5. The app will open!

### Method 3: Terminal (For Tech Users)

```bash
# Remove quarantine flag
xattr -d com.apple.quarantine "/Applications/Rugby Referee Review.app"
```

---

## ✅ After First Opening

Once you've opened the app using one of the methods above, macOS will remember your choice. You can open it normally from now on (double-click, Launchpad, etc.).

---

## ❓ Why This Happens

This app is **not code-signed** with an Apple Developer certificate ($99/year). The app is safe - it's just not notarized by Apple.

**macOS Gatekeeper blocks all unsigned apps by default to protect users.**

---

## 🔐 Is This Safe?

Yes! This is open-source software. You can:
- View the source code on GitHub
- See exactly what the app does
- Build it yourself if you prefer

The security warning is just Apple's way of saying "we haven't verified this developer."

---

## 🐛 Still Having Issues?

**App won't open at all:**
- Make sure you extracted the ZIP completely
- Make sure the .app is in /Applications folder
- Try Method 3 (Terminal) above

**Can't find "Open Anyway" button:**
- You need macOS 10.15 (Catalina) or later
- Try Method 2 (right-click Open) instead

**Other problems:**
- Open an issue on GitHub
- Email support with details

---

## 📱 System Requirements

- macOS 10.15 (Catalina) or later
- Apple Silicon (M1/M2/M3) or Intel processor
- ~50MB free disk space

---

**Once installed, enjoy your referee reviews!** 🏉✨
