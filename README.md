# Rugby Referee Review System

A desktop application for rugby referees to track their development using the Community Rugby Referee Development Framework (CRRDF).

**Version:** 2.0.8-alpha  
**License:** MIT  
**Author:** Andrew Clarkson

---

## Overview

This application helps rugby referees systematically review their performances and track improvement over time. Built around the CRRDF framework, it provides structured reflection prompts, performance scoring, and visual analytics.

## Features

### Review Creation
- Structured self-reflection across five CRRDF pillars
- GFA performance scoring (10 categories, 1-5 scale)
- Game metadata tracking (date, grade, result)
- Coach feedback section
- Excel export for sharing and archiving

### Performance Tracking
- Analytics dashboard with trend visualization
- Review history with search functionality
- Quick access to recent reviews
- Progress statistics

### User Experience
- Personal setup on first run (auto-fill referee/coach names)
- Keyboard shortcuts for navigation
- Status bar feedback
- Home screen with action overview

## Installation

### Requirements
- Windows 10+, macOS 10.14+, or Ubuntu 20.04+
- No additional dependencies for binary releases

### Download
Get the latest release for your platform:
- **Windows:** Extract ZIP, run `Rugby Referee Review.exe`
- **macOS:** Extract ZIP, run `Rugby Referee Review`
- **Linux:** Extract tarball, run `rugby-referee-review`

### First Run
On first launch, you'll enter:
- Your full name (auto-fills in reviews)
- Preferred coach name (optional)

This information can be updated later via Settings → Personal Info.

## Usage

### Creating a Review

1. **Home Screen:** Click "New Review" or press Ctrl+N
2. **Game Information:** Enter date, grade, result
3. **Self Reflection:** Answer general reflection questions
4. **CRRDF Pillars:** Work through 5 pillars (Technical, Tactical, Management, Mental, Physical)
5. **GFA Performance:** Rate yourself in 10 key areas
6. **Coach Feedback:** Add notes from your coach
7. **Save & Export:** Generates Excel file and saves JSON for history

### Viewing Analytics

Access via home screen or File → View Analytics (Ctrl+Shift+A)

Displays:
- Total review count and date range
- GFA score trends over time
- Performance statistics
- Recent review summary

### Managing Reviews

**Browse Reviews** (Ctrl+B):
- View all saved reviews
- Search by name, date, or grade
- Load existing reviews to edit
- Delete unwanted reviews

**Recent Reviews:**
Quick access to your last 5 reviews from the home screen

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+H | Home screen |
| Ctrl+N | New review |
| Ctrl+O | Open review |
| Ctrl+B | Browse reviews |
| Ctrl+Shift+A | Analytics |
| F1 | About |
| Ctrl+Q | Quit |

## Data Storage

**Reviews:** `Documents/RugbyRefereeReviews/`
- Format: JSON (for app) + Excel (for export)
- Filename: `Review_[Name]_[Date].json`

**Settings:** `~/.rugby_referee_review_config.json`
- Contains name, coach, and preferences
- Can be deleted to reset first-run setup

## Game Grades

Currently configured for Otago region:
- Division 1, 2, 3
- Southern Premier, Central Premier
- Women's Division 1, 2
- Premier 1st XV
- U20 Colts, U21 Colts Division 1, 2
- High School
- Other

To customize for your region, edit the `GAME_GRADES` list in the source code (future versions will support UI configuration).

## CRRDF Framework

The Community Rugby Referee Development Framework structures development across five pillars:

1. **Technical** - Law application, decision accuracy
2. **Tactical** - Game management, positioning
3. **Management** - Player interactions, communication
4. **Mental** - Confidence, focus, resilience
5. **Physical** - Fitness, positioning, stamina

Each pillar includes guided reflection questions to encourage systematic improvement.

## GFA Performance Areas

Game, Form & Appearance scoring covers:
- Game Management
- Communication & Signals
- Advantage Application
- Positioning & Angles
- Physical Fitness
- Scrum Management
- Tackle/Breakdown
- Maul Management
- Offside Lines
- Penalty Decisions

Ratings: 1 (Unsatisfactory) to 5 (Excellent)

## Troubleshooting

### Windows Security Warning
Windows Defender may show "Unknown Publisher" for unsigned applications.
- Click "More info" → "Run anyway"
- This is standard for open-source software without code signing certificates

### Antivirus False Positives
Some antivirus software may flag PyInstaller-built executables.
- This is a known issue with PyInstaller
- Add an exception if needed
- Source code is available for inspection

### Reviews Won't Load
- Check file isn't corrupted
- Ensure it's a valid JSON file from this application
- Try opening a different review

### Analytics Not Displaying
- Requires at least one completed review
- Verify reviews saved to correct directory
- Check GFA scores are present in reviews

### Icon Not Showing
If the window icon doesn't appear, ensure `icon.ico` exists in the application directory (should be bundled automatically).

## Development

### Building from Source

**Requirements:**
```bash
pip install openpyxl ttkbootstrap pillow matplotlib
```

**Run:**
```bash
python referee_review_app.py
```

**Build Executable:**
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "Rugby Referee Review" --icon icon.ico --add-data "icon.ico;." referee_review_app.py
```

### Project Structure
```
ReviewApp/
├── referee_review_app.py    # Main application
├── icon.ico                  # Windows icon
├── icon.iconset/             # macOS icon
├── icon_512.png              # Linux icon
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── QUICK_START.md            # Quick reference guide
└── .github/
    └── workflows/
        └── build-releases.yml # CI/CD configuration
```

### Contributing

Issues and feature requests: [GitHub Issues](https://github.com/agclarkson/ReviewApp/issues)

When reporting bugs, include:
- Operating system and version
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if applicable

## Roadmap

Future enhancements under consideration:
- Regional grade configuration via UI
- PDF export option
- Review comparison tool
- Goal tracking system
- Multi-language support

## License

MIT License - see LICENSE file for details.

## Acknowledgments

Based on the Community Rugby Referee Development Framework (CRRDF).

---

**For questions or support:** Open an issue on GitHub or contact the developer.