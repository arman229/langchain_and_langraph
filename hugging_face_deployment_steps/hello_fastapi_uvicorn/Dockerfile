FROM python:3.12-slim 
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/ 
COPY . /app 
WORKDIR /app
RUN uv sync --frozen --no-cache 
CMD ["/app/.venv/bin/uvicorn", "chatbot.main:app","--host", "0.0.0.0", "--port", "7860"]