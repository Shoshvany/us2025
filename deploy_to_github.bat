@echo off
REM Deploy US Trip 2025 PWA to GitHub Pages

echo 🗽 Deploying US Trip 2025 PWA to GitHub Pages...
echo ================================================

REM Check if we're in a git repository
if not exist ".git" (
    echo ❌ Not in a Git repository. Initializing...
    git init
    git remote add origin https://github.com/Shoshvany/us2025.git
)

REM Add all PWA files
echo 📂 Adding PWA files...
git add index.html
git add manifest.json
git add sw.js
git add icon-*.png 2>nul || echo ⚠️  No icon files found - create them using icon_generator.html

REM Add all travel documents  
echo 📚 Adding travel documents...
git add *.md

REM Add optional files
git add PWA_SETUP.md 2>nul
git add DEPLOYMENT_CHECKLIST.md 2>nul
git add icon.svg 2>nul

REM Check status
echo 📋 Files to be committed:
git status --porcelain

REM Commit changes
echo 💾 Committing changes...
git commit -m "🚀 Deploy US Trip 2025 PWA - Add Progressive Web App functionality - Include all travel documents (NYC, Orlando, Boston) - Add PWA manifest and service worker - Ready for GitHub Pages deployment"

REM Push to GitHub
echo 🚀 Pushing to GitHub...
git push -u origin main

echo.
echo 🎉 Deployment complete!
echo.
echo 🌐 Your PWA will be available at:
echo    https://Shoshvany.github.io/us2025
echo.
echo 📱 To install on iPhone:
echo    1. Open the URL in Safari
echo    2. Tap Share → Add to Home Screen
echo.
echo ⏰ Allow 2-3 minutes for GitHub Pages to build
echo.
echo 📋 Next: Enable GitHub Pages in your repository settings
echo    Go to: https://github.com/Shoshvany/us2025/settings/pages

pause
