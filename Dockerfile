FROM python:3.9-slim
WORKDIR /app

# Copy only necessary files
COPY  MainScores.py Score.py Utils.py requirements.txt scores_file.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Ensure Scores.txt is writable
RUN chmod a+rw scores_file.txt

# Expose port 8777
EXPOSE 8777

# Run the Flask server
CMD ["python","MainScores.py"]
