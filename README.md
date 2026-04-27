# 🚀 No-Code Text-to-SQL Analysis Agent

An intelligent full-stack application that converts **natural language queries into SQL**, executes them on a database, and returns results with optional analysis.

Built using **FastAPI + React + MySQL + LLM (Groq/OpenAI)**.

---

## 🌟 Features

* 🔤 Convert plain English questions into SQL queries
* 🧠 AI-powered SQL generation using LLMs (Groq / OpenAI)
* 🗄️ Automatic database schema detection
* 📊 Execute SQL and display results in table format
* 📝 Query history tracking
* 📁 Upload datasets dynamically
* ⚡ FastAPI backend with clean architecture
* 🎨 Modern responsive React frontend

---

## 🏗️ Project Architecture

```
text-to-sql/
│
├── backend/
│   ├── routes/            # API endpoints
│   ├── services/          # Business logic
│   ├── utils/             # Config & helpers
│   ├── app.py             # FastAPI entry point
│   └── .env               # Environment variables
│
├── frontend/
│   ├── src/
│   ├── components/
│   ├── pages/
│   └── App.jsx
│
└── README.md
```

---

## ⚙️ Tech Stack

### Backend

* FastAPI
* SQLAlchemy
* MySQL
* Uvicorn

### Frontend

* React (Vite)
* CSS

### AI Integration

* Groq API / OpenAI API

---

## 🔑 Environment Variables

Create a `.env` file inside `backend/`:

```
# Database
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=text_to_sql_db

# LLM Provider
LLM_PROVIDER=groq

# Groq
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile
GROQ_BASE_URL=https://api.groq.com/openai/v1

# OpenAI (optional)
OPENAI_API_KEY=your_openai_key
OPENAI_MODEL=gpt-4.1-mini

# Frontend
FRONTEND_ORIGIN=http://localhost:5173
```

---

## 🚀 How to Run the Project

### 🔹 1. Clone the repository

```
git clone https://github.com/your-username/your-repo.git
cd text-to-sql
```

---

### 🔹 2. Setup Backend

```
cd backend
pip install -r requirements.txt
```

Run server:

```
uvicorn app:app --reload
```

Backend runs at:

```
http://127.0.0.1:8000
```

---

### 🔹 3. Setup Frontend

```
cd frontend
npm install
npm run dev
```

Frontend runs at:

```
http://localhost:5173
```

---

## 🧠 How It Works

1. User enters a natural language query
   👉 Example: *"Show total revenue by region"*

2. Backend:

   * Fetches database schema
   * Formats schema into prompt
   * Sends prompt to LLM (Groq/OpenAI)

3. LLM generates SQL:

```sql
SELECT region, SUM(revenue)
FROM sales_data
GROUP BY region;
```

4. Backend executes SQL using SQLAlchemy

5. Results returned to frontend and displayed

---

## 📊 Example Queries

Try these:

* Show first 10 rows from mpg dataset
* What is average mpg by origin?
* Count number of cars per cylinder
* Which car has highest horsepower?
* Show cars with mpg > 30
* Average weight by model year

---

## 🛠️ Key Fixes & Learnings

* ✅ Fixed SQLAlchemy row mapping issue (`row._mapping`)
* ✅ Resolved OpenAI client proxy error
* ✅ Fixed schema extraction bug
* ✅ Configured Groq API correctly with base URL
* ✅ Handled API connection errors
* ✅ Cleaned LLM response formatting

---

## ⚠️ Important Notes

Never push `.env` file to GitHub

Add `.gitignore`:

```
.env
__pycache__/
node_modules/
```

---

## 📌 Future Improvements

* 📈 Add data visualization (charts)
* 🔐 Authentication system
* 🧾 Query saving & bookmarks
* 🤖 Chat-style conversational interface
* 📊 Auto insights generation

---

## 👨‍💻 Author

**Karthik Yadav**

* 💻 Information Science Engineering Student
* 🚀 Passionate about AI, Web Development & Data Systems

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub and share it!
