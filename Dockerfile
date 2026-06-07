FROM python:3.12-slim

# Install system-level Git required by gitpython
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

# 🚀 FIX: Install the lightweight CPU version of torch before anything else
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# Install the rest of your requirements (pip will now skip downloading heavy torch wheels)
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]