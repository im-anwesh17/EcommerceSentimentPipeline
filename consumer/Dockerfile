FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Download necessary NLTK corpora during build to avoid runtime downloads
RUN python -m nltk.downloader vader_lexicon

COPY . /app/

CMD ["python", "main.py"]
