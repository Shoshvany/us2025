#!/bin/bash
# One-click PWA deployment for macOS
# Double-click this file to deploy your travel PWA

cd "$(dirname "$0")"
./quick_deploy.sh

echo ""
echo "🎉 Press any key to close..."
read -n 1
