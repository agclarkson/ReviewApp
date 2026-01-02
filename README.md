# ORRA Referee Review System

A desktop application for rugby referees to conduct structured post-game reviews based on the Community Rugby Referee Development Framework (CRRDF).

## Features

### 🎯 Structured Review Process
- **Game Metadata**: Record game details, grade, result, and personal goals
- **Self Reflection**: Initial reflection on goals, successes, and challenges
- **CRRDF Deep Dive**: Guided questions across all 5 pillars:
  - Technical Pillar (law application, decision-making)
  - Tactical Pillar (awareness, advantage, positioning)
  - Management Pillar (game management, safety, strategies)
  - Mental Pillar (preparation, managing pressure, soft skills)
  - Physical Pillar (fitness, positioning)
- **GFA Scoring**: Rate performance in Game Focus Areas (1-5 scale):
  - Tackle/Ruck (Tackler, Jackler)
  - Scrum (Stability, Push Straight)
  - Lineout/Maul (Fair contest, Legal setup)
  - Space (Kicks, Breakdown/Maul)
  - Management (Advantage, Foul Play/Big Moments)

### 📊 Export to Excel
- Generates spreadsheet matching ORRA Premier Review Document format
- Includes all reflections and CRRDF responses
- Ready to share with coaches or upload to systems

### 🧠 Intelligent Prompting
- Each question includes prompts to deepen your thinking
- Based on CRRDF performance indicators
- Helps identify specific areas for improvement

## Installation

### Requirements
- Python 3.7 or higher
- tkinter (usually included with Python)
- openpyxl library

### Windows Installation

1. **Install Python** (if not already installed):
   - Download from https://www.python.org/downloads/
   - During installation, check "Add Python to PATH"

2. **Download the application**:
   - Save `referee_review_app.py` to your computer

3. **Install required library**:
   - Open Command Prompt (search for "cmd" in Start menu)
   - Run: `pip install openpyxl`

4. **Run the application**:
   - Double-click `referee_review_app.py`, or
   - Open Command Prompt in the folder and run: `python referee_review_app.py`

### Mac Installation

1. **Python is usually pre-installed**. Check by opening Terminal and running:
   ```bash
   python3 --version
   ```

2. **Download the application**:
   - Save `referee_review_app.py` to your computer

3. **Install required library**:
   ```bash
   pip3 install openpyxl
   ```

4. **Run the application**:
   ```bash
   python3 referee_review_app.py
   ```

### Linux Installation

1. **Install Python** (if needed):
   ```bash
   sudo apt-get update
   sudo apt-get install python3 python3-tk python3-pip
   ```

2. **Install required library**:
   ```bash
   pip3 install openpyxl
   ```

3. **Run the application**:
   ```bash
   python3 referee_review_app.py
   ```

## Usage Guide

### Starting a Review

1. **Launch the application** by running the Python file
2. **Enter game information**:
   - Game & Grade (e.g., "Premier 1")
   - Date, Result
   - Your name and coach name
3. **Set your match goals**:
   - Primary goal (main focus area)
   - Secondary goal
4. **Rate game difficulty** (1-10 scale)

### Self Reflection

Answer four key questions:
- Did you meet your goals?
- What went well?
- What was the biggest challenge?
- What are you taking forward?

### CRRDF Deep Dive

Work through each of the five pillars:
- Read the introduction to each pillar
- Answer questions with specific examples
- Use the prompts to guide deeper reflection

**Example questions:**
- *Technical*: "Were your decisions based on actual player actions?"
- *Tactical*: "How appropriate was your advantage application?"
- *Management*: "Did you recognize the right level of management?"
- *Mental*: "Did you identify and mitigate any 'clutter'?"

### GFA Scoring

Rate your performance in each Game Focus Area using the 1-5 scale:
- **1** = Unacceptable (errors significantly impacted game)
- **2** = Below Standard (limited awareness, negative influence)
- **3** = Satisfactory (adequate, minor errors, meets expectations)
- **4** = Sound (good awareness, positive contribution)
- **5** = Excellent (consistently high level, best practice)

### Exporting

1. Click "Save & Export"
2. Choose save location
3. File is saved in Excel format matching ORRA template
4. Review can be shared with coaches or uploaded to systems

## Tips for Effective Reviews

### Be Specific
❌ "Tackle area was good"
✅ "Identified tackler release accurately 8/10 times, particularly at crucial moments in Red 22. Missed one non-release in 65th minute that led to turnover."

### Use Examples
Include specific incidents:
- Time in match (e.g., "23rd minute")
- Teams involved
- What you did well/could improve
- Impact on the game

### Link to CRRDF
Connect your experiences to the framework:
- Which pillar does this relate to?
- What performance indicator does it demonstrate?
- How does it support your development goals?

### Be Honest
The review is for YOUR development:
- Acknowledge mistakes
- Identify patterns
- Celebrate genuine successes
- Set realistic improvement goals

## Understanding CRRDF Levels

The app helps you reflect on standards across community rugby levels:

- **Level 1**: Beginning referee (U19 and below)
- **Level 2**: Developing (Secondary School, Weight-restricted grades)
- **Level 3**: Satisfactory (Colts, Senior 2nds, 1st XV)
- **Level 4**: Sound (up to Premier/Senior 1)
- **Level 5**: Excellent (Premier/Senior 1 standard)

## Coach Integration

Coaches can:
1. Add their scores to the GFA section (Column G in Excel)
2. Add feedback in the "Coach Review/Feedback" section
3. Reference specific CRRDF responses in feedback
4. Use the document for promotion recommendations

## Troubleshooting

### Application won't start
- Check Python is installed: `python --version` or `python3 --version`
- Check openpyxl is installed: `pip list | grep openpyxl`
- Try running from command line to see error messages

### Excel file won't open
- Ensure you have Excel, LibreOffice, or Google Sheets
- Check file has .xlsx extension
- Try opening with different spreadsheet program

### Questions not saving
- Ensure you click "Next" buttons to progress
- Don't close app until export is complete
- Check your responses appear in final Excel file

## File Structure

```
referee_review_app.py    # Main application
README.md                # This file
[output files]           # Generated Excel reviews
```

## Customization

### Adding Questions
Edit the `CRRDF_QUESTIONS` dictionary in the code to add custom questions.

### Modifying GFAs
Edit the `GFA_CATEGORIES` dictionary to change focus areas.

### Changing Scale
Edit `RATING_SCALE` to modify scoring descriptions.

## Support

For issues or suggestions:
- Contact your Referee Development Officer
- Reach out to ORRA committee
- Check for updates to the application

## Version History

- **v1.0** (2025-01): Initial release
  - Full CRRDF framework integration
  - All 5 pillars with guided questions
  - GFA scoring system
  - Excel export in ORRA format

## Credits

Developed for Otago Rugby Referees Association (ORRA)

Based on:
- Community Rugby Referee Development Framework (NZR, Feb 2025)
- ORRA Premier Review Document Master template
- World Rugby match official development principles

---

*"The referee is the custodian of the game"*
