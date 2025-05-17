FROM python:3.11-slim

WORKDIR /app

# Install UV package manager
RUN pip install uv

# Copy requirements file
COPY requirements.txt .

# Install dependencies using UV
RUN uv pip install -r requirements.txt

# Copy the application code
COPY . .

# Expose the port Streamlit runs on
EXPOSE 8501

# Command to run the application
CMD ["streamlit", "run", "main.py", "--server.address", "0.0.0.0"] 