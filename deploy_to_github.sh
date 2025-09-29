#!/bin/bash
# Deploy US Trip 2025 PWA to GitHub Pages

echo "🗽 Deploying US Trip 2025 PWA to GitHub Pages..."
echo "================================================"

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Not in a Git repository. Initializing..."
    git init
    git remote add origin https://github.com/Shoshvany/us2025.git
fi

# Add all PWA files
echo "📂 Adding PWA files..."
git add index.html
git add manifest.json
git add sw.js
git add icon-*.png 2>/dev/null || echo "⚠️  No icon files found - create them using icon_generator.html"

# Add all travel documents  
echo "📚 Adding travel documents..."
git add *.md

# Add optional files
git add PWA_SETUP.md 2>/dev/null
git add DEPLOYMENT_CHECKLIST.md 2>/dev/null
git add icon.svg 2>/dev/null

# Check status
echo "📋 Files to be committed:"
git status --porcelain

# Commit changes
echo "💾 Committing changes..."
git commit -m "🚀 Deploy US Trip 2025 PWA

- Add Progressive Web App functionality
- Include all travel documents (NYC, Orlando, Boston)
- Add PWA manifest and service worker
- Ready for GitHub Pages deployment

Features:
✅ Install to home screen
✅ Offline functionality  
✅ Native app experience
✅ All travel docs included"

# Push to GitHub
echo "🚀 Pushing to GitHub..."
git push -u origin main

echo ""
echo "🎉 Deployment complete!"
echo ""
echo "🌐 Your PWA will be available at:"
echo "   https://Shoshvany.github.io/us2025"
echo ""
echo "📱 To install on iPhone:"
echo "   1. Open the URL in Safari"
echo "   2. Tap Share → Add to Home Screen"
echo ""
echo "⏰ Allow 2-3 minutes for GitHub Pages to build"
echo ""
echo "📋 Next: Enable GitHub Pages in your repository settings"
echo "   Go to: https://github.com/Shoshvany/us2025/settings/pages"
