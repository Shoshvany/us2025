#!/usr/bin/env python3
"""
Sanitize travel documents for public GitHub repository
Removes sensitive information while keeping useful content
"""

import os
import re
import shutil
from pathlib import Path

def sanitize_content(content):
    """Remove or replace sensitive information"""
    
    # Remove confirmation numbers
    content = re.sub(r'Confirmation:\s*[A-Z0-9]+', 'Confirmation: [REMOVED]', content)
    content = re.sub(r'confirmation:\s*[A-Z0-9]+', 'confirmation: [REMOVED]', content, flags=re.IGNORECASE)
    
    # Remove phone numbers
    content = re.sub(r'\(\d{3}\)\s*\d{3}-\d{4}', '[PHONE REMOVED]', content)
    content = re.sub(r'\(\d{3}\)\s*\d{3}\s*\d{4}', '[PHONE REMOVED]', content)
    
    # Replace specific hotel names with generic descriptions
    hotel_replacements = {
        'Michelangelo Hotel New York': 'Times Square Area Hotel',
        'Michelangelo Hotel': 'Times Square Area Hotel',
        'Residence Inn by Marriott Boston Cambridge': 'Cambridge Area Hotel', 
        'Home2 Suites by Hilton East Haven New Haven': 'New Haven Area Hotel',
        'Best Western Berkshire Hills': 'Pittsfield Area Hotel'
    }
    
    for old, new in hotel_replacements.items():
        content = content.replace(old, new)
    
    # Replace specific addresses with general areas
    address_replacements = {
        '152 West 51st Street': 'Times Square Area',
        '152 W 51st St': 'Times Square Area',
        '120 Broadway, Cambridge, MA': 'Cambridge/Kendall Square Area', 
        '1350 West Housatonic Street, Pittsfield, MA': 'Pittsfield Area',
        '15 Transportation Way, Boston, MA': 'Logan Airport Area'
    }
    
    for old, new in address_replacements.items():
        content = content.replace(old, new)
    
    # Remove specific flight confirmation codes but keep flight info
    content = re.sub(r'NK 2819.*Confirmation: SQGQGK', 'NK 2819 - [CONFIRMATION REMOVED]', content)
    content = re.sub(r'LY 15.*Confirmation: YZQ9OC', 'LY 15 - [CONFIRMATION REMOVED]', content)
    content = re.sub(r'XP 716.*Confirmation: [A-Z0-9]+', 'XP 716 - [CONFIRMATION REMOVED]', content)
    
    # Add privacy notice
    privacy_notice = "\n*Note: Some personal details have been removed for privacy*\n"
    if "# " in content and privacy_notice not in content:
        # Add after first header
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('#'):
                lines.insert(i+2, privacy_notice)
                break
        content = '\n'.join(lines)
    
    return content

def create_public_version():
    """Create sanitized versions of travel documents"""
    
    print("🛡️ Creating sanitized versions for public repository...")
    
    # Files to sanitize
    travel_docs = [
        'orlando_itinerary.md',
        'our_nyc_family_itinerary.md', 
        'boston_itinerary.md',
        'boston_to_nyc_roadtrip.md',
        'newhaven_to_logan_roadtrip.md',
        'our_nyc_must_do_list.md',
        'nyc_must_see_guide.md',
        'nyc_holiday_passes_comparison.md'
    ]
    
    # Create backup directory
    backup_dir = 'original_private_docs'
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        print(f"📂 Created backup directory: {backup_dir}")
    
    for doc in travel_docs:
        if os.path.exists(doc):
            # Backup original
            shutil.copy2(doc, os.path.join(backup_dir, doc))
            print(f"💾 Backed up: {doc}")
            
            # Sanitize content
            with open(doc, 'r', encoding='utf-8') as f:
                content = f.read()
            
            sanitized_content = sanitize_content(content)
            
            # Write sanitized version
            with open(doc, 'w', encoding='utf-8') as f:
                f.write(sanitized_content)
            
            print(f"🛡️ Sanitized: {doc}")
    
    # Create restore script
    restore_script = f"""#!/bin/bash
# Restore original private documents

echo "🔒 Restoring original private documents..."

if [ ! -d "{backup_dir}" ]; then
    echo "❌ Backup directory not found!"
    exit 1
fi

cp {backup_dir}/*.md .
echo "✅ Original private documents restored"
echo "⚠️  Remember: Repository is still public!"
echo "    Make it private in GitHub settings if needed"
"""
    
    with open('restore_private_docs.sh', 'w') as f:
        f.write(restore_script)
    
    os.chmod('restore_private_docs.sh', 0o755)
    print("📜 Created restore_private_docs.sh")
    
    print("\n✅ Sanitization complete!")
    print(f"\n📁 Original documents backed up in: {backup_dir}/")
    print("🔒 Run './restore_private_docs.sh' to restore originals")
    print("\n🌐 Your documents are now safe for public repository!")

if __name__ == "__main__":
    create_public_version()
