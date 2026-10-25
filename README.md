# ⚡ LocalStore DigitalBooster

A full-stack web application to help local stores manage their digital presence — inventory, campaigns, analytics, and more.

---

## 📁 Project Structure

```
localstore-digitalbooster/
│
├── app.py                        # Flask entry point
├── requirements.txt              # Python dependencies
├── seed_data.py                  # MongoDB seed script
├── .env.example                  # Environment variable template
│
├── backend/
│   ├── __init__.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── db.py                 # MongoDB connection
│   ├── models/
│   │   ├── __init__.py
│   │   ├── store.py              # Store schema & validation
│   │   ├── product.py            # Product schema & validation
│   │   └── campaign.py           # Campaign schema & validation
│   └── routes/
│       ├── __init__.py
│       ├── stores.py             # /api/stores  (CRUD)
│       ├── products.py           # /api/products (CRUD)
│       ├── campaigns.py          # /api/campaigns (CRUD)
│       └── analytics.py          # /api/analytics (aggregations)
│
└── frontend/
    ├── index.html                # Dashboard / Landing
    ├── css/
    │   └── style.css             # All styles
    ├── js/
    │   ├── main.js               # Shared utilities
    │   └── api.js                # API wrapper (fetch)
    └── pages/
        ├── stores.html           # Store management
        ├── products.html         # Product inventory
        ├── analytics.html        # Analytics & charts
        └── campaigns.html        # Campaign manager
```

---

## 🚀 Setup & Run

### Prerequisites
- Python 3.10+
- MongoDB (running locally on port 27017) or MongoDB Atlas
- A modern browser

---

### 1. Clone / Set up the project

```bash
cd localstore-digitalbooster
```

### 2. Create Python virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment

```bash
cp .env.example .env
# Edit .env if needed (default uses localhost MongoDB)
```

### 5. Start MongoDB

```bash
# Mac (Homebrew)
brew services start mongodb-community

# Linux
sudo systemctl start mongod

# Windows
net start MongoDB
```

### 6. (Optional) Seed sample data

```bash
python seed_data.py
```

### 7. Start Flask backend

```bash
python app.py
# API runs on http://localhost:5000
```

### 8. Open the frontend

Open `frontend/index.html` in your browser.  
*(Or use VS Code Live Server / any static file server)*

---

## 🔌 API Endpoints

### Stores — `/api/stores`
| Method | Endpoint             | Description          |
|--------|----------------------|----------------------|
| GET    | `/api/stores/`       | List all stores      |
| GET    | `/api/stores/<id>`   | Get single store     |
| POST   | `/api/stores/`       | Create store         |
| PUT    | `/api/stores/<id>`   | Update store         |
| DELETE | `/api/stores/<id>`   | Delete store         |
| PATCH  | `/api/stores/<id>/toggle` | Toggle active   |

### Products — `/api/products`
| Method | Endpoint                   | Description           |
|--------|----------------------------|-----------------------|
| GET    | `/api/products/`           | List all products     |
| GET    | `/api/products/<id>`       | Get single product    |
| POST   | `/api/products/`           | Create product        |
| PUT    | `/api/products/<id>`       | Update product        |
| DELETE | `/api/products/<id>`       | Delete product        |
| PATCH  | `/api/products/<id>/stock` | Update stock qty      |

### Campaigns — `/api/campaigns`
| Method | Endpoint                     | Description          |
|--------|------------------------------|----------------------|
| GET    | `/api/campaigns/`            | List all campaigns   |
| POST   | `/api/campaigns/`            | Create campaign      |
| PUT    | `/api/campaigns/<id>`        | Update campaign      |
| DELETE | `/api/campaigns/<id>`        | Delete campaign      |
| PATCH  | `/api/campaigns/<id>/stats`  | Update stats         |

### Analytics — `/api/analytics`
| Method | Endpoint                          | Description              |
|--------|-----------------------------------|--------------------------|
| GET    | `/api/analytics/summary`          | Platform summary stats   |
| GET    | `/api/analytics/stores-by-category` | Store distribution     |
| GET    | `/api/analytics/products-by-category` | Product distribution |
| GET    | `/api/analytics/top-stores`       | Top stores by products   |

---

## 🛠️ Tech Stack

| Layer     | Technology           |
|-----------|----------------------|
| Frontend  | HTML5, CSS3, Vanilla JavaScript |
| Backend   | Python 3, Flask      |
| Database  | MongoDB (PyMongo)    |
| Fonts     | Syne + DM Sans (Google Fonts) |

---

## 🌐 MongoDB Atlas (Cloud)

To use MongoDB Atlas instead of local MongoDB:

1. Create a free cluster at [mongodb.com/atlas](https://mongodb.com/atlas)
2. Get your connection string
3. Update `.env`:
```
MONGO_URI=mongodb+srv://<user>:<password>@cluster.mongodb.net/
DB_NAME=digitalbooster
```
