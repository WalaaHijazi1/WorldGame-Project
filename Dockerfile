FROM python:3.9-slim
WORKDIR /app

# Copy only necessary files
COPY  Live.py Score.py  requirements.txt  ./

# Copy HTML templates
COPY templates/ templates/

# Copy static files (CSS, JS, images)
COPY static/ static/

# Install required Python packages
RUN pip3 install --no-cache-dir -r requirements.txt

# Install basic Linux packages
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN curl -fsSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable

EXPOSE 8777

CMD ["python", "Live.py"]