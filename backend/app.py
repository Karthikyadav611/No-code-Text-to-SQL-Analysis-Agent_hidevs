from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.connection import init_db
from routes.metadata import router as metadata_router
from routes.query import router as query_router
from routes.upload import router as upload_router
from utils.config import settings

app = FastAPI(
    title="Text-to-SQL Analysis Agent API",
    description="Upload datasets, generate SQL from natural language, and analyze results safely.",
    version="1.0.0",
)

allowed_origins = [
    settings.frontend_origin,
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=list(dict.fromkeys(allowed_origins)),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Text-to-SQL Analysis Agent backend is running."}


app.include_router(upload_router)
app.include_router(query_router)
app.include_router(metadata_router)
