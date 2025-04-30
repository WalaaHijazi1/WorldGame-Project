FROM python:3.9-slim
WORKDIR /app

RUN apt-get update && apt-get install -y \
    chromium chromium-driver \
    fonts-liberation \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libnspr4 \
    libnss3 \
    libxss1 \
    xdg-utils \
    wget unzip

# Set environment variables for Chrome
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/lib/chromium/chromedriver
ENV PATH="${CHROMEDRIVER_PATH}:${PATH}"

# Link ChromeDriver to a location in PATH
RUN ln -sf /usr/lib/chromium/chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/lib/chromium/chro

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