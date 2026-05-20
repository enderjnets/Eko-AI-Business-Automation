FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (incl. runtime libs for Playwright/Chromium
# used by Scrapling Phase 2 StealthyFetcher — anti-bot browser-rendered fetches)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    postgresql-client \
    curl \
    libnspr4 libnss3 libatk-bridge2.0-0 libcups2 libxkbcommon0 \
    libxcomposite1 libxdamage1 libxrandr2 libgbm1 libpango-1.0-0 \
    libcairo2 libasound2 libatspi2.0-0 libxshmfence1 libxfixes3 \
    fonts-liberation fonts-noto-color-emoji \
    && rm -rf /var/lib/apt/lists/*

# Install uv (Python package manager)
RUN curl -LsSf https://astral.sh/uv/install.sh | bash
ENV PATH="/root/.local/bin:${PATH}"

# Install Kimi CLI
RUN uv tool install kimi-cli

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download Chromium for Playwright/Patchright (used by Scrapling StealthyFetcher).
# ~150MB but cached as a Docker layer between rebuilds when requirements unchanged.
RUN patchright install chromium || playwright install chromium

# Copy application code
COPY . .

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
