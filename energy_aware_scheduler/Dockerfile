# Use official Python runtime as a parent image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY energy_aware_scheduler/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY energy_aware_scheduler /app/energy_aware_scheduler
COPY energy_aware_scheduler/web_dashboard /app/web_dashboard

# Expose port for Flask server
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=energy_aware_scheduler.k8s_plugin.server
ENV FLASK_RUN_HOST=0.0.0.0

# Start the Flask server
CMD ["flask", "run"]
