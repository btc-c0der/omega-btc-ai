FROM python:3.9-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . /app/src/omega_bot_farm/qa/tech_debt_bot/

# Expose port for health checks
EXPOSE 8083

# Run the tech debt voider
CMD ["python", "/app/src/omega_bot_farm/qa/tech_debt_bot/tech_debt_v001d3r.py", "-d"] 