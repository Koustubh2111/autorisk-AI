# Use official Python image as base
FROM python:latest

# Set working directory inside container
WORKDIR /app

# Copy requirements first (for better cache)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy API code into container
COPY ./api/risk_scoring_api.py .

# Expose port (uvicorn default)
EXPOSE 8000

# Run the API server with reload (for dev, remove --reload in prod)
CMD ["uvicorn", "risk_scoring_api:app", "--host", "0.0.0.0", "--port", "8000"]
