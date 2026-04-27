import os
from dataclasses import dataclass
from urllib.parse import quote_plus

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    db_host: str = os.getenv("DB_HOST", "localhost")
    db_port: int = int(os.getenv("DB_PORT", "3306"))
    db_user: str = os.getenv("DB_USER", "root")
    db_password: str = os.getenv("DB_PASSWORD", "")
    db_name: str = os.getenv("DB_NAME", "text_to_sql_db")

    llm_provider: str = os.getenv("LLM_PROVIDER", "openai").strip().lower()

    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    openai_base_url: str = os.getenv("OPENAI_BASE_URL", "")

    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    groq_model: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    groq_base_url: str = os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1")

    frontend_origin: str = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
    max_result_rows: int = int(os.getenv("MAX_RESULT_ROWS", "500"))

    @property
    def sqlalchemy_database_uri(self) -> str:
        safe_password = quote_plus(self.db_password)
        return (
            f"mysql+pymysql://{self.db_user}:{safe_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}?charset=utf8mb4"
        )

    @property
    def resolved_llm_api_key(self) -> str:
        if self.llm_provider == "groq":
            return self.groq_api_key
        return self.openai_api_key

    @property
    def resolved_llm_base_url(self) -> str | None:
        if self.llm_provider == "groq":
            return self.groq_base_url
        return self.openai_base_url or None

    @property
    def resolved_llm_model(self) -> str:
        if self.llm_provider == "groq":
            return self.groq_model
        return self.openai_model


settings = Settings()
