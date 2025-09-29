#!/usr/bin/env python3
"""
GitHub Pages PWA Setup Helper
Prepares your travel planning PWA for deployment
"""

import os
import shutil
from pathlib import Path

def create_simple_icons():
    """Create placeholder icons using text-based approach if PIL isn't available"""
    print("📱 Creating simple placeholder icons...")
    
    # Create a simple HTML page that can generate icons
    icon_generator_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Icon Generator</title>
    <style>
        canvas { border: 1px solid #ccc; margin: 10px; }
        body { font-family: Arial, sans-serif; padding: 20px; }
    </style>
</head>
<body>
    <h1>PWA Icon Generator</h1>
    <p>Right-click each canvas and "Save image as..." with the filename shown below it.</p>
    
    <script>
        const sizes = [72, 96, 128, 144, 152, 192, 384, 512];
        
        sizes.forEach(size => {
            const canvas = document.createElement('canvas');
            canvas.width = size;
            canvas.height = size;
            const ctx = canvas.getContext('2d');
            
            // Create gradient background
            const gradient = ctx.createLinearGradient(0, 0, size, size);
            gradient.addColorStop(0, '#667eea');
            gradient.addColorStop(1, '#764ba2');
            ctx.fillStyle = gradient;
            ctx.fillRect(0, 0, size, size);
            
            // Add white text
            ctx.fillStyle = 'white';
            ctx.font = `bold ${size/8}px Arial`;
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText('US', size/2, size/2 - size/16);
            ctx.fillText('2025', size/2, size/2 + size/16);
            
            document.body.appendChild(canvas);
            const label = document.createElement('p');
            label.textContent = `Save as: icon-${size}.png`;
            label.style.textAlign = 'center';
            label.style.margin = '0 0 20px 0';
            document.body.appendChild(label);
        });
    </script>
</body>
</html>
    """
    
    with open('icon_generator.html', 'w') as f:
        f.write(icon_generator_html)
    
    print("✅ Created icon_generator.html")
    print("   Open this file in your browser to create icons manually")

def setup_github_pages():
    """Set up files for GitHub Pages deployment"""
    print("🚀 Setting up GitHub Pages PWA...")
    
    # Files that should exist
    required_files = [
        'index.html',
        'manifest.json', 
        'sw.js',
        'PWA_SETUP.md'
    ]
    
    # Check which files exist
    existing_files = []
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            existing_files.append(file)
        else:
            missing_files.append(file)
    
    print(f"\n✅ Found {len(existing_files)} required files:")
    for file in existing_files:
        print(f"   - {file}")
    
    if missing_files:
        print(f"\n❌ Missing {len(missing_files)} required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    # Check for travel documents
    md_files = [f for f in os.listdir('.') if f.endswith('.md') and f != 'PWA_SETUP.md']
    print(f"\n📚 Found {len(md_files)} travel documents:")
    for file in sorted(md_files):
        print(f"   - {file}")
    
    # Create icons if they don't exist
    icon_files = [f"icon-{size}.png" for size in [72, 96, 128, 144, 152, 192, 384, 512]]
    existing_icons = [f for f in icon_files if os.path.exists(f)]
    
    if len(existing_icons) < 8:
        print(f"\n🎨 Found {len(existing_icons)}/8 icon files")
        create_simple_icons()
    else:
        print(f"\n🎨 All {len(existing_icons)} icon files found!")
    
    return True

def create_deployment_checklist():
    """Create a checklist for GitHub Pages deployment"""
    checklist = """# 🚀 GitHub Pages Deployment Checklist

## ✅ Pre-Deployment
- [ ] All required files are ready (index.html, manifest.json, sw.js)
- [ ] All travel documents (.md files) are in the repository
- [ ] Icons are created (8 PNG files: 72px to 512px)
- [ ] Test the index.html file locally

## 📂 Upload to GitHub Repository
1. Go to https://github.com/Shoshvany/us2025
2. Upload these files:
   - [ ] index.html
   - [ ] manifest.json  
   - [ ] sw.js
   - [ ] icon-72.png through icon-512.png (8 files)
   - [ ] All your .md travel documents
   - [ ] PWA_SETUP.md (optional)

## ⚙️ Enable GitHub Pages
1. [ ] Go to repository Settings
2. [ ] Click on "Pages" in the left sidebar
3. [ ] Under "Source", select "Deploy from a branch" 
4. [ ] Choose "main" branch and "/ (root)" folder
5. [ ] Click "Save"
6. [ ] Wait 2-3 minutes for deployment

## 📱 Test Your PWA
1. [ ] Visit: https://Shoshvany.github.io/us2025
2. [ ] Verify all documents load correctly
3. [ ] Test on mobile device
4. [ ] Install on iPhone: Safari → Share → Add to Home Screen

## 🎉 Success!
Your travel planning PWA is now live and installable!

**Share URL:** https://Shoshvany.github.io/us2025
"""
    
    with open('DEPLOYMENT_CHECKLIST.md', 'w') as f:
        f.write(checklist)
    
    print("📋 Created DEPLOYMENT_CHECKLIST.md")

def main():
    print("🗽 US Trip 2025 - GitHub Pages PWA Setup")
    print("=" * 50)
    
    if setup_github_pages():
        create_deployment_checklist()
        print("\n🎉 Setup complete! Next steps:")
        print("1. Create icons using icon_generator.html (open in browser)")
        print("2. Upload all files to GitHub repository")
        print("3. Enable GitHub Pages in repository settings") 
        print("4. Visit https://Shoshvany.github.io/us2025")
        print("\nSee DEPLOYMENT_CHECKLIST.md for detailed steps!")
    else:
        print("\n❌ Setup incomplete. Please ensure all required files exist.")

if __name__ == "__main__":
    main()
