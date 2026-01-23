# Rugby Referee Review System v2.1.0-alpha2

## 🎯 Individual Development Plan Feature + UI Improvements

Alpha Release 2 introduces a complete **Individual Development Plan (IDP)** builder and significant keyboard navigation improvements!

### ✨ What's New in Alpha 2:

**📋 Individual Development Plan (IDP)**
- **Guided IDP wizard** with 9 sections
- Thoughtful questions that prompt reflection and goal-setting
- Section-by-section navigation with progress tracking
- **SMART goal guidance** for 3 key focus areas
- Auto-save to JSON
- **Export to Word** matching ORRA template format
- Edit existing IDP anytime
- Separate from reviews (not counted in stats)

**⌨️ Keyboard Navigation**
- **Tab key** now moves between text fields (no more tab characters!)
- **Enter key** activates focused buttons
- Complete keyboard workflow - no mouse needed
- Works in both reviews and IDP

**🖥️ Window Improvements**
- App now opens **maximized** (fullscreen)
- All content visible without resizing
- Better use of screen space

**🐛 Bug Fixes**
- Fixed IDP count appearing in review statistics
- Fixed initialization order crash
- Added mousewheel scrolling to IDP wizard
- Icon now displays in window title bar and taskbar

### IDP Sections:

**Current Reality (3 sections):**
1. **Club Level** - Your current club status and goals
2. **Representative** - Rep involvement and aspirations  
3. **Aspirations** - Ultimate goals and this season's targets

**The How (3 sections):**
4. **Fitness** - Fitness level, Bronco targets, training plan
5. **Law** - Confidence, weak areas, development plan
6. **Mental** - Strengths, challenges, resilience building

**Focus Areas (3 sections):**
7-9. **Three SMART Goals** - Specific, measurable development targets
   - Why important
   - How to achieve
   - How to track
   - Obstacles and solutions

### Also Includes (from Alpha 1):

**Core Features:**
- ✅ CRRDF framework implementation
- ✅ GFA performance tracking
- ✅ Review history and search
- ✅ Analytics dashboard
- ✅ Excel export
- ✅ Home screen with quick actions
- ✅ Keyboard shortcuts (Ctrl+H, Ctrl+N, Ctrl+D, etc.)
- ✅ Status bar feedback
- ✅ Personal setup and auto-fill

---

## 📥 Download:
- **Windows:** `rugby-referee-review-windows.zip`
- **macOS:** `rugby-referee-review-macos.zip`
- **Linux:** `rugby-referee-review-linux.tar.gz`

---

## 🚀 Quick Start:

### Creating Your IDP:
1. Home screen → Click "Create Development Plan"
2. Work through 9 guided sections
3. Answer thoughtful questions for each
4. Save draft anytime
5. Complete and export to Word

### Keyboard Navigation:
- **Tab** - Move between fields
- **Enter** - Click focused button
- **Ctrl+D** - Open IDP
- **Ctrl+H** - Home screen
- **Ctrl+N** - New review

---

## ⚠️ Alpha Release Notes:

**This is alpha software - please test and report issues!**

### Known Limitations:
- IDP cannot be customized per region yet
- No progress tracking between IDP checkpoints
- No linking between reviews and IDP focus areas
- Limited validation on SMART goals

### Testing Focus:
We need feedback on:
1. **IDP workflow:** Is the guided approach helpful?
2. **Questions:** Are they clear and useful?
3. **Keyboard navigation:** Does Tab/Enter work as expected?
4. **Word export:** Does it match ORRA template properly?
5. **Any crashes or bugs**

---

## 🐛 Report Issues:
- Help → Report Issue in app
- GitHub: https://github.com/agclarkson/ReviewApp/issues

---

## 📋 What's Next for Beta:

**Planned features:**
- IDP progress tracking (quarterly check-ins)
- Link reviews to IDP focus areas
- Review suggestions based on weak areas
- Analytics tied to IDP goals
- Regional customization for game grades
- PDF export option
- Review comparison tool

---

## 🔄 Upgrade from Alpha 1:

Your existing data is preserved:
- All reviews remain intact
- Settings unchanged
- Create your first IDP!
- Enjoy improved keyboard navigation

---

## 📖 Documentation:
- `README.md` - Complete user guide
- `QUICK_START.md` - Fast start guide
- `DEVELOPMENT.md` - Technical documentation

---

## 💾 Data Storage:

**Reviews:** `Documents/RugbyRefereeReviews/*.json`
**IDP:** `Documents/RugbyRefereeReviews/idp.json`
**Config:** `~/.rugby_referee_review_config.json`
**Exports:** Wherever you save them

---

## ⚙️ System Requirements:

**Minimum:**
- Windows 10+ / macOS 10.14+ / Ubuntu 20.04+
- 4GB RAM
- 100MB disk space
- 1280x720 display (app opens maximized)

**Recommended:**
- 8GB RAM
- 1920x1080 display or larger
- Mouse with scroll wheel

---

## 📜 License:
MIT License - Free and open source

---

## 🙏 Acknowledgments:
- Based on CRRDF Framework
- ORRA IDP template
- Alpha testers for valuable feedback

---

## ⌨️ Keyboard Shortcuts Reference:

| Shortcut | Action |
|----------|--------|
| Ctrl+H | Home |
| Ctrl+N | New Review |
| Ctrl+D | Development Plan |
| Ctrl+B | Browse Reviews |
| Ctrl+Shift+A | Analytics |
| Ctrl+O | Open Review |
| F1 | About |
| Ctrl+Q | Quit |
| Tab | Next field |
| Enter | Activate button |

---

**Thank you for testing Alpha 2!** Your feedback helps make this tool better for the entire referee community. 🏉✨

**Questions or issues?** Open a GitHub issue or contact the developer.

---

**Copyright © 2025 Andrew Clarkson** | MIT License | Based on CRRDF Framework