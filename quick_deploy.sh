#!/bin/bash
# Quick deployment for offline PWA - No updates needed during travel

echo "🚀 Quick PWA Deployment - Offline Travel Edition"
echo "================================================"

echo "📋 Automated Deployment Steps:"
echo "1. ✅ Sanitize documents (remove sensitive info)"  
echo "2. ✅ Generate PWA icons automatically"
echo "3. ✅ Deploy to GitHub"
echo "4. 📱 Install PWA on devices (manual)"
echo "5. 🔒 Make repo private again (manual)"
echo ""

# Step 1: Sanitize documents
echo "🛡️ Step 1: Sanitizing documents for public repo..."
python3 sanitize_for_public.py

echo ""
echo "🎨 Step 2: Generating PWA icons automatically..."
python3 generate_icons.py

# Verify icons were created
icon_count=$(ls icon-*.png 2>/dev/null | wc -l)
if [ $icon_count -eq 8 ]; then
    echo "✅ All 8 PWA icons generated successfully!"
else
    echo "⚠️  Only found $icon_count/8 icons. Installing Pillow and retrying..."
    python3 -m pip install Pillow --break-system-packages --quiet
    python3 generate_icons.py
    icon_count=$(ls icon-*.png 2>/dev/null | wc -l)
    if [ $icon_count -eq 8 ]; then
        echo "✅ All 8 PWA icons generated successfully!"
    else
        echo "❌ Icon generation failed. Continuing without all icons..."
    fi
fi

echo ""
echo "📤 Step 3: Deploying to GitHub..."

# Initialize git if needed
if [ ! -d ".git" ]; then
    echo "🔧 Initializing Git repository..."
    git init
    git branch -M main
    git remote add origin https://github.com/Shoshvany/us2025.git
else
    echo "📂 Git repository already initialized"
fi

# Check if remote exists and is correct
current_remote=$(git remote get-url origin 2>/dev/null || echo "none")
if [ "$current_remote" != "https://github.com/Shoshvany/us2025.git" ]; then
    echo "🔧 Setting correct remote URL..."
    git remote set-url origin https://github.com/Shoshvany/us2025.git 2>/dev/null || git remote add origin https://github.com/Shoshvany/us2025.git
fi

# Stage all PWA files
echo "📦 Staging files for commit..."
git add index.html manifest.json sw.js icon-*.png *.md PWA_SETUP.md DEPLOYMENT_CHECKLIST.md 2>/dev/null

# Check if there are changes to commit
if git diff --staged --quiet; then
    echo "ℹ️  No changes to commit - files may already be up to date"
else
    echo "💾 Committing changes..."
    git commit -m "🗽 Deploy Offline Travel PWA

✈️ Complete travel planning for October 2025
🏙️ NYC • 🎢 Orlando • 🦞 Boston

Features:
✅ Works 100% offline after install
✅ All itineraries cached locally  
✅ Native app experience on iPhone
✅ No internet needed during travel

Ready for: Make public → Install PWA → Make private"
fi

echo "🚀 Pushing to GitHub..."
git push -u origin main

echo ""
echo "🎉 Deployment Complete!"
# Final validation
echo ""
echo "🔍 Final validation..."
required_files=("index.html" "manifest.json" "sw.js")
missing_files=()

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        missing_files+=("$file")
    fi
done

icon_count=$(ls icon-*.png 2>/dev/null | wc -l)
if [ $icon_count -lt 8 ]; then
    missing_files+=("icons (only $icon_count/8 found)")
fi

if [ ${#missing_files[@]} -eq 0 ]; then
    echo "✅ All required files present!"
else
    echo "⚠️  Missing files: ${missing_files[*]}"
fi

echo ""
echo "📱 QUICK SETUP LINKS (Do These Now):"
echo ""
echo "🔓 1. Make Repository PUBLIC:"
echo "   👆 CLICK: https://github.com/Shoshvany/us2025/settings"
echo "   📍 Scroll to 'Danger Zone' → Change visibility → Make public"
echo ""
echo "⚙️  2. Enable GitHub Pages:"
echo "   👆 CLICK: https://github.com/Shoshvany/us2025/settings/pages"
echo "   📍 Source: Deploy from branch → main → / (root) → Save"
echo ""
echo "📱 3. Install PWA (wait 3 minutes after step 2):"
echo "   👆 OPEN: https://Shoshvany.github.io/us2025"
echo "   📍 iPhone Safari → Share → Add to Home Screen"
echo ""
echo "🔒 4. Make Repository PRIVATE Again:"
echo "   👆 CLICK: https://github.com/Shoshvany/us2025/settings"
echo "   📍 Scroll to 'Danger Zone' → Change visibility → Make private"
echo ""
echo "✅ 5. Test Offline:"
echo "   📍 Turn off WiFi → Open PWA → Should work perfectly!"
echo ""
echo "🧳 During Travel (October):"
echo "✅ PWA works 100% offline with all your itineraries"
echo "✅ No GitHub or internet access needed"
echo "✅ Repository stays private"
echo "✅ Native app experience on all devices"
echo ""
echo "🔒 To restore original private documents after trip:"
echo "   ./restore_private_docs.sh"
