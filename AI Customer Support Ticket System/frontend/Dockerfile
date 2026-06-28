# Base Image
FROM python:3.10-slim

# Working Directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all frontend files
COPY . .

# Run Streamlit
CMD ["streamlit", "run", "app.py", "--server.port", "8505", "--server.address", "0.0.0.0"]