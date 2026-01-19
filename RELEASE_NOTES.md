# Rugby Referee Review System v2.0.8-alpha

## Alpha Release

This is an alpha release for testing and feedback. The application is functional and ready for real-world use, but may contain bugs or rough edges.

### What's Included

**Core Features:**
- CRRDF framework implementation with guided reflection
- GFA performance tracking and scoring
- Review history and search
- Analytics dashboard with trend visualization
- Excel export
- Auto-save functionality

**User Experience:**
- First-run personal setup
- Auto-fill referee and coach names
- Home screen with quick actions
- Keyboard shortcuts
- Status bar feedback
- Recent reviews quick access

**Technical:**
- Cross-platform (Windows, Mac, Linux)
- Standalone executables (no Python required)
- Local data storage
- Custom application icon

### Known Limitations

**Configuration:**
- Game grades are hardcoded (Otago region by default)
- Regional customization requires code changes
- No UI for grade management yet

**Features:**
- No PDF export (Excel only)
- No review comparison tool
- No goal tracking system
- Limited chart export options

**Platform:**
- Windows may show security warning (unsigned binary)
- Some antivirus may flag as false positive
- First launch may be slow (unpacking)

### Testing Focus

We need feedback on:

1. **Workflow:** Is the review process intuitive?
2. **Stability:** Any crashes or data loss?
3. **Performance:** Speed and responsiveness
4. **Usability:** Confusing areas or missing features?
5. **Data:** Analytics accuracy and usefulness

### How to Provide Feedback

**Report Issues:**
- Help → Report Issue in app
- GitHub Issues: https://github.com/agclarkson/ReviewApp/issues

**Include:**
- Operating system and version
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if helpful

**Feature Requests:**
- Use GitHub Issues with "enhancement" label
- Describe the use case and benefit

### Installation

1. Download appropriate file for your platform
2. Extract to preferred location
3. Run executable
4. Complete first-run setup
5. Start reviewing!

### Platform-Specific Notes

**Windows:**
- Extract ZIP file
- Run `Rugby Referee Review.exe`
- May show "Unknown Publisher" warning (click "More info" → "Run anyway")
- Windows Defender may require exception

**macOS:**
- Extract ZIP file
- Run `Rugby Referee Review`
- May need to allow in System Preferences → Security & Privacy
- Right-click → Open if prevented from launching

**Linux:**
- Extract tarball: `tar -xzf rugby-referee-review-linux.tar.gz`
- Make executable: `chmod +x rugby-referee-review`
- Run: `./rugby-referee-review`
- May need to install system dependencies

### Data Storage

All data stored locally:
- Reviews: `Documents/RugbyRefereeReviews/`
- Config: `~/.rugby_referee_review_config.json`
- No cloud sync or external services

### What's Next

**Beta Phase Goals:**
- Regional grade configuration UI
- Improved analytics (more chart types)
- Export enhancements (PDF, chart images)
- Bug fixes based on alpha feedback
- Performance optimization

**1.0 Release Goals:**
- Stable, tested codebase
- Complete documentation
- Code signing (if budget permits)
- Installer packages
- Multi-language support (if demand exists)

### Version History

**v2.0.8-alpha (Current)**
- Initial alpha release
- All core features functional
- Home screen and navigation
- Keyboard shortcuts
- Status bar
- Icon support

**Previous Phases (Development):**
- Phase 6: Home screen, shortcuts, status bar
- Phase 5: Personal setup and auto-fill
- Phase 4: Analytics dashboard
- Phase 3: Review history
- Phase 2: UI polish
- Phase 1: CRRDF implementation

### System Requirements

**Minimum:**
- Windows 10+ / macOS 10.14+ / Ubuntu 20.04+
- 4GB RAM
- 100MB disk space
- 1280x720 display

**Recommended:**
- 8GB RAM
- 1920x1080 display
- SSD for faster loading

### License

MIT License - Free and open source

### Acknowledgments

Built on the Community Rugby Referee Development Framework (CRRDF).

Special thanks to:
- CRRDF framework developers
- Alpha testers (you!)
- Rugby referee community

### Support

**Documentation:**
- README.md - Complete guide
- QUICK_START.md - Fast introduction

**Community:**
- GitHub Issues for bugs and features
- Source code available for inspection

### Disclaimer

This is alpha software. While functional, it may contain bugs. Always backup important data. No warranty provided.

---

**Ready to test?** Download, install, and start tracking your development!

**Questions or issues?** Open a GitHub issue or contact the developer.

---

**Copyright © 2025 Andrew Clarkson** | MIT License | Based on CRRDF Framework