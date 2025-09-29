# 🗽 US Trip 2025 PWA Setup Guide

## 🎯 What You'll Get
A Progressive Web App that you can install on your iPhone home screen with:
- ✅ All your travel documents offline
- ✅ Native app-like experience  
- ✅ One-tap access from home screen
- ✅ Works without internet after first load

## 📋 Setup Steps

### 1. Create PWA Icons
```bash
# Install required package
pip install Pillow

# Run icon generator
python create_icons.py
```

This creates all the icon sizes needed (icon-72.png through icon-512.png).

### 2. Upload to GitHub
Upload these files to your `https://github.com/Shoshvany/us2025` repository:

**Required Files:**
- `index.html` - Main PWA interface
- `manifest.json` - PWA configuration
- `sw.js` - Service worker for offline functionality  
- `icon-*.png` - All generated icons (8 files)
- All your `.md` travel documents

**Optional Files:**
- `PWA_SETUP.md` - This setup guide
- `create_icons.py` - Icon generator script

### 3. Enable GitHub Pages
1. Go to your repo: `https://github.com/Shoshvany/us2025`
2. Click **Settings** tab
3. Scroll to **Pages** section
4. Under **Source**, select **Deploy from a branch**
5. Choose **main** branch and **/ (root)** folder
6. Click **Save**

### 4. Access Your PWA
- **URL:** `https://Shoshvany.github.io/us2025`
- **Wait 2-3 minutes** for GitHub Pages to build

### 5. Install on iPhone
1. Open `https://Shoshvany.github.io/us2025` in **Safari** (not Chrome!)
2. Tap the **Share** button (square with arrow)
3. Scroll down and tap **"Add to Home Screen"**
4. Customize the name if desired
5. Tap **"Add"**

## 📱 iPhone Installation Visual Guide

```
Safari → Your PWA URL → Share Button → Add to Home Screen → Add
```

The app will appear on your home screen with your custom icon!

## 🔧 Customization Options

### Change App Colors
Edit `manifest.json`:
```json
"theme_color": "#667eea",     // Status bar color
"background_color": "#667eea"  // Splash screen color
```

### Change App Name
Edit `manifest.json`:
```json
"name": "Your Custom Name",
"short_name": "Short Name"
```

### Add More Documents
1. Upload new `.md` files to your repo
2. Add them to the `index.html` file in the appropriate section
3. Add them to the `sw.js` file in the `urlsToCache` array

## 🎨 Icon Customization
If you want custom icons:
1. Create square PNG images in these sizes: 72, 96, 128, 144, 152, 192, 384, 512
2. Name them `icon-{size}.png` (e.g., `icon-192.png`)
3. Upload to your repository

## 🐛 Troubleshooting

**PWA not installing on iPhone?**
- Make sure you're using Safari (not Chrome or other browsers)
- Clear Safari cache and try again
- Check that all icon files are uploaded

**Documents not loading?**
- Verify all `.md` files are in the repository root
- Check that file names match exactly in `index.html`

**App not updating?**
- Clear browser cache
- Force refresh with Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)

## 📊 PWA Features Included

✅ **Offline Functionality** - Works without internet after first load  
✅ **App Icon** - Custom travel-themed icon  
✅ **Splash Screen** - Professional loading screen  
✅ **Full Screen** - No browser UI when opened from home screen  
✅ **Background Sync** - Ready for future features  
✅ **Push Notifications** - Ready for travel reminders  

## 🔄 Updating Content

To update your travel documents:
1. Edit the `.md` files in your repository
2. Commit and push changes
3. GitHub Pages will automatically update
4. Users will get updates when they refresh the app

## 💡 Pro Tips

- **Keep it simple:** Stick to markdown formatting for best compatibility
- **Test on mobile:** Always test your PWA on the actual device
- **Share the URL:** Others can install your PWA too!
- **Regular updates:** GitHub Pages updates automatically when you push changes

## 🌐 Browser Support

- ✅ **iOS Safari** - Full PWA support
- ✅ **Android Chrome** - Full PWA support  
- ✅ **Desktop Chrome** - Install as desktop app
- ⚠️ **iOS Chrome** - Limited PWA support (use Safari instead)

---

Your travel planning PWA is now ready! 🎉 

**Final URL:** `https://Shoshvany.github.io/us2025`
