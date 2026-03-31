#!/bin/bash

# Angel Investor Dashboard - Setup Script

echo "🚀 Setting up Angel Investor Dashboard..."
echo ""

# Check for Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install it from https://nodejs.org/"
    exit 1
fi

echo "✅ Node.js $(node -v)"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
npm install

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "✅ Dependencies installed"
echo ""

# Load sample data
echo "📊 Loading sample data..."
node seed-data.js

echo ""
echo "✅ Setup complete!"
echo ""
echo "🎯 Next steps:"
echo "   1. Start the dashboard: npm start"
echo "   2. Open your browser: http://localhost:3000"
echo "   3. Add your angel deals and track returns"
echo ""
echo "💡 For CLI view, run: node cli.js"
echo ""
