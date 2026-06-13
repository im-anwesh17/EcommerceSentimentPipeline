import os
import json
import time
import psycopg2
from psycopg2 import pool
from kafka import KafkaConsumer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Configuration
KAFKA_BROKERS = os.environ.get('KAFKA_BROKERS', 'localhost:9092').split(',')
KAFKA_REVIEW_TOPIC = os.environ.get('KAFKA_REVIEW_TOPIC', 'reviews_topic')
DB_USER = os.environ.get('POSTGRES_USER', 'postgres')
DB_PASS = os.environ.get('POSTGRES_PASSWORD', 'postgres')
DB_NAME = os.environ.get('POSTGRES_DB', 'postgres')
DB_HOST = os.environ.get('POSTGRES_HOST', 'postgres')
DB_PORT = os.environ.get('POSTGRES_PORT', '5432')

# Setup VADER
analyzer = SentimentIntensityAnalyzer()

def get_db_pool(retries=5, delay=5):
    """
    Establish a connection pool to PostgreSQL with exponential backoff retry.
    """
    for i in range(retries):
        try:
            connection_pool = psycopg2.pool.SimpleConnectionPool(
                1, 10,
                user=DB_USER,
                password=DB_PASS,
                host=DB_HOST,
                port=DB_PORT,
                database=DB_NAME
            )
            if connection_pool:
                return connection_pool
        except Exception:
            time.sleep(delay * (2 ** i))
    raise Exception("Could not connect to PostgreSQL after multiple retries")

def analyze_sentiment(text):
    """
    Returns sentiment score and label using VADER.
    """
    scores = analyzer.polarity_scores(text)
    compound = scores['compound']
    
    if compound >= 0.05:
        label = 'Positive'
    elif compound <= -0.05:
        label = 'Negative'
    else:
        label = 'Neutral'
        
    return compound, label

def main():
    connection_pool = get_db_pool()
    
    consumer = KafkaConsumer(
        KAFKA_REVIEW_TOPIC,
        bootstrap_servers=KAFKA_BROKERS,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='nlp-consumer-group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    for message in consumer:
        payload = message.value
        review_id = payload.get('review_id')
        text = payload.get('text')
        
        if not review_id or not text:
            continue
            
        score, label = analyze_sentiment(text)
        
        conn = connection_pool.getconn()
        try:
            with conn.cursor() as cursor:
                # Update the review in the database securely using parameterized queries
                update_query = """
                    UPDATE reviews_review 
                    SET sentiment_score = %s, sentiment_label = %s 
                    WHERE id = %s
                """
                cursor.execute(update_query, (score, label, review_id))
            conn.commit()
        except Exception:
            conn.rollback()
        finally:
            connection_pool.putconn(conn)

if __name__ == "__main__":
    main()
