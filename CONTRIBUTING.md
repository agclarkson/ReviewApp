# Contributing to ORRA Referee Review System

Thank you for your interest in improving the ORRA Referee Review System! This guide will help you contribute effectively.

## 🎯 Ways to Contribute

- **Report bugs** - Found an issue? Let us know!
- **Suggest features** - Have an idea? We'd love to hear it!
- **Improve documentation** - Help make guides clearer
- **Submit code** - Fix bugs or add features
- **Test releases** - Try beta versions and provide feedback

## 🐛 Reporting Bugs

When reporting bugs, please include:

1. **Description** - What happened?
2. **Expected behavior** - What should have happened?
3. **Steps to reproduce** - How can we recreate it?
4. **Environment** - OS, Python version, app version
5. **Screenshots** - If applicable
6. **Error messages** - Full error text

**Example:**
```
Title: Excel export fails on macOS Sonoma

Description: When clicking "Save & Export", the app crashes
Expected: Should open save dialog
Steps:
1. Complete review
2. Click "Save & Export"
3. App crashes

Environment:
- macOS Sonoma 14.2
- Python 3.11.7
- App version 1.0.0

Error: [paste error message]
```

## 💡 Suggesting Features

Before suggesting a feature:
1. Check if it already exists
2. Check if someone else suggested it
3. Consider if it fits CRRDF framework

When suggesting:
1. **Describe the feature** - What should it do?
2. **Explain the benefit** - Why is it useful?
3. **Propose implementation** - How could it work?
4. **Consider alternatives** - Other ways to solve it?

## 🔧 Development Setup

### Prerequisites
- Python 3.7+
- Git
- Code editor (VS Code, PyCharm, etc.)

### Setup

```bash
# Clone repository
git clone https://github.com/YOUR-USERNAME/orra-referee-review.git
cd orra-referee-review

# Install dependencies
pip install -r requirements.txt

# Run the app
python referee_review_app.py
```

### Testing Changes

```bash
# Test locally
python referee_review_app.py

# Test a complete review
# - Enter test data
# - Complete all sections
# - Verify Excel export
# - Check exported file

# Test on different OS (if possible)
```

## 📝 Code Guidelines

### Python Style
- Follow PEP 8 style guide
- Use descriptive variable names
- Add comments for complex logic
- Keep functions focused and small

### Code Structure
```python
# Good: Clear, descriptive
def save_and_next_question(self):
    """Save current answer and move to next"""
    # Save answer
    # Update progress
    # Show next question

# Avoid: Unclear, doing too much
def process(self):
    # Everything in one function
```

### Documentation
- Update README.md for user-facing changes
- Update QUICK_START.md for workflow changes
- Add docstrings to new functions
- Comment complex CRRDF logic

## 🔀 Pull Request Process

### Before Submitting

1. **Test thoroughly**
   - Run the app
   - Test all features
   - Verify Excel export
   - Check on your OS

2. **Update documentation**
   - README.md (if user-visible changes)
   - Code comments
   - Relevant guides

3. **Check code quality**
   - No syntax errors
   - Follows style guide
   - Clear commit messages

### Submitting PR

1. **Fork the repository**
2. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/bug-description
   ```

3. **Make changes**
   ```bash
   git add .
   git commit -m "Add feature: description"
   ```

4. **Push to fork**
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create Pull Request**
   - Go to original repository
   - Click "New Pull Request"
   - Select your fork and branch
   - Fill in description

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing Done
- [ ] Tested locally
- [ ] Tested Excel export
- [ ] Updated documentation
- [ ] Tested on [OS]

## Screenshots (if applicable)
[Add screenshots]

## Related Issues
Fixes #123
```

## 🎨 UI/UX Contributions

### Design Principles
- **CRRDF-first** - Framework guides structure
- **Clear hierarchy** - Important info stands out
- **Minimal friction** - Easy navigation
- **Professional** - ORRA-appropriate styling

### Color Palette
```python
# Current colors
ORRA_BLUE = "#003366"
ORRA_TEAL = "#00796b"
BACKGROUND = "#f0f0f0"
WHITE = "#ffffff"
GRAY_TEXT = "#666666"
```

### Adding UI Features
1. Match existing style
2. Test on different screen sizes
3. Ensure keyboard navigation works
4. Keep accessibility in mind

## 📋 CRRDF Framework Changes

When modifying CRRDF content:

1. **Reference source** - Cite NZR CRRDF document
2. **Maintain structure** - Keep 5 pillar organization
3. **Preserve intent** - Stay true to framework goals
4. **Test thoroughly** - Verify prompts make sense
5. **Document changes** - Update relevant docs

### Adding Questions

```python
# In referee_review_app.py
CRRDF_QUESTIONS = {
    "pillar_name": {
        "title": "Pillar Title",
        "questions": [
            {
                "q": "Your question?",
                "prompts": [
                    "Helpful prompt 1",
                    "Helpful prompt 2",
                    "Helpful prompt 3"
                ]
            }
        ]
    }
}
```

## 🏗️ GitHub Actions Changes

When modifying build process:

1. **Test workflow** - Use workflow_dispatch trigger
2. **Document changes** - Update GITHUB_SETUP.md
3. **Consider all OS** - Test Windows, Mac, Linux
4. **Check build size** - Keep executables reasonable
5. **Verify downloads** - Test actual release files

## 🧪 Testing Guidelines

### Test Checklist

**Basic Functionality:**
- [ ] App starts without errors
- [ ] All screens load
- [ ] Navigation works
- [ ] Buttons respond
- [ ] Text entry works

**Review Flow:**
- [ ] Metadata saves
- [ ] Goals save
- [ ] Reflections save
- [ ] CRRDF questions work
- [ ] GFA scoring works
- [ ] Excel export succeeds

**Excel Output:**
- [ ] File opens in Excel
- [ ] All data present
- [ ] Formatting correct
- [ ] Formulas work (if any)
- [ ] Compatible with ORRA template

**Cross-Platform (if possible):**
- [ ] Windows
- [ ] macOS
- [ ] Linux

## 📚 Documentation Guidelines

### Writing Style
- **Clear** - Easy to understand
- **Concise** - No unnecessary words
- **Complete** - All info needed
- **Correct** - Technically accurate

### Document Types
- **README.md** - User guide (non-technical)
- **QUICK_START.md** - Fast-track (very simple)
- **SETUP.md** - Maintainer guide (technical)
- **docs/** - Detailed guides (comprehensive)

### Screenshots
- Use clear, high-resolution images
- Highlight relevant UI elements
- Keep file sizes reasonable
- Store in `docs/images/` folder

## 🎓 Learning Resources

### Python & Tkinter
- [Python Docs](https://docs.python.org/3/)
- [Tkinter Tutorial](https://docs.python.org/3/library/tkinter.html)
- [Real Python Tkinter Guide](https://realpython.com/python-gui-tkinter/)

### Excel & openpyxl
- [openpyxl Docs](https://openpyxl.readthedocs.io/)

### GitHub Actions
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [PyInstaller Docs](https://pyinstaller.org/)

### CRRDF
- Community Rugby Referee Development Framework (NZR, Feb 2025)
- Contact ORRA for latest version

## ❓ Questions?

- **Technical issues** - Open GitHub Issue
- **CRRDF questions** - Contact ORRA Development Officer
- **General queries** - Email ORRA committee

## 🙏 Recognition

Contributors will be:
- Listed in release notes
- Acknowledged in commits
- Thanked by ORRA community

Thank you for helping improve referee development! 🏉
