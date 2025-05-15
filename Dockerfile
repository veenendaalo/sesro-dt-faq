# 1) use a full Python image so pip installs reliably
FROM python:3.10

# 2) upgrade pip early
RUN pip install --upgrade pip

# 3) set working dir
WORKDIR /app

# 4) copy & install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5) copy your app & data
COPY app.py .
COPY faq.xlsx .

# 6) expose the app port
EXPOSE 8501

# 7) launch via python -m to guarantee Streamlit is found
CMD ["python", "-m", "streamlit", "run", "app.py", \
     "--server.port=8501", "--server.address=0.0.0.0"]
