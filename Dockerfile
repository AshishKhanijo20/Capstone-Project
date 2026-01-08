# ---------- Base image ----------
FROM python:3.11-slim

# ---------- Environment ----------
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ---------- System dependencies ----------
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ---------- Working directory ----------
WORKDIR /app

# ---------- Python dependencies ----------
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ---------- Application code ----------
COPY . .

# ---------- Expose port ----------
EXPOSE 8000

# ---------- Run server ----------
CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000"]
