FROM python:3.12-slim 
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/ 
COPY . /app 
WORKDIR /app
RUN uv sync --frozen --no-cache 
CMD ["/app/.venv/bin/fastapi", "run", "chatbot/main.py", "--port", "7860", "--host", "0.0.0.0"]