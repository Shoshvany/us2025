#!/usr/bin/env python3
"""
Auto-generate PWA icons without external dependencies
Creates simple travel-themed icons using built-in libraries
"""

import os
from pathlib import Path

def create_svg_icon(size):
    """Create SVG icon that can be converted to PNG"""
    svg_content = f'''<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#667eea"/>
      <stop offset="100%" style="stop-color:#764ba2"/>
    </linearGradient>
  </defs>
  
  <!-- Background -->
  <rect width="{size}" height="{size}" rx="{size//8}" fill="url(#bg)"/>
  
  <!-- Travel bag -->
  <rect x="{size//3}" y="{size//2.5}" width="{size//3}" height="{size//5}" rx="{size//64}" fill="white" stroke="#34495e" stroke-width="{max(2, size//128)}"/>
  
  <!-- Handle -->
  <path d="M {size//2.4} {size//3} Q {size//2} {size//4} {size//1.7} {size//3}" stroke="#34495e" stroke-width="{max(3, size//85)}" fill="none"/>
  
  <!-- Text 2025 -->
  <text x="{size//2}" y="{size//1.4}" font-family="Arial, sans-serif" font-size="{max(12, size//14)}" font-weight="bold" text-anchor="middle" fill="white">2025</text>
  
  <!-- Location pins -->
  <circle cx="{size//3.4}" cy="{size//2}" r="{max(4, size//43)}" fill="#e74c3c"/>
  <circle cx="{size//1.4}" cy="{size//2.3}" r="{max(4, size//43)}" fill="#27ae60"/>
  <circle cx="{size//1.8}" cy="{size//1.3}" r="{max(4, size//43)}" fill="#f39c12"/>
</svg>'''
    return svg_content

def create_html_to_png_converter():
    """Create HTML file that can generate PNG icons from SVG"""
    html_content = '''<!DOCTYPE html>
<html>
<head>
    <title>Auto Icon Generator</title>
</head>
<body>
    <h1>Generating PWA Icons...</h1>
    <script>
        const sizes = [72, 96, 128, 144, 152, 192, 384, 512];
        let completed = 0;
        
        function downloadIcon(canvas, size) {
            const link = document.createElement('a');
            link.download = `icon-${size}.png`;
            link.href = canvas.toDataURL();
            link.click();
        }
        
        sizes.forEach((size, index) => {
            setTimeout(() => {
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
                
                // Add travel bag
                ctx.fillStyle = 'white';
                ctx.strokeStyle = '#34495e';
                ctx.lineWidth = Math.max(2, size/64);
                const bagWidth = size/3;
                const bagHeight = size/5;
                const bagX = size/3;
                const bagY = size/2.5;
                ctx.fillRect(bagX, bagY, bagWidth, bagHeight);
                ctx.strokeRect(bagX, bagY, bagWidth, bagHeight);
                
                // Add handle
                ctx.beginPath();
                ctx.arc(size/2, bagY - size/8, bagWidth/4, 0, Math.PI);
                ctx.stroke();
                
                // Add text
                ctx.fillStyle = 'white';
                ctx.font = `bold ${Math.max(12, size/14)}px Arial`;
                ctx.textAlign = 'center';
                ctx.fillText('2025', size/2, size/1.4);
                
                // Add location pins
                ctx.fillStyle = '#e74c3c';
                ctx.beginPath();
                ctx.arc(size/3.4, size/2, Math.max(4, size/43), 0, 2*Math.PI);
                ctx.fill();
                
                ctx.fillStyle = '#27ae60';
                ctx.beginPath();
                ctx.arc(size/1.4, size/2.3, Math.max(4, size/43), 0, 2*Math.PI);
                ctx.fill();
                
                ctx.fillStyle = '#f39c12';
                ctx.beginPath();
                ctx.arc(size/1.8, size/1.3, Math.max(4, size/43), 0, 2*Math.PI);
                ctx.fill();
                
                // Auto-download
                downloadIcon(canvas, size);
                
                completed++;
                if (completed === sizes.length) {
                    document.body.innerHTML = '<h1>✅ All icons generated!</h1><p>Check your Downloads folder for icon-*.png files</p><p>Move them to your project directory</p>';
                }
            }, index * 500); // Stagger downloads
        });
    </script>
</body>
</html>'''
    
    with open('auto_icon_generator.html', 'w') as f:
        f.write(html_content)
    
    return 'auto_icon_generator.html'

def main():
    print("🎨 Generating PWA icons automatically...")
    
    # Try to create icons with different methods
    methods_tried = []
    
    # Method 1: Try with cairosvg (if available)
    try:
        import cairosvg
        print("✅ Using cairosvg for high-quality PNG generation...")
        
        sizes = [72, 96, 128, 144, 152, 192, 384, 512]
        for size in sizes:
            svg_content = create_svg_icon(size)
            png_data = cairosvg.svg2png(bytestring=svg_content.encode('utf-8'))
            
            with open(f'icon-{size}.png', 'wb') as f:
                f.write(png_data)
            print(f"✅ Created icon-{size}.png")
        
        methods_tried.append("cairosvg")
        return True
        
    except ImportError:
        methods_tried.append("cairosvg (not available)")
    
    # Method 2: Try with Pillow
    try:
        from PIL import Image, ImageDraw, ImageFont
        import io
        print("✅ Using Pillow for PNG generation...")
        
        sizes = [72, 96, 128, 144, 152, 192, 384, 512]
        for size in sizes:
            # Create image with gradient background
            img = Image.new('RGB', (size, size), color='white')
            draw = ImageDraw.Draw(img)
            
            # Draw gradient background
            for i in range(size):
                color_value = int(102 + (118 - 102) * i / size)  # #667eea to #764ba2
                draw.line([(0, i), (size, i)], fill=(color_value, 126, 234))
            
            # Draw travel bag
            bag_width = size // 3
            bag_height = size // 5
            bag_top = int(size / 2.5)
            bag_left = size // 3
            
            draw.rectangle([bag_left, bag_top, bag_left + bag_width, bag_top + bag_height], 
                          fill='white', outline='#34495e', width=max(2, size//64))
            
            # Handle
            handle_y = bag_top - size // 8
            draw.arc([bag_left + bag_width//4, handle_y, bag_left + 3*bag_width//4, bag_top + 10], 
                     0, 180, fill='#34495e', width=max(3, size//85))
            
            # Add "2025" text
            try:
                font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", max(12, size//14))
            except:
                font = ImageFont.load_default()
            
            text = "2025"
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_x = size//2 - text_width // 2
            text_y = int(size/1.4)
            
            draw.text((text_x, text_y), text, fill='white', font=font)
            
            # Add location pins
            pin_size = max(4, size // 43)
            draw.ellipse([size//3.4 - pin_size, size//2 - pin_size, 
                         size//3.4 + pin_size, size//2 + pin_size], fill='#e74c3c')
            draw.ellipse([size//1.4 - pin_size, int(size/2.3) - pin_size,
                         size//1.4 + pin_size, int(size/2.3) + pin_size], fill='#27ae60')
            draw.ellipse([size//1.8 - pin_size, int(size/1.3) - pin_size,
                         size//1.8 + pin_size, int(size/1.3) + pin_size], fill='#f39c12')
            
            img.save(f'icon-{size}.png', 'PNG')
            print(f"✅ Created icon-{size}.png")
        
        methods_tried.append("Pillow")
        return True
        
    except ImportError:
        methods_tried.append("Pillow (not available)")
    
    # Method 3: Create HTML auto-generator
    print("⚠️  No image libraries found. Creating auto-generator...")
    html_file = create_html_to_png_converter()
    print(f"✅ Created {html_file}")
    print(f"📂 Open {html_file} in your browser - icons will download automatically!")
    
    methods_tried.append("HTML auto-generator")
    return False

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n💡 Install image library for automatic generation:")
        print("   pip install Pillow")
        print("   or: pip install cairosvg")
