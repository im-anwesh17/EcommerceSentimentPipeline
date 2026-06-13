# Live E-Commerce Sentiment Analysis Pipeline

An end-to-end sentiment analysis pipeline designed to process e-commerce product reviews in real time. Built with Django, Kafka, Python (NLTK/VADER), PostgreSQL, and Streamlit, all fully containerized with Docker Compose.

## Architecture

1. **Django REST API (Backend)**: Receives new product reviews via HTTP POST. 
2. **Kafka Producer**: Django publishes the review payload to a Kafka topic (`reviews_topic`) asynchronously.
3. **Zookeeper & Kafka**: Manages the message broker queuing system.
4. **NLP Consumer**: A Python background service that listens to the Kafka topic, processes the review text using the VADER sentiment analysis model, calculates a `sentiment_score` (-1.0 to 1.0) and a `sentiment_label` (Positive, Neutral, Negative), and persists the results.
5. **PostgreSQL**: Stores the Products and Reviews.
6. **Streamlit (Frontend)**: A real-time dashboard that polls the Django API to display sentiment distribution charts and the latest processed reviews.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Local Development & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/EcommerceSentimentPipeline.git
   cd EcommerceSentimentPipeline
   ```

2. **Environment Variables**
   Create a `.env` file based on `.env.example` in the root directory:
   ```env
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_DB=sentiment_db
   ```

3. **Orchestrate Services**
   Spin up all 6 containers (Django, Kafka, Zookeeper, Postgres, NLP Consumer, and Streamlit):
   ```bash
   docker-compose up --build -d
   ```

4. **Seed the Database**
   Populate the database with sample products to begin posting reviews:
   ```bash
   docker-compose exec django_backend python manage.py migrate
   docker-compose exec django_backend python seed.py
   ```

5. **Access the Application**
   - **Streamlit Dashboard**: [http://localhost:8501](http://localhost:8501)
   - **Django API**: [http://localhost:8000/api/](http://localhost:8000/api/)

## Testing the Pipeline

To simulate a real-time review arriving at the backend:
```bash
curl -X POST http://localhost:8000/api/reviews/ \
     -H "Content-Type: application/json" \
     -d '{"product": 1, "text": "This product is absolutely amazing and I love the quality!", "rating": 5}'
```
You will immediately see the review processed and reflected on the Streamlit dashboard!

## Technologies Used

- **Python 3.11**
- **Django & Django REST Framework**
- **Apache Kafka & Confluent Kafka Python Client**
- **NLTK (VADER Sentiment)**
- **Streamlit & Plotly**
- **PostgreSQL**
- **Docker & Docker Compose**
