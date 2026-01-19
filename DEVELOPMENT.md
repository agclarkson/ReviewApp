# Developer Documentation

Technical documentation for Rugby Referee Review System development.

---

## Architecture

### Technology Stack

**Core:**
- Python 3.11+
- tkinter (GUI framework)
- ttkbootstrap (modern themed widgets)

**Data:**
- JSON (review storage)
- openpyxl (Excel export)
- Pathlib (file system operations)

**Visualization:**
- matplotlib (charts and graphs)
- TkAgg backend (embedded in tkinter)

**Build:**
- PyInstaller (executable generation)
- GitHub Actions (CI/CD)

### Application Structure

```
ReviewApp/
├── referee_review_app.py       # Main application (2000+ lines)
│   ├── ReviewSession           # Data model
│   ├── CRRDFReviewApp          # Main application class
│   ├── PlaceholderEntry/Text   # Custom widgets
│   └── Utility functions       # Helpers
│
├── Resources/
│   ├── icon.ico                # Windows icon
│   ├── icon.iconset/           # macOS icon source
│   └── icon_512.png            # Linux icon
│
├── Configuration/
│   ├── requirements.txt        # Python dependencies
│   └── .github/workflows/      # CI/CD pipeline
│
└── Documentation/
    ├── README.md               # User documentation
    ├── QUICK_START.md          # Quick reference
    └── DEVELOPMENT.md          # This file
```

### Code Organization

**Data Model (ReviewSession):**
- Stores review state (metadata, goals, reflections, scores)
- Serializable to JSON
- No business logic

**UI Layer (CRRDFReviewApp):**
- tkinter-based interface
- Screen management (home, metadata, pillars, etc.)
- Event handling
- File I/O coordination

**Screens:**
- Home screen
- Metadata entry
- Self reflection
- CRRDF pillar navigation
- GFA scoring
- Analytics dashboard
- Review browser

---

## Development Setup

### Prerequisites

```bash
# Python 3.11 or higher
python --version

# pip package manager
pip --version
```

### Clone and Setup

```bash
# Clone repository
git clone https://github.com/agclarkson/ReviewApp.git
cd ReviewApp

# Install dependencies
pip install -r requirements.txt

# Run application
python referee_review_app.py
```

### Dependencies

**Runtime:**
- `openpyxl>=3.1.2` - Excel file generation
- `ttkbootstrap>=1.10.1` - Modern themed widgets
- `pillow>=10.0.0` - Image handling
- `matplotlib>=3.8.0` - Chart generation

**Development:**
- `pyinstaller` - Executable building

### Development Workflow

```bash
# 1. Create feature branch
git checkout -b feature/your-feature

# 2. Make changes
# Edit referee_review_app.py

# 3. Test locally
python referee_review_app.py

# 4. Commit
git add .
git commit -m "Description of changes"

# 5. Push
git push origin feature/your-feature

# 6. Create pull request (if collaborative)
```

---

## Building Executables

### Local Build

**Windows:**
```cmd
pyinstaller --onefile --windowed ^
  --name "Rugby Referee Review" ^
  --icon icon.ico ^
  --add-data "icon.ico;." ^
  referee_review_app.py
```

**macOS:**
```bash
pyinstaller --onefile --windowed \
  --name "Rugby Referee Review" \
  --icon icon.icns \
  --add-data "icon.icns:." \
  referee_review_app.py
```

**Linux:**
```bash
pyinstaller --onefile --windowed \
  --name "rugby-referee-review" \
  --icon icon_512.png \
  --add-data "icon_512.png:." \
  referee_review_app.py
```

**Output:** `dist/` directory contains executable

### CI/CD Pipeline

**Trigger:** Push tag matching `v*`

**Process:**
1. Checkout code
2. Setup Python 3.11
3. Install dependencies
4. Build for Windows, macOS, Linux (parallel)
5. Package binaries (ZIP/tarball)
6. Create GitHub release
7. Upload artifacts

**Configuration:** `.github/workflows/build-releases.yml`

**Manual trigger:** GitHub Actions → Run workflow

---

## Code Structure

### Main Components

**ReviewSession Class:**
```python
class ReviewSession:
    metadata: dict          # Game info
    goals: dict            # Primary/secondary goals
    difficulty: int        # 1-10 scale
    reflections: dict      # General reflections
    crrdf_reflections: dict # Pillar answers
    gfa_scores: dict       # Performance ratings
    coach_feedback: str    # Coach notes
```

**CRRDFReviewApp Class:**
```python
class CRRDFReviewApp:
    root: tk.Tk                    # Main window
    session: ReviewSession         # Current review
    content: tk.Frame             # Content area
    status_bar: tk.Label          # Status display
    config: dict                  # User settings
    reviews_dir: Path             # Storage location
    
    # Screens
    show_home_screen()
    show_metadata_entry()
    show_self_reflection()
    show_pillar_questions()
    show_gfa_scoring()
    
    # File operations
    save_review_json()
    load_review_json()
    export_to_excel()
    
    # Utilities
    update_status()
    clear_content()
```

### Data Flow

```
User Input → ReviewSession → JSON File
                 ↓
            Excel Export
                 ↓
         Analytics Dashboard
```

### Storage Format

**JSON Review File:**
```json
{
  "version": "2.0.8-alpha",
  "saved_at": "2025-01-14T10:30:00",
  "metadata": {
    "game_grade": "Division 1",
    "date": "2025-01-14",
    "result": "Home 24-17 Away",
    "referee": "John Smith",
    "coach": "Jane Doe"
  },
  "goals": {
    "primary": "Improve breakdown decisions",
    "secondary": "Better communication"
  },
  "difficulty": 7,
  "reflections": { ... },
  "crrdf_reflections": { ... },
  "gfa_scores": { ... },
  "coach_feedback": "..."
}
```

**Config File:**
```json
{
  "first_run": false,
  "user_name": "John Smith",
  "coach_name": "Jane Doe"
}
```

---

## Adding Features

### Example: Add New Screen

```python
def show_new_screen(self):
    """Show a new screen"""
    # Clear existing content
    self.clear_content()
    
    # Update status
    self.update_status("New screen loaded")
    
    # Create UI
    frame = tk.Frame(self.content, bg="white")
    frame.pack(fill=tk.BOTH, expand=True)
    
    # Add widgets
    tk.Label(frame, text="New Screen", 
            font=("Segoe UI", 16, "bold")).pack(pady=20)
    
    # Add to menu if needed
    # file_menu.add_command(label="New Screen", 
    #                      command=self.show_new_screen)
```

### Example: Add Data Field

```python
# 1. Add to ReviewSession
class ReviewSession:
    def __init__(self):
        # ... existing fields ...
        self.new_field = ""

# 2. Collect in UI
entry = tk.Entry(frame)
entry.pack()
# ... later ...
self.session.new_field = entry.get()

# 3. Include in JSON
review_data = {
    # ... existing fields ...
    "new_field": self.session.new_field
}

# 4. Load from JSON
self.session.new_field = data.get('new_field', '')
```

### Example: Add Menu Item

```python
def create_menu_bar(self):
    # ... existing menus ...
    
    # Add to File menu
    file_menu.add_command(
        label="New Action",
        command=self.new_action_handler,
        accelerator="Ctrl+X"
    )
    
    # Bind keyboard shortcut
    self.root.bind('<Control-x>', 
                   lambda e: self.new_action_handler())
```

---

## Testing

### Manual Testing Checklist

**First Run:**
- [ ] Welcome screen appears
- [ ] Name/coach saved correctly
- [ ] Home screen loads

**Review Creation:**
- [ ] All fields accessible
- [ ] Data persists between screens
- [ ] GFA sliders work
- [ ] Export generates valid Excel
- [ ] JSON saves correctly

**Review Management:**
- [ ] Browse shows all reviews
- [ ] Search filters correctly
- [ ] Load populates fields
- [ ] Delete removes file
- [ ] Recent reviews update

**Analytics:**
- [ ] Opens without errors
- [ ] Charts render correctly
- [ ] Stats accurate
- [ ] Handles empty data

**Keyboard Shortcuts:**
- [ ] All shortcuts function
- [ ] Shown in menus
- [ ] No conflicts

**Cross-Platform:**
- [ ] Windows build works
- [ ] macOS build works
- [ ] Linux build works
- [ ] Icons appear correctly

### Common Issues

**Import Errors:**
```bash
# Missing dependency
pip install [package]

# Wrong Python version
python --version  # Should be 3.11+
```

**Build Errors:**
```bash
# PyInstaller not found
pip install pyinstaller

# Icon not found
# Ensure icon files in repo root
```

**Runtime Errors:**
```python
# Add error handling
try:
    risky_operation()
except Exception as e:
    print(f"Error: {e}")
    messagebox.showerror("Error", str(e))
```

---

## Version Management

### Version Format

`MAJOR.MINOR.PATCH-STAGE`

Examples:
- `2.0.8-alpha` - Alpha release
- `2.1.0-beta` - Beta release
- `2.1.0` - Stable release

### Release Process

1. **Update version in code:**
   ```python
   __version__ = "2.0.9-alpha"
   ```

2. **Update documentation**
   - README.md
   - RELEASE_NOTES.md

3. **Commit and tag:**
   ```bash
   git add .
   git commit -m "Release v2.0.9-alpha"
   git tag v2.0.9-alpha
   git push origin main
   git push origin v2.0.9-alpha
   ```

4. **GitHub Actions builds automatically**

5. **Test downloads**

6. **Announce release**

---

## Code Style

### Conventions

**Naming:**
- Classes: `PascalCase`
- Functions: `snake_case`
- Constants: `UPPER_CASE`
- Private: `_leading_underscore`

**Docstrings:**
```python
def function_name(param1, param2):
    """Brief description.
    
    Args:
        param1: Description
        param2: Description
        
    Returns:
        Description of return value
    """
```

**Comments:**
- Use for why, not what
- Keep up to date with code
- Avoid obvious comments

**Formatting:**
- 4 spaces for indentation
- Max line length: 100 characters (flexible)
- Blank lines between functions

### UI Conventions

**Colors:**
- Primary: #1976D2 (blue)
- Success: #4CAF50 (green)
- Warning: #FF9800 (orange)
- Error: #F44336 (red)
- Background: #FAFAFA (light gray)

**Fonts:**
- Primary: Segoe UI
- Headers: Bold
- Sizes: 9-18pt

**Spacing:**
- Padding: 10-20px
- Margins: 20-40px
- Consistent throughout

---

## Performance

### Optimization Tips

**File I/O:**
- Use Path objects (faster than os.path)
- Batch operations when possible
- Cache review list when browsing

**UI:**
- Use pack() for simple layouts
- Avoid excessive widget creation
- Clear widgets before recreating

**Analytics:**
- Limit data points for charts
- Process in background if slow
- Cache calculations

### Profiling

```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# Code to profile
app.show_analytics_dashboard()

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(20)
```

---

## Security

### Data Privacy

- All data stored locally
- No network communication (except GitHub issues link)
- No telemetry or analytics
- User controls all data

### Input Validation

```python
# Validate dates
try:
    datetime.strptime(date_str, "%Y-%m-%d")
except ValueError:
    messagebox.showerror("Invalid Date", 
                        "Use format: YYYY-MM-DD")
    return

# Sanitize filenames
safe_name = "".join(c for c in name 
                   if c.isalnum() or c in (' ', '-', '_'))
```

### File Safety

- Use try/except for all file operations
- Validate JSON before loading
- Don't execute user-provided code
- Sanitize paths

---

## Troubleshooting

### Build Issues

**"Module not found"**
```bash
pip install -r requirements.txt
```

**"Icon not found"**
- Ensure icon files in repo root
- Check add-data parameter syntax

**"Windows Defender blocks exe"**
- Expected for unsigned binaries
- Submit to Microsoft (if persistent)
- Consider code signing (paid)

### Runtime Issues

**"Config file corrupt"**
```bash
# Delete and restart
rm ~/.rugby_referee_review_config.json
```

**"Reviews not loading"**
- Check JSON validity
- Verify file permissions
- Check directory exists

**"Analytics crash"**
- Verify matplotlib installed
- Check review has GFA scores
- Ensure at least one review exists

---

## Resources

**Python:**
- [tkinter documentation](https://docs.python.org/3/library/tkinter.html)
- [PyInstaller manual](https://pyinstaller.org/en/stable/)

**Libraries:**
- [ttkbootstrap docs](https://ttkbootstrap.readthedocs.io/)
- [matplotlib gallery](https://matplotlib.org/stable/gallery/)
- [openpyxl docs](https://openpyxl.readthedocs.io/)

**Tools:**
- [GitHub Actions docs](https://docs.github.com/en/actions)
- [Git reference](https://git-scm.com/docs)

---

## Contact

**Issues:** https://github.com/agclarkson/ReviewApp/issues  
**Developer:** Andrew Clarkson

---

**Last Updated:** 2025-01-19  
**Version:** 2.0.8-alpha