# No-Code Text-to-SQL Analysis Agent

An end-to-end full-stack app that converts natural language into SQL, runs safe read-only queries, and shows results in a web UI.

## Demo video Here : 
  https://youtu.be/yJ8fh5NxpYI

## Features

- Upload CSV/XLSX datasets
- Store uploads as MySQL tables
- Generate SQL from natural language using LLM (Groq default)
- Validate and allow only SELECT-style queries
- Execute SQL and render table + chart output
- Detect table relationships (declared FK + inferred `*_id` joins)
- Keep query history (latest 3 shown in UI)

## Project Structure

```text
backend/
  app.py
  routes/
  services/
  database/
  utils/

frontend/
  pages/
  components/
  services/
```

## Tech Stack

- Backend: FastAPI, SQLAlchemy, PyMySQL, Pandas
- Frontend: React (Vite), Axios, Recharts
- LLM: Groq (OpenAI-compatible API client)

## Backend Setup

1. Create MySQL database:

```sql
CREATE DATABASE text_to_sql_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. Configure environment:

```powershell
cd backend
Copy-Item .env.example .env
```

3. Set `GROQ_API_KEY` in `backend/.env` and keep:

```dotenv
LLM_PROVIDER=groq
```

4. Install dependencies and run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Run from project root:

```powershell
cd ..
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Or run from backend:

```powershell
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Backend URL: [http://localhost:8000](http://localhost:8000)

## Frontend Setup

```powershell
cd frontend
Copy-Item .env.example .env
npm install
npm run dev
```

Frontend URL: [http://localhost:5173](http://localhost:5173)

## API Endpoints

- `POST /api/upload` Upload CSV/XLSX and import to MySQL
- `POST /api/query` Natural language to SQL execution
- `GET /api/schema` Table schema and detected relationships
- `GET /api/datasets` Uploaded dataset metadata
- `GET /api/history` Query history (default latest 3)
- `GET /health` Health check

## Example Multi-Table Data

Use these pair of files:

- `customers.csv` with `id`
- `orders.csv` with `customer_id`

Then ask:

- Show each order with customer name and city
- Total completed order amount by customer
- Customers with no completed orders

## Safety

- Blocks destructive SQL keywords (`DROP`, `DELETE`, `UPDATE`, `ALTER`, etc.)
- Prevents multi-statement execution
- Adds row limit when query has no `LIMIT`

## Notes

- Do not commit `.env` files or secrets.
- If CORS errors appear in browser, verify backend is running and `/api/schema` returns `200`.
