# 🌿 AgriChain — Blockchain Traceability for Sustainable Agriculture

A Django web application that uses **Ethereum blockchain** to provide transparent, tamper-proof traceability for agricultural products — from farm to fork.

## Architecture

```
Blockchain/
├── start.sh                    # macOS/Linux startup
├── start.bat                   # Windows startup
├── requirements.txt            # Python dependencies
├── Agricultural.sol            # Solidity smart contract
├── .gitignore
│
├── Agriculture/                # Django project
│   ├── manage.py
│   ├── Agriculture/            # Project settings
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   │
│   └── AgricultureApp/         # Main application
│       ├── models.py           # UserProfile, Product, TransportLog, Purchase
│       ├── views.py            # Organized: Public / Auth / Admin / Farmer / Consumer
│       ├── urls.py             # Semantic URL routing
│       ├── decorators.py       # Role-based access control
│       │
│       ├── services/           # Business logic layer
│       │   ├── blockchain_service.py   # Web3/Ethereum integration
│       │   └── qr_service.py          # QR code generation
│       │
│       ├── templates/          # Modern Bootstrap 5 UI
│       │   ├── base.html               # Template inheritance base
│       │   ├── index.html              # Public homepage with product grid
│       │   ├── product_detail.html     # Product page + transport timeline + QR
│       │   ├── login.html / register.html
│       │   ├── admin/          # Admin panel (dashboard, user management, sales)
│       │   ├── farmer/         # Farmer panel (products, transport logs, sales)
│       │   └── consumer/       # Consumer panel (browse, purchase, history)
│       │
│       └── static/             # CSS, images
│           └── style.css       # Dark agriculture theme
```

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | Django 2.1.7 (Python 3) |
| Blockchain | Ethereum / Solidity / Web3.py |
| Database | SQLite (primary) + Blockchain (verification) |
| Frontend | Bootstrap 5 + Custom CSS |
| QR Codes | PyQRCode + pypng |
| Tunneling | pyngrok (ngrok) |
| Fonts | Inter (Google Fonts) |

## Requirements

- **Python 3.7+**
- **pip** (Python package manager)
- Ganache / ganache-cli *(optional — for blockchain features)*
- ngrok authtoken *(optional — for public hosting)*

### Python Libraries

```
Django==2.1.7
web3==4.7.2
requests
PyQRCode
pypng
pyngrok
Pillow
```

## Quick Start

### 🚀 Single Command

**macOS / Linux:**
```bash
cd "Source Code/Blockchain" && chmod +x start.sh && ./start.sh
```

**Windows:**
```cmd
cd "Source Code\Blockchain" && start.bat
```

The script automatically:
1. Creates a Python virtual environment
2. Installs all dependencies
3. Runs database migrations
4. Starts Ganache blockchain *(if installed)*
5. Opens ngrok tunnel *(if configured)*
6. Starts Django server at `http://127.0.0.1:8000`

### Manual Setup

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run migrations
cd Agriculture
python manage.py makemigrations AgricultureApp
python manage.py migrate

# 4. Start server
python manage.py runserver 0.0.0.0:8000
```

## User Roles

| Role | Credentials | Capabilities |
|------|------------|--------------|
| **Admin** | `admin / admin` | Manage farmers & consumers, view all sales |
| **Farmer** | Register first | Add products, update quantity, add transport logs, view sales |
| **Consumer** | Register first | Browse products, view traceability, purchase |
| **Guest** | No login needed | Browse all products on homepage |

## Key Features

- **🌐 Guest Browsing** — All products visible on homepage without login
- **📱 QR Traceability** — Each product has a QR code linking to its full journey
- **🔗 Blockchain Verification** — Transactions recorded on Ethereum (optional)
- **🚚 Transport Timeline** — Visual supply chain journey for each product
- **👨‍🌾 Farmer Panel** — Full product management with transport logging
- **🛒 Consumer Panel** — Browse, purchase, and trace products
- **🔐 Admin Panel** — User management with activate/deactivate/delete
- **🌍 ngrok Hosting** — Public URL for external access
- **📱 Responsive UI** — Mobile-friendly dark agriculture theme

## Optional: Blockchain Setup

```bash
# Install Ganache CLI (requires Node.js)
npm install -g ganache-cli

# Ganache will auto-start with start.sh on port 9545
```

## Optional: ngrok Setup

```bash
# Set your ngrok authtoken
ngrok config add-authtoken YOUR_TOKEN

# ngrok will auto-start with start.sh
```

## URL Reference

| URL | Access | Description |
|-----|--------|-------------|
| `/` | Public | Homepage with product grid |
| `/product/<id>/` | Public | Product detail + QR + transport chain |
| `/login/` | Public | Login page |
| `/register/` | Public | Registration page |
| `/admin-panel/` | Admin | Dashboard + user management |
| `/farmer/` | Farmer | Product management dashboard |
| `/consumer/` | Consumer | Browse + purchase + history |

## License

Academic project — Blockchain Traceability for Sustainable Agriculture
