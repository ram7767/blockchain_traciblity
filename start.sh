#!/bin/bash
# ============================================================
# Blockchain Traceability for Sustainable Agriculture
# Single-command startup script
# ============================================================
# Usage: ./start.sh
# ============================================================

set -e

# Navigate to script directory
cd "$(dirname "$0")"

echo "🌿 Blockchain Traceability for Sustainable Agriculture"
echo "======================================================="

# Step 1: Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
fi

# Step 2: Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Step 3: Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt --quiet

# Step 4: Navigate to Django project
cd Agriculture

# Step 5: Run migrations
echo "🗄️  Running database migrations..."
python manage.py migrate --run-syncdb --verbosity 0

# Step 6: Start Django server
echo ""
echo "✅ Setup complete!"
echo "🌐 Starting Django server at http://127.0.0.1:8000"
echo ""
echo "⚠️  NOTE: Make sure Ganache/Truffle blockchain is running on http://127.0.0.1:9545"
echo "    Press Ctrl+C to stop the server"
echo ""
python manage.py runserver
