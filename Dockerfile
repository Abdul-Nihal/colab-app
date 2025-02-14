# Use a suitable base image for your Flask app.
# Python slim is generally a good choice for size optimization
FROM python:3.9-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first to leverage Docker's caching
COPY requirements.txt .

# Install project dependencies
RUN pip install -r requirements.txt --no-cache-dir

# Copy the rest of the application code
COPY . .

# Expose the port your Flask app listens on (default is 5000)
EXPOSE 5000

# Set environment variables if needed (e.g., for database connections)
# ENV DATABASE_URL="your_database_url"

# Define the command to run when the container starts

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "main:app"]
# Using Gunicorn for production WSGI server
# (or) For Development: CMD ["python", "app.py"]