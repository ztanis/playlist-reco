FROM python:3.11-slim

WORKDIR /app

# Install UV package manager
RUN pip install uv

# Copy requirements file
COPY requirements.txt .

# Create virtual environment and install dependencies
RUN uv venv && \
    . .venv/bin/activate && \
    uv pip install -r requirements.txt

# Copy the application code
COPY . .

# Expose the port Streamlit runs on
EXPOSE 8501

# Set the PATH to include the virtual environment's bin directory
ENV PATH="/app/.venv/bin:$PATH"

# Command to run the application
CMD ["streamlit", "run", "main.py", "--server.address", "0.0.0.0"] 