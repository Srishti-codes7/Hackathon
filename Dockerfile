# 1. Base image with Python installed
FROM python:3.11-slim

# 2. Prevent Python from buffering stdout/stderr (helps with real-time logging)
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# 3. Set the working directory inside the container
WORKDIR /app

# 4. Copy requirements first to leverage Docker layer caching
COPY requirements.txt .

# 5. Install dependencies without caching the installation files
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the rest of your application code
COPY . .

# 7. Expose the port your app runs on (adjust if using 8000 for FastAPI/Django or 5000 for Flask)
EXPOSE 8000

# 8. Command to start your application (replace app.py with your entry point)
CMD ["python", "app.py"]