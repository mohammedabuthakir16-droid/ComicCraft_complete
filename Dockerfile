FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

ENV PORT=8000
ENV HOST=0.0.0.0
ENV DEBUG=false

EXPOSE 8000

CMD ["sh", "-c", "uvicorn run:app --host 0.0.0.0 --port ${PORT:-8000}"]
