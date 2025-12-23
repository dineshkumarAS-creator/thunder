@echo off
echo Pushing TradeFlow AI to GitHub repository...
echo.

cd /d "c:\Users\sridh\OneDrive\Desktop\Track Eye\trade-flow-ai"

echo Step 1: Updating remote repository URL...
git remote set-url origin https://github.com/dineshkumarAS-creator/dinesh.git

echo.
echo Step 2: Verifying remote URL...
git remote -v

echo.
echo Step 3: Checking status...
git status

echo.
echo Step 4: Adding all files...
git add .

echo.
echo Step 5: Committing changes...
git commit -m "Complete TradeFlow AI with ICEGATE Customs and Global Carrier API integrations"

echo.
echo Step 6: Pushing to GitHub...
git push -u origin main --force

echo.
echo Done! Check https://github.com/dineshkumarAS-creator/dinesh.git
pause
