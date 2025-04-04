# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirement.txt ./
RUN pip install --no-cache-dir -r requirement.txt

# Copy the rest of the app files
COPY . .

# Expose port 5000
EXPOSE 5000

# Start the Flask server
CMD ["python", "app.py"]
