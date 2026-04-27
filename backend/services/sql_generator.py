import re
from openai import OpenAI
from utils.config import settings


class SQLGeneratorService:
    def __init__(self) -> None:
        self.client = self._build_client()

    def _build_client(self) -> OpenAI | None:
        # If no API key → disable LLM
        if not settings.resolved_llm_api_key:
            return None

        client_kwargs = {
            "api_key": settings.resolved_llm_api_key
        }

        # Add base_url ONLY if present (important for Groq)
        if settings.resolved_llm_base_url:
            client_kwargs["base_url"] = settings.resolved_llm_base_url

        return OpenAI(**client_kwargs)

    def _build_prompt(self, natural_language_query: str, schema_text: str) -> str:
        return f"""You are an expert SQL generator.

Database schema:
{schema_text}

Convert the following natural language query into SQL.
Return ONLY SQL query without explanation.

Few-shot examples:

Question: Show the first 10 rows from sales_data
SQL: SELECT * FROM sales_data LIMIT 10;

Question: What is total revenue by region?
SQL: SELECT region, SUM(revenue) AS total_revenue
FROM sales_data
GROUP BY region
ORDER BY total_revenue DESC;

Question: How many orders were placed each month?
SQL: SELECT DATE_FORMAT(order_date, '%Y-%m') AS order_month, COUNT(*) AS total_orders
FROM sales_data
GROUP BY order_month
ORDER BY order_month;

Natural language query:
{natural_language_query}

SQL:
"""

    @staticmethod
    def _clean_model_output(raw_output: str) -> str:
        output = (raw_output or "").strip()

        # Remove ```sql ... ```
        output = re.sub(r"^```(?:sql)?\s*", "", output, flags=re.IGNORECASE)
        output = re.sub(r"\s*```$", "", output)

        return output.strip()

    def generate_sql(self, natural_language_query: str, schema_text: str) -> str:
        if not self.client:
            raise RuntimeError(
                f"Missing API key for provider '{settings.llm_provider}'. "
                "Update backend/.env with valid LLM credentials."
            )

        try:
            response = self.client.chat.completions.create(
                model=settings.resolved_llm_model,
                messages=[
                    {
                        "role": "user",
                        "content": self._build_prompt(natural_language_query, schema_text)
                    }
                ],
                temperature=0
            )

            content = response.choices[0].message.content if response.choices else ""
            return self._clean_model_output(content or "")

        except Exception as e:
            raise RuntimeError(f"LLM request failed: {str(e)}")


# Singleton instance
sql_generator_service = SQLGeneratorService()