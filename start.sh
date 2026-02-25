#!/bin/bash
# ============================================================
# AgriChain — Blockchain Traceability for Sustainable Agriculture
# Single-command startup script (macOS/Linux)
# ============================================================

set -e
cd "$(dirname "$0")"

echo ""
echo "🌿 ╔══════════════════════════════════════════════════════╗"
echo "   ║   AgriChain — Blockchain Agricultural Traceability   ║"
echo "   ╚══════════════════════════════════════════════════════╝"
echo ""

# --- Step 1: Python Virtual Environment ---
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
fi
source venv/bin/activate
echo "✅ Virtual environment active"

# --- Step 2: Upgrade pip & Install Dependencies ---
echo "📥 Installing dependencies..."
pip install --upgrade pip --quiet 2>/dev/null
pip install -r requirements.txt --quiet

# --- Step 3: Create media directories ---
mkdir -p Agriculture/media/products Agriculture/media/qrcodes

# --- Step 4: Database Setup ---
echo "🗄️  Running database migrations..."
cd Agriculture
python manage.py makemigrations AgricultureApp --verbosity 0 2>/dev/null || true
python manage.py migrate --run-syncdb --verbosity 0

# --- Step 4b: Seed sample data (if new DB) ---
echo "🌱 Checking sample data..."
python manage.py seed_data

# --- Step 5: Try to start Ganache blockchain (optional) ---
echo ""
BLOCKCHAIN_STATUS="❌ Offline (SQLite-only mode)"
if command -v ganache-cli &> /dev/null; then
    echo "⛓️  Starting Ganache blockchain on port 9545..."
    ganache-cli -p 9545 --quiet &
    GANACHE_PID=$!
    sleep 2
    BLOCKCHAIN_STATUS="✅ Running (PID: $GANACHE_PID)"
elif command -v ganache &> /dev/null; then
    echo "⛓️  Starting Ganache blockchain on port 9545..."
    ganache -p 9545 --quiet &
    GANACHE_PID=$!
    sleep 2
    BLOCKCHAIN_STATUS="✅ Running (PID: $GANACHE_PID)"
else
    echo "⚠️  Ganache not found — blockchain features disabled"
    echo "   Install: npm install -g ganache-cli"
fi

# --- Step 6: Start ngrok tunnel (optional) ---
echo ""
NGROK_URL="Not available"
if python -c "import pyngrok" 2>/dev/null; then
    # Kill any stale ngrok sessions first
    python -c "from pyngrok import ngrok; ngrok.kill()" 2>/dev/null || true
    sleep 1
    echo "🌐 Starting ngrok tunnel..."
    NGROK_URL=$(python -c "
from pyngrok import ngrok
try:
    tunnel = ngrok.connect(8000)
    print(tunnel.public_url)
except Exception as e:
    print('Failed: ' + str(e))
" 2>/dev/null) || true
    if [[ "$NGROK_URL" == Failed* ]] || [[ -z "$NGROK_URL" ]]; then
        NGROK_URL="Not available (set NGROK_AUTHTOKEN or run: ngrok config add-authtoken YOUR_TOKEN)"
    fi
else
    echo "⚠️  pyngrok not available — ngrok tunnel disabled"
fi

# --- Step 7: Print Status & Start Server ---
echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                    🌿 AgriChain Ready!                  ║"
echo "╠══════════════════════════════════════════════════════════╣"
echo "║                                                         ║"
echo "  🌐 Local:      http://127.0.0.1:8000"
echo "  🌍 Public:     $NGROK_URL"
echo "  ⛓️  Blockchain: $BLOCKCHAIN_STATUS"
echo "║                                                         ║"
echo "  📌 Admin:      admin / admin"
echo "║                                                         ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down..."
    [ ! -z "$GANACHE_PID" ] && kill $GANACHE_PID 2>/dev/null
    python -c "from pyngrok import ngrok; ngrok.kill()" 2>/dev/null
    echo "👋 Goodbye!"
}
trap cleanup EXIT

# Start Django
python manage.py runserver 0.0.0.0:8000
