# 🗽 NYC Family Trip Planner - Local Web Server

View your NYC trip planning documents in your browser with a beautiful, easy-to-navigate interface!

## 🚀 Quick Start

### Option 1: Simple Start (Python required)
```bash
python3 serve_docs.py
```

### Option 2: Auto-install Dependencies
```bash
# Install markdown for better formatting (optional but recommended)
pip install markdown

# Start server
python3 serve_docs.py
```

### Option 3: One-command start
```bash
chmod +x start_server.sh
./start_server.sh
```

## 🌐 Access Your Documents

Once running, open your browser to:
- **Main Index:** http://localhost:8080
- **Mobile Access:** http://[your-ip]:8080 (great for phones/tablets!)

## 📱 Features

### Beautiful Index Page
- **Grid layout** of all your planning documents
- **Quick navigation** between files
- **Mobile-friendly** responsive design
- **Real-time updates** when you edit files

### Enhanced Document Viewing
- **Markdown to HTML** conversion for beautiful formatting
- **Proper styling** with NYC-themed colors
- **Easy navigation** back to index
- **Table formatting** for comparisons
- **Emoji support** for visual appeal

## 📄 Your Documents

The server will display all these files with proper formatting:

1. **🎯 Complete Family Itinerary** (`our_nyc_family_itinerary.md`)
   - Day-by-day detailed schedule
   - Timing, meals, and activities
   - Transportation and tips

2. **🌟 Must-See Places Guide** (`nyc_must_see_guide.md`)  
   - Ranked attractions and activities
   - Detailed descriptions and tips
   - Family-friendly recommendations

3. **✅ Personal Must-Do List** (`our_nyc_must_do_list.md`)
   - Your curated activity choices
   - Notes and preferences
   - Editable working document

4. **🎫 Attraction Passes Comparison** (`nyc_holiday_passes_comparison.md`)
   - GoCity vs CityPASS vs TopView
   - Detailed feature comparison
   - Pricing and value analysis

## 🔧 Technical Details

- **Port:** 8080 (customizable in script)
- **Python:** Works with Python 3.6+
- **Dependencies:** None required, `markdown` optional for better formatting
- **Auto-refresh:** No cache, always shows latest changes
- **Cross-platform:** Works on Mac, Windows, Linux

## 🛑 Stopping the Server

Press `Ctrl+C` in the terminal to stop the server.

## 📱 Sharing with Family

The server can be accessed from any device on your local network:
1. Find your computer's IP address
2. Share: `http://[your-ip]:8080`
3. Family members can view on phones/tablets!

## 🔧 Customization

Edit `serve_docs.py` to:
- Change port number (line: `PORT = 8080`)
- Modify styling and colors
- Add new file types
- Customize descriptions

---

**Perfect for:** Planning sessions, family meetings, mobile reference during your NYC trip!

🎯 *Happy trip planning!*

