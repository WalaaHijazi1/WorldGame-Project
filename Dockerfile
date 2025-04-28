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

EXPOSE 8777

CMD ["python", "Live.py"]