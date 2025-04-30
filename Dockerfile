FROM python:3.9-slim
WORKDIR /app

# Install Chromium and ChromeDriver
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    fonts-liberation \
    libnss3 \
    libxss1 \
    libappindicator3-1 \
    libasound2 \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for Selenium
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/lib/chromium/chromedriver

# Copy only necessary files
COPY  Live.py Score.py  requirements.txt  ./

# Copy HTML templates
COPY templates/ templates/

# Copy static files (CSS, JS, images)
COPY static/ static/

# Install required Python packages
RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8777

CMD ["python", "Live.py"]