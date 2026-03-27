# EconVerse 🌍

Turn-based multiplayer macroeconomic world simulation.
Each player builds a nation from scratch. Trade, war, crises, diplomacy.

---

## Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the backend
```bash
uvicorn backend.main:app --reload
```

### 3. Open the frontend
Visit: http://localhost:8000

Or open `frontend/index.html` directly in your browser
(set API = "http://localhost:8000" in js/app.js — already set by default)

---

## API Docs
Visit: http://localhost:8000/docs

---

## Folder Structure
```
econverse/
├── backend/
│   ├── main.py                  # FastAPI app
│   ├── db.py                    # JSON storage
│   ├── models/
│   │   ├── world.py             # World data model
│   │   ├── country.py           # Country data model
│   │   ├── crisis.py            # Crisis & Rivalry definitions
│   │   └── institution.py       # WorldBank, UN, TradeUnion
│   ├── routes/
│   │   ├── world_routes.py      # /world/create, /world/list
│   │   └── country_routes.py    # /country/create, /country/options
│   ├── engine/
│   │   └── budget.py            # Starting stat calculator
│   └── data/
│       └── db.json              # Auto-created on first run
├── frontend/
│   ├── index.html               # Single page app
│   ├── css/style.css
│   └── js/app.js
├── requirements.txt
└── README.md
```

---

## How It Works

1. Someone creates a **World** (lobby opens)
2. Players join and **build their country** — name, geography, history, crises, budget
3. Crises and rivalries give **bonus coins** but add penalties
4. Budget allocation determines **starting stats**
5. Once all players ready — **Turn simulation begins** (next phase)

---

## Deploy (free)

**Backend → Render.com**
- Connect GitHub repo
- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`

**Frontend → Netlify / Vercel**
- Just drag the `frontend/` folder
- Update `API` in `js/app.js` to your Render URL

---

## Next Phase (Turn Engine)
- `engine/turn.py` — simulate one world turn
- Player action submission system
- World Bank loan mechanics  
- War resolution system
- Trade deal engine
- UN voting system
