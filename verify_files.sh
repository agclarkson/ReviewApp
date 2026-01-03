#!/bin/bash
# Verification script to check all required files are present

echo "======================================"
echo "ORRA Referee Review - Files Check"
echo "======================================"
echo ""

check_file() {
    if [ -f "$1" ]; then
        echo "✓ $1"
        return 0
    else
        echo "✗ MISSING: $1"
        return 1
    fi
}

check_dir() {
    if [ -d "$1" ]; then
        echo "✓ $1/"
        return 0
    else
        echo "✗ MISSING: $1/"
        return 1
    fi
}

MISSING=0

echo "Core Application Files:"
check_file "referee_review_app.py" || MISSING=$((MISSING + 1))
check_file "requirements.txt" || MISSING=$((MISSING + 1))
echo ""

echo "Launcher Scripts:"
check_file "launch_review_app.bat" || MISSING=$((MISSING + 1))
check_file "launch_review_app.sh" || MISSING=$((MISSING + 1))
echo ""

echo "Documentation:"
check_file "README.md" || MISSING=$((MISSING + 1))
check_file "QUICK_START.md" || MISSING=$((MISSING + 1))
check_file "PROJECT_OVERVIEW.md" || MISSING=$((MISSING + 1))
check_file "SETUP.md" || MISSING=$((MISSING + 1))
check_file "LICENSE" || MISSING=$((MISSING + 1))
check_file "ORRA_Referee_Review_System_Documentation.docx" || MISSING=$((MISSING + 1))
echo ""

echo "Configuration:"
check_file ".gitignore" || MISSING=$((MISSING + 1))
echo ""

echo "GitHub Actions:"
check_dir ".github/workflows" || MISSING=$((MISSING + 1))
check_file ".github/workflows/build-releases.yml" || MISSING=$((MISSING + 1))
echo ""

echo "Additional Documentation:"
check_dir "docs" || MISSING=$((MISSING + 1))
check_file "docs/GITHUB_SETUP.md" || MISSING=$((MISSING + 1))
check_file "docs/RELEASE_QUICK_REF.md" || MISSING=$((MISSING + 1))
check_file "docs/WORKFLOW_DIAGRAM.md" || MISSING=$((MISSING + 1))
check_file "docs/GFA_DESCRIPTIONS.md" || MISSING=$((MISSING + 1))
check_file "docs/PLACEHOLDER_FEATURE.md" || MISSING=$((MISSING + 1))
echo ""

echo "======================================"
if [ $MISSING -eq 0 ]; then
    echo "✓ All files present!"
    echo "✓ Ready to push to GitHub"
    echo ""
    echo "Next steps:"
    echo "1. git init"
    echo "2. git add ."
    echo "3. git commit -m 'Initial commit'"
    echo "4. git remote add origin YOUR-REPO-URL"
    echo "5. git push -u origin main"
else
    echo "✗ $MISSING file(s) missing"
    echo "Please ensure all files are present"
fi
echo "======================================"
