FROM python:3.11-slim-buster
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

# Install supervisor
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    --no-install-recommends supervisor \
    && rm -rf /var/lib/apt/lists/*

# Configure supervisor (create a config file)
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Set the entry point to start supervisor
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]