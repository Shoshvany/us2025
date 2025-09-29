#!/usr/bin/env python3
"""
NYC Trip Planner - Local Web Server
Serves markdown files with browser-friendly HTML conversion and index page
"""

import http.server
import socketserver
import os
import re
from urllib.parse import unquote
from pathlib import Path

# Try to import markdown, install if needed
try:
    import markdown
    from markdown.extensions import codehilite, tables, toc
    MARKDOWN_AVAILABLE = True
except ImportError:
    MARKDOWN_AVAILABLE = False
    print("⚠️  markdown library not found. Install with: pip install markdown")
    print("   Falling back to basic HTML rendering...")

PORT = 80
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class MarkdownHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def do_GET(self):
        # Handle root path - show index
        if self.path == '/' or self.path == '/index':
            self.serve_index()
            return
        
        # Handle markdown files
        if self.path.endswith('.md'):
            self.serve_markdown()
            return
        
        # Handle other files normally
        super().do_GET()

    def serve_index(self):
        """Generate and serve an index page listing all markdown files"""
        md_files = [f for f in os.listdir(DIRECTORY) if f.endswith('.md')]
        
        html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🗽 NYC Family Trip Planner</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            background: white;
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            margin-bottom: 10px;
            font-size: 2.2em;
        }
        .subtitle {
            text-align: center;
            color: #7f8c8d;
            margin-bottom: 30px;
            font-size: 1.1em;
        }
        .file-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .file-card {
            border: 2px solid #e74c3c;
            border-radius: 8px;
            padding: 20px;
            text-decoration: none;
            color: inherit;
            transition: all 0.3s ease;
            background: linear-gradient(135deg, #fff 0%, #f8f9fa 100%);
        }
        .file-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(231, 76, 60, 0.3);
            border-color: #c0392b;
        }
        .file-title {
            font-size: 1.3em;
            font-weight: bold;
            color: #e74c3c;
            margin-bottom: 8px;
        }
        .file-desc {
            color: #555;
            font-size: 0.95em;
        }
        .status {
            background: #27ae60;
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.8em;
            display: inline-block;
            margin-top: 10px;
        }
        .footer {
            text-align: center;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 2px solid #eee;
            color: #7f8c8d;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🗽 NYC Family Trip Planner</h1>
        <div class="subtitle">October 4-9, 2025 | 2 Adults + 3 Kids (ages 5, 9, 11)</div>
        
        <div class="file-grid">
"""
        
        file_descriptions = {
            'our_nyc_family_itinerary.md': {
                'title': '🎯 Complete Family Itinerary',
                'desc': 'Day-by-day detailed schedule with timing, meals, and all activities'
            },
            'nyc_must_see_guide.md': {
                'title': '🌟 Must-See Places Guide', 
                'desc': 'Comprehensive ranked guide to NYC attractions and activities'
            },
            'our_nyc_must_do_list.md': {
                'title': '✅ Personal Must-Do List',
                'desc': 'Your curated list of chosen activities and experiences'
            },
            'nyc_holiday_passes_comparison.md': {
                'title': '🎫 Attraction Passes Comparison',
                'desc': 'Detailed comparison of GoCity, CityPASS, and TopView passes'
            }
        }
        
        for md_file in sorted(md_files):
            file_info = file_descriptions.get(md_file, {
                'title': f'📄 {md_file.replace("_", " ").replace(".md", "").title()}',
                'desc': f'Additional planning document'
            })
            
            html += f'''
            <a href="/{md_file}" class="file-card">
                <div class="file-title">{file_info['title']}</div>
                <div class="file-desc">{file_info['desc']}</div>
                <div class="status">Ready to View</div>
            </a>
            '''
        
        html += """
        </div>
        
        <div class="footer">
            <p><strong>🚀 Server Running Successfully!</strong></p>
            <p>Click any document above to view in your browser</p>
            <p><em>Files auto-refresh when changed</em></p>
        </div>
    </div>
</body>
</html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

    def serve_markdown(self):
        """Convert and serve markdown file as HTML"""
        file_path = unquote(self.path[1:])  # Remove leading slash
        full_path = os.path.join(DIRECTORY, file_path)
        
        if not os.path.exists(full_path):
            self.send_error(404)
            return
            
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Convert markdown to HTML
            if MARKDOWN_AVAILABLE:
                md = markdown.Markdown(extensions=[
                    'codehilite',
                    'tables', 
                    'toc',
                    'markdown.extensions.nl2br'
                ])
                html_content = md.convert(content)
                # Add target="_blank" to all links for new tab opening
                html_content = re.sub(r'<a href="([^"]*)"', r'<a href="\1" target="_blank"', html_content)
            else:
                # Basic fallback conversion
                html_content = self.basic_markdown_convert(content)
            
            # Create full HTML page
            filename = os.path.basename(file_path)
            title = filename.replace('_', ' ').replace('.md', '').title()
            
            html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - NYC Trip Planner</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
            color: #333;
            background: #f8f9fa;
        }}
        .container {{
            background: white;
            border-radius: 8px;
            padding: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .nav-bar {{
            background: #e74c3c;
            color: white;
            padding: 15px;
            border-radius: 8px 8px 0 0;
            margin: -30px -30px 30px -30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .nav-bar a {{
            color: white;
            text-decoration: none;
            padding: 8px 15px;
            background: rgba(255,255,255,0.2);
            border-radius: 4px;
            transition: background 0.3s;
        }}
        .nav-bar a:hover {{
            background: rgba(255,255,255,0.3);
        }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #e74c3c; padding-bottom: 10px; }}
        h2 {{ color: #34495e; margin-top: 30px; }}
        h3 {{ color: #e74c3c; }}
        h4 {{ color: #7f8c8d; font-weight: bold; margin-top: 15px; font-size: 1.1em; }}
        hr {{ border: none; border-top: 2px solid #e0e6ed; margin: 25px 0; border-radius: 2px; }}
        table {{ border-collapse: collapse; width: 100%; margin: 15px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px 12px; text-align: left; }}
        th {{ background-color: #f8f9fa; font-weight: bold; }}
        code {{ background: #f8f9fa; padding: 2px 4px; border-radius: 3px; font-family: 'Monaco', 'Consolas', monospace; }}
        pre {{ background: #f8f9fa; padding: 15px; border-radius: 5px; overflow-x: auto; }}
        blockquote {{ border-left: 4px solid #e74c3c; margin: 15px 0; padding-left: 20px; color: #666; }}
        ul, ol {{ margin: 10px 0; padding-left: 25px; }}
        li {{ margin: 5px 0; }}
        .emoji {{ font-size: 1.2em; }}
        @media (max-width: 600px) {{
            .nav-bar {{ flex-direction: column; gap: 10px; }}
            body {{ padding: 10px; }}
            .container {{ padding: 20px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="nav-bar">
            <span class="emoji">🗽</span>
            <strong>{title}</strong>
            <a href="/">← Back to Index</a>
        </div>
        {html_content}
    </div>
</body>
</html>
            """
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))
            
        except Exception as e:
            self.send_error(500, f"Error processing file: {str(e)}")

    def basic_markdown_convert(self, content):
        """Basic markdown to HTML conversion fallback"""
        html = content
        
        # Headers (order matters - h4 before h3, etc.)
        html = re.sub(r'^#### (.*)', r'<h4>\1</h4>', html, flags=re.MULTILINE)
        html = re.sub(r'^### (.*)', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.*)', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^# (.*)', r'<h1>\1</h1>', html, flags=re.MULTILINE)
        
        # Horizontal rules
        html = re.sub(r'^---$', r'<hr>', html, flags=re.MULTILINE)
        
        # Links - must come before bold/italic to avoid conflicts
        html = re.sub(r'\[([^\]]*)\]\(([^)]*)\)', r'<a href="\2" target="_blank">\1</a>', html)
        
        # Bold and italic
        html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
        
        # Lists
        lines = html.split('\n')
        in_list = False
        result_lines = []
        
        for line in lines:
            if line.strip().startswith('- '):
                if not in_list:
                    result_lines.append('<ul>')
                    in_list = True
                result_lines.append(f'<li>{line.strip()[2:]}</li>')
            else:
                if in_list:
                    result_lines.append('</ul>')
                    in_list = False
                result_lines.append(line)
        
        if in_list:
            result_lines.append('</ul>')
            
        html = '\n'.join(result_lines)
        
        # Line breaks
        html = html.replace('\n\n', '</p><p>')
        html = f'<p>{html}</p>'
        html = html.replace('<p></p>', '')
        
        return html


def main():
    """Start the development server"""
    print(f"🗽 NYC Trip Planner Server")
    print(f"📍 Serving files from: {DIRECTORY}")
    print(f"🌐 Server starting at: http://localhost:{PORT}")
    print(f"📱 Mobile friendly: http://[your-ip]:{PORT}")
    
    if not MARKDOWN_AVAILABLE:
        print(f"💡 For better formatting, install: pip install markdown")
    
    print(f"\n✨ Available documents:")
    md_files = [f for f in os.listdir(DIRECTORY) if f.endswith('.md')]
    for md_file in sorted(md_files):
        print(f"   📄 {md_file}")
    
    print(f"\n🚀 Starting server... Press Ctrl+C to stop")
    
    try:
        with socketserver.TCPServer(("", PORT), MarkdownHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print(f"\n👋 Server stopped. Thanks for planning your NYC trip!")


if __name__ == "__main__":
    main()

