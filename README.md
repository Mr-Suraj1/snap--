# SnapSell - Product Photo Enhancer MVP

One-tap white background + enhancement for Indian online sellers.

## What it does
- Upload product photo from phone
- Removes background -> clean white background
- Auto-enhances light, color, sharpness
- Before / After view + HD download
- 5 free credits (localStorage), then paywall

## Run locally

Backend:
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app:app --host 0.0.0.0 --port 8000
```

Frontend:
Open `frontend/index.html` in browser, or serve:
```bash
cd frontend
python3 -m http.server 3000
# open http://localhost:3000
```

Note: Frontend expects backend at `http://localhost:8000/enhance`. Change `API_URL` in index.html when deploying.

## Deploy
- Backend: Render, Railway, or Hugging Face Spaces (free)
- Frontend: Vercel, Netlify (free) - update API_URL to your backend URL

## Time to build
- Day 1: UI done
- Day 2: Backend done
- Day 3: Credits + polish
- Day 4: Test with real seller photos

Total: 3-4 days part-time.
