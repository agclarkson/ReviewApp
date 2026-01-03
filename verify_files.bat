@echo off
REM Verification script to check all required files are present

echo ======================================
echo ORRA Referee Review - Files Check
echo ======================================
echo.

set MISSING=0

echo Core Application Files:
if exist "referee_review_app.py" (echo [32m✓[0m referee_review_app.py) else (echo [31m✗ MISSING: referee_review_app.py[0m & set /a MISSING+=1)
if exist "requirements.txt" (echo [32m✓[0m requirements.txt) else (echo [31m✗ MISSING: requirements.txt[0m & set /a MISSING+=1)
echo.

echo Launcher Scripts:
if exist "launch_review_app.bat" (echo [32m✓[0m launch_review_app.bat) else (echo [31m✗ MISSING: launch_review_app.bat[0m & set /a MISSING+=1)
if exist "launch_review_app.sh" (echo [32m✓[0m launch_review_app.sh) else (echo [31m✗ MISSING: launch_review_app.sh[0m & set /a MISSING+=1)
echo.

echo Documentation:
if exist "README.md" (echo [32m✓[0m README.md) else (echo [31m✗ MISSING: README.md[0m & set /a MISSING+=1)
if exist "QUICK_START.md" (echo [32m✓[0m QUICK_START.md) else (echo [31m✗ MISSING: QUICK_START.md[0m & set /a MISSING+=1)
if exist "PROJECT_OVERVIEW.md" (echo [32m✓[0m PROJECT_OVERVIEW.md) else (echo [31m✗ MISSING: PROJECT_OVERVIEW.md[0m & set /a MISSING+=1)
if exist "SETUP.md" (echo [32m✓[0m SETUP.md) else (echo [31m✗ MISSING: SETUP.md[0m & set /a MISSING+=1)
if exist "LICENSE" (echo [32m✓[0m LICENSE) else (echo [31m✗ MISSING: LICENSE[0m & set /a MISSING+=1)
if exist "ORRA_Referee_Review_System_Documentation.docx" (echo [32m✓[0m ORRA_Referee_Review_System_Documentation.docx) else (echo [31m✗ MISSING: ORRA_Referee_Review_System_Documentation.docx[0m & set /a MISSING+=1)
echo.

echo Configuration:
if exist ".gitignore" (echo [32m✓[0m .gitignore) else (echo [31m✗ MISSING: .gitignore[0m & set /a MISSING+=1)
echo.

echo GitHub Actions:
if exist ".github\workflows" (echo [32m✓[0m .github\workflows\) else (echo [31m✗ MISSING: .github\workflows\[0m & set /a MISSING+=1)
if exist ".github\workflows\build-releases.yml" (echo [32m✓[0m .github\workflows\build-releases.yml) else (echo [31m✗ MISSING: .github\workflows\build-releases.yml[0m & set /a MISSING+=1)
echo.

echo Additional Documentation:
if exist "docs" (echo [32m✓[0m docs\) else (echo [31m✗ MISSING: docs\[0m & set /a MISSING+=1)
if exist "docs\GITHUB_SETUP.md" (echo [32m✓[0m docs\GITHUB_SETUP.md) else (echo [31m✗ MISSING: docs\GITHUB_SETUP.md[0m & set /a MISSING+=1)
if exist "docs\RELEASE_QUICK_REF.md" (echo [32m✓[0m docs\RELEASE_QUICK_REF.md) else (echo [31m✗ MISSING: docs\RELEASE_QUICK_REF.md[0m & set /a MISSING+=1)
if exist "docs\WORKFLOW_DIAGRAM.md" (echo [32m✓[0m docs\WORKFLOW_DIAGRAM.md) else (echo [31m✗ MISSING: docs\WORKFLOW_DIAGRAM.md[0m & set /a MISSING+=1)
if exist "docs\GFA_DESCRIPTIONS.md" (echo [32m✓[0m docs\GFA_DESCRIPTIONS.md) else (echo [31m✗ MISSING: docs\GFA_DESCRIPTIONS.md[0m & set /a MISSING+=1)
if exist "docs\PLACEHOLDER_FEATURE.md" (echo [32m✓[0m docs\PLACEHOLDER_FEATURE.md) else (echo [31m✗ MISSING: docs\PLACEHOLDER_FEATURE.md[0m & set /a MISSING+=1)
echo.

echo ======================================
if %MISSING%==0 (
    echo [32m✓ All files present![0m
    echo [32m✓ Ready to push to GitHub[0m
    echo.
    echo Next steps:
    echo 1. git init
    echo 2. git add .
    echo 3. git commit -m "Initial commit"
    echo 4. git remote add origin YOUR-REPO-URL
    echo 5. git push -u origin main
) else (
    echo [31m✗ %MISSING% file(s) missing[0m
    echo Please ensure all files are present
)
echo ======================================
pause
