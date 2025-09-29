#!/bin/bash
# Restore original private documents

echo "🔒 Restoring original private documents..."

if [ ! -d "original_private_docs" ]; then
    echo "❌ Backup directory not found!"
    exit 1
fi

cp original_private_docs/*.md .
echo "✅ Original private documents restored"
echo "⚠️  Remember: Repository is still public!"
echo "    Make it private in GitHub settings if needed"
