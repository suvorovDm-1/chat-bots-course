FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN python -m venv /app/venv && \
    /app/venv/bin/pip install --upgrade pip && \
    /app/venv/bin/pip install --no-cache-dir -r requirements.txt

COPY bot/ ./bot/

ENV PATH="/app/venv/bin:$PATH"

CMD ["python", "-m", "bot"]
