FROM python:3.11-slim

# Set working dir
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ project
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Streamlit yêu cầu disable CORS/HEADLESS trong container
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLECORS=false
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

CMD ["streamlit", "run", "gui.py"]
