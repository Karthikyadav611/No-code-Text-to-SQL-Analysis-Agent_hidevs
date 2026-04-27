# Text-to-SQL Analysis Agent with User Data Upload

Production-ready full-stack project for "chat with your data" workflows:

- Upload CSV/XLSX files
- Store uploaded data as MySQL tables
- Ask natural-language questions
- Convert text to SQL via LLM (OpenAI or Groq)
- Validate SQL for safety (SELECT-only)
- Execute queries and return table/chart-friendly results
- Track query history with generated SQL and execution time

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

## Backend Setup (FastAPI + MySQL)

1. Create a MySQL database:
```sql
CREATE DATABASE text_to_sql_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. Configure environment:
```powershell
cd backend
Copy-Item .env.example .env
```

3. Install Python dependencies and run API:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Backend URL: [http://localhost:8000](http://localhost:8000)

## Frontend Setup (React + Vite)

1. Configure environment:
```powershell
cd frontend
Copy-Item .env.example .env
```

2. Install and run:
```powershell
npm install
npm run dev
```

Frontend URL: [http://localhost:5173](http://localhost:5173)

## API Endpoints

- `POST /api/upload` - Upload CSV/XLSX and import to MySQL
- `POST /api/query` - Natural language query -> SQL -> safe execution
- `GET /api/schema` - Current schema (used in LLM prompt)
- `GET /api/datasets` - Uploaded dataset list
- `GET /api/history` - Query history
- `GET /health` - API health check

## Safety Design

- SQL validation blocks non-SELECT/destructive operations
- Multiple statements are blocked
- Forbidden keywords blocked: `DROP`, `DELETE`, `UPDATE`, `ALTER`, etc.
- Optional automatic row limit applied for large result protection
- Errors are handled and returned cleanly to the UI

## LLM Prompt Template

The SQL generator uses the required format:

```text
You are an expert SQL generator.
Database schema:
{schema}

Convert the following natural language query into SQL.
Return ONLY SQL query without explanation.
```

Few-shot examples are appended to improve SQL quality.
