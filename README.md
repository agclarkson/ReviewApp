# Rugby Referee Review System

A desktop application for rugby referees to track their development using the Community Rugby Referee Development Framework (CRRDF) and create Individual Development Plans (IDPs).

**Version:** 2.1.0-alpha2  
**License:** MIT  
**Author:** Andrew Clarkson

---

## Overview

This application helps rugby referees systematically review their performances, set development goals, and track improvement over time. Built around the CRRDF framework with integrated IDP planning, it provides structured reflection prompts, performance scoring, visual analytics, and guided goal-setting.

## Features

### Review Creation
- Structured self-reflection across five CRRDF pillars
- GFA performance scoring (10 categories, 1-5 scale)
- Game metadata tracking (date, grade, result)
- Coach feedback section
- Excel export for sharing and archiving

### Individual Development Plan (IDP) - NEW in Alpha 2
- **Guided IDP wizard** with thoughtful questions that prompt reflection
- 9 sections covering Current Reality, The How, and Focus Areas
- SMART goal guidance for measurable development targets
- Auto-save to JSON format
- **Export to Word** matching ORRA template format
- Edit and update IDP throughout the season
- Separate from reviews (not counted in statistics)

### Performance Tracking
- Analytics dashboard with trend visualization
- Review history with search functionality
- Quick access to recent reviews
- Progress statistics

### User Experience
- Personal setup on first run (auto-fill referee/coach names)
- Keyboard shortcuts for navigation
- **Tab/Enter keyboard workflow** - navigate entire app without mouse
- Status bar feedback
- Home screen with action overview
- Opens maximized for full visibility

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

**Keyboard Tip:** Use **Tab** to move between fields and **Enter** to click buttons - no mouse needed!

### Creating Your Individual Development Plan

1. **Home Screen:** Click "Create Development Plan" or press Ctrl+D
2. **Current Reality (3 sections):**
   - Club level: Describe your current status and goals
   - Representative: Detail your rep involvement and aspirations
   - Aspirations: Define your ultimate goals and this season's targets
3. **The How (3 sections):**
   - Fitness: Plan your fitness development and set targets (e.g., Bronco time)
   - Law: Assess knowledge and plan improvements
   - Mental: Identify strengths and build resilience
4. **Focus Areas (3 sections):**
   - Set 3 SMART goals with specific, measurable targets
   - Explain why each is important
   - Define how you'll achieve and track progress
   - Identify obstacles and solutions
5. **Save & Export:** Saves to JSON and exports to Word

**Guided Questions:**
Each section has thoughtful prompts with help text and examples to guide your reflection and goal-setting.

### Editing Your IDP

Your IDP button on the home screen will show "Edit Development Plan" once created:
1. Click to open wizard
2. Navigate to any section
3. Update your answers
4. Save changes
5. Re-export to Word if needed

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
| Ctrl+D | Development Plan |
| Ctrl+O | Open review |
| Ctrl+B | Browse reviews |
| Ctrl+Shift+A | Analytics |
| F1 | About |
| Ctrl+Q | Quit |
| **Tab** | **Next field** |
| **Enter** | **Click focused button** |

**Full keyboard navigation:** You can use the entire app without touching your mouse!

## Data Storage

**Reviews:** `Documents/RugbyRefereeReviews/`
- Format: JSON (for app) + Excel (for export)
- Filename: `Review_[Name]_[Date].json`

**IDP:** `Documents/RugbyRefereeReviews/idp.json`
- Single IDP file per user
- Saved separately from reviews
- Not counted in review statistics

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

## Individual Development Plan Structure

### Current Reality (3 sections)

**Club Level:**
- What level do you currently referee?
- How would you describe your performances?
- What are your main challenges?
- Where do you want to be by end of season?

**Representative:**
- What's your current rep involvement?
- Tell us about your rep experience
- What are your rep goals this year?

**Aspirations:**
- What's your ultimate refereeing goal?
- What's realistic for this season?
- What would success look like this year?

### The How (3 sections)

**Fitness:**
- Current fitness level and Bronco test time
- Training frequency and types
- Specific fitness targets
- Obstacles and how to overcome them

**Law Knowledge:**
- Confidence level (1-5)
- Areas needing work
- Consistency challenges
- Development plan

**Mental Game:**
- Mental strengths
- What affects your performance mentally
- How you'll build resilience

### Focus Areas (3 sections)

Each focus area requires:
- **Category:** Fitness, Law, Mental, Positioning, Communication, etc.
- **Specific area:** What exactly you're focusing on
- **Why important:** How this helps achieve your aspirations
- **SMART goal:** Specific, Measurable, Achievable, Relevant, Time-bound
- **How to achieve:** Specific actions, frequency, timeline
- **How to track:** Measurement method
- **Obstacles:** What might stop you and how you'll overcome it

**Example SMART Goals:**
- "Achieve 5:30 Bronco test by June 2025"
- "Referee 10 Division 2 games this season"
- "Get positive positioning feedback from 3 different coaches"

## Troubleshooting

### Windows Security Warning
Windows Defender may show "Unknown Publisher" for unsigned applications.
- Click "More info" → "Run anyway"
- This is normal for open-source software without code signing certificates

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

### IDP Won't Export to Word
- Ensure you have disk space available
- Try saving to a different location
- Check that python-docx is installed (bundled in releases)

### Scrolling Not Working
- Use mouse wheel in IDP sections
- Ensure you're clicking inside the scrollable content area
- Use the scrollbar if wheel doesn't work

### Icon Not Showing
- Icon should be bundled automatically in releases
- If building from source, ensure icon files are present

### App Opens Too Small
- App should open maximized automatically
- If not, maximize the window manually
- Future updates will remember window state

## Development

### Building from Source

**Requirements:**
```bash
pip install -r requirements.txt
```

**Contents of requirements.txt:**
```
openpyxl>=3.1.2
ttkbootstrap>=1.10.1
pillow>=10.0.0
matplotlib>=3.8.0
python-docx>=0.8.11
```

**Run:**
```bash
python referee_review_app.py
```

**Build Executable:**

**Windows:**
```cmd
pyinstaller --onefile --windowed --name "Rugby Referee Review" --icon icon.ico --add-data "icon.ico;." referee_review_app.py
```

**macOS:**
```bash
pyinstaller --onefile --windowed --name "Rugby Referee Review" --icon icon.icns --add-data "icon.icns:." referee_review_app.py
```

**Linux:**
```bash
pyinstaller --onefile --windowed --name "rugby-referee-review" --icon icon_512.png --add-data "icon_512.png:." referee_review_app.py
```

### Project Structure
```
ReviewApp/
├── referee_review_app.py    # Main application (2,898 lines)
├── icon.ico                  # Windows icon
├── icon.iconset/             # macOS icon source
├── icon_512.png              # Linux icon
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── QUICK_START.md            # Quick reference guide
├── DEVELOPMENT.md            # Technical documentation
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

### Alpha 2 Status
This is an alpha release for testing. Known limitations:
- IDP cannot be customized per region yet
- No progress tracking between IDP checkpoints
- No linking between reviews and IDP focus areas
- Limited validation on SMART goals

### Beta Release Goals
- IDP progress tracking (quarterly check-ins)
- Link reviews to IDP focus areas
- Review suggestions based on weak areas
- Analytics tied to IDP goals
- Regional grade configuration via UI
- PDF export option
- Review comparison tool

### 1.0 Release Goals
- Stable, tested codebase
- Complete documentation
- Code signing (if budget permits)
- Installer packages
- Multi-language support (if demand exists)

## Alpha Testing

**We need your feedback on:**
1. IDP workflow - Is the guided approach helpful?
2. Questions - Are they clear and useful?
3. Keyboard navigation - Does Tab/Enter work as expected?
4. Word export - Does it match ORRA template properly?
5. Any crashes or bugs

**How to report:**
- Help → Report Issue in the app
- GitHub Issues: https://github.com/agclarkson/ReviewApp/issues

## License

MIT License - see LICENSE file for details.

Copyright © 2025 Andrew Clarkson

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Acknowledgments

This application is based on:
- **Community Rugby Referee Development Framework (CRRDF)** - Structured development approach
- **ORRA Individual Development Plan Template** - IDP format and structure

Special thanks to:
- CRRDF framework developers
- Otago Rugby Referees Association
- Alpha testers providing valuable feedback
- The rugby referee community

## System Requirements

**Minimum:**
- Windows 10+ / macOS 10.14+ / Ubuntu 20.04+
- 4GB RAM
- 100MB disk space
- 1280x720 display

**Recommended:**
- 8GB RAM
- 1920x1080 display or larger
- SSD for faster loading
- Mouse with scroll wheel

## Support

**Documentation:**
- README.md - Complete guide (this file)
- QUICK_START.md - Fast introduction
- DEVELOPMENT.md - Technical documentation

**Get Help:**
- Check the troubleshooting section above
- Review QUICK_START.md for common tasks
- Open an issue on GitHub
- Use Help → Report Issue in the app

**Community:**
- GitHub Issues for bugs and features
- Source code available for inspection
- Contributions welcome

---

**For questions or support:** Open an issue on GitHub or contact the developer.

**Version:** 2.1.0-alpha2  
**Last Updated:** January 2025  
**Copyright © 2025 Andrew Clarkson**