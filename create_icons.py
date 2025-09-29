#!/usr/bin/env python3
"""
Icon generator for US Trip 2025 PWA
Creates all the required icon sizes for the PWA manifest
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size, filename):
    """Create a simple travel-themed icon"""
    # Create image with gradient background
    img = Image.new('RGB', (size, size), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw gradient background
    for i in range(size):
        color_value = int(102 + (118 - 102) * i / size)  # #667eea to #764ba2
        draw.line([(0, i), (size, i)], fill=(color_value, 126, 234))
    
    # Draw travel icon elements
    center = size // 2
    
    # Draw a simple travel bag shape
    bag_width = size // 3
    bag_height = size // 4
    bag_top = center - bag_height // 2
    bag_left = center - bag_width // 2
    
    # Main bag body
    draw.rectangle([bag_left, bag_top, bag_left + bag_width, bag_top + bag_height], 
                  fill=(255, 255, 255, 200), outline=(52, 73, 94))
    
    # Handle
    handle_y = bag_top - size // 8
    draw.arc([bag_left + bag_width//4, handle_y, bag_left + 3*bag_width//4, bag_top + 10], 
             0, 180, fill=(52, 73, 94), width=3)
    
    # Add "2025" text if size is large enough
    if size >= 96:
        try:
            # Try to use a system font
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size//8)
        except:
            font = ImageFont.load_default()
        
        text = "2025"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = center - text_width // 2
        text_y = bag_top + bag_height + 10
        
        draw.text((text_x, text_y), text, fill='white', font=font)
    
    # Add small location pins
    if size >= 72:
        pin_size = max(4, size // 32)
        # NYC pin
        draw.ellipse([center - bag_width//2 - pin_size, center - pin_size, 
                     center - bag_width//2 + pin_size, center + pin_size], 
                    fill=(231, 76, 60))
        
        # Orlando pin  
        draw.ellipse([center + bag_width//2 - pin_size, center - bag_height//4 - pin_size,
                     center + bag_width//2 + pin_size, center - bag_height//4 + pin_size], 
                    fill=(46, 204, 113))
    
    img.save(filename, 'PNG')
    print(f"Created {filename} ({size}x{size})")

def main():
    """Generate all required icon sizes"""
    sizes = [72, 96, 128, 144, 152, 192, 384, 512]
    
    print("🎨 Creating PWA icons for US Trip 2025...")
    
    # Check if PIL is available
    try:
        from PIL import Image
    except ImportError:
        print("❌ PIL (Pillow) not found. Install with: pip install Pillow")
        print("   Or create icons manually using any image editor.")
        return
    
    for size in sizes:
        filename = f"icon-{size}.png"
        create_icon(size, filename)
    
    print("\n✅ All icons created successfully!")
    print("\n📱 Next steps:")
    print("1. Upload all files to your GitHub repository")
    print("2. Enable GitHub Pages in repository settings")
    print("3. Your PWA will be available at: https://Shoshvany.github.io/us2025")
    print("4. On iOS: Open in Safari → Share → Add to Home Screen")

if __name__ == "__main__":
    main()
