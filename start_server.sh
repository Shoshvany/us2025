#!/bin/bash

# NYC Trip Planner - Auto-Start Web Server
# Makes it super easy to view your planning documents in a browser

echo "🗽 NYC Family Trip Planner - Starting Web Server..."
echo

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed or not in PATH"
    echo "   Please install Python 3 from: https://www.python.org/downloads/"
    echo
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if markdown is installed, offer to install it
if ! python3 -c "import markdown" 2> /dev/null; then
    echo "📦 Markdown library not found (optional for better formatting)"
    echo
    read -p "   Install markdown for enhanced formatting? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "📦 Installing markdown..."
        pip3 install markdown
        if [ $? -eq 0 ]; then
            echo "✅ Markdown installed successfully!"
        else
            echo "⚠️  Markdown installation failed, continuing with basic formatting..."
        fi
    else
        echo "⏭️  Skipping markdown installation (basic formatting will be used)"
    fi
else
    echo "✅ Markdown library found - enhanced formatting enabled!"
fi

echo
echo "🚀 Starting server..."
echo "📍 Your documents will be available at: http://localhost:8080"
echo "📱 Mobile access: http://$(ipconfig getifaddr en0 2>/dev/null || hostname -I | awk '{print $1}' 2>/dev/null || echo 'your-ip'):8080"
echo
echo "💡 Tip: Bookmark http://localhost:8080 for easy access!"
echo "🛑 Press Ctrl+C to stop the server when done"
echo
echo "────────────────────────────────────────────────────────"

# Start the Python server
python3 serve_docs.py

