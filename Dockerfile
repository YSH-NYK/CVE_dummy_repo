# Base image deliberately vulnerable for OS package CVE testing (CVE-2021-3711 in openssl)
FROM alpine:3.14.0

LABEL maintainer="Sentinel CVE Fixer Team"
LABEL description="Demo container image for Locator Agent testing"

WORKDIR /app

# Install OS packages and build dependencies for Python / Node modules
RUN apk add --no-cache openssl curl python3 py3-pip nodejs npm build-base python3-dev jpeg-dev zlib-dev

# Copy dependency specifications
COPY requirements.txt .
COPY package.json package-lock.json ./

# Upgrade pip and install Python and Node.js dependencies inside the container
RUN pip3 install --no-cache-dir --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt
RUN npm install --no-package-lock --production

# Copy application source
COPY src/ ./src/

EXPOSE 8080

CMD ["python3", "src/app.py"]
