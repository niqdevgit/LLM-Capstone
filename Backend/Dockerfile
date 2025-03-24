# Use Python as the base image
FROM python:3.10

RUN mkdir /k2xml
# Set the working directory inside the container
WORKDIR /app

# Install dependencies for Mono
RUN apt-get update && apt-get install -y \
    mono-runtime \
    libmono-system-windows-forms4.0-cil \
    libmono-cil-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file and install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Expose the port Flask runs on
EXPOSE 5000

# Run the application
CMD ["python", "main.py"]
