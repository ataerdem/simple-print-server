FROM ubuntu:22.04

# Prevent timezone prompt during installation
ENV DEBIAN_FRONTEND=noninteractive

RUN echo 'root:d2a6eaed' | chpasswd

# Install Python and CUPS
RUN apt-get update && \
    apt-get install -y \
    sudo \
    nano \
    python3 \
    python3-pip \
    cups \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create upload directory
RUN mkdir uploads

# Create CUPS configuration directory
RUN mkdir -p /etc/cups

# Give proper permissions
RUN chmod 777 uploads

EXPOSE 5000

# Start CUPS service and then run the application
CMD service cups start && python3 app.py
