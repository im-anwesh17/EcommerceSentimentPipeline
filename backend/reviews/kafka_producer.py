import json
import threading
import logging
from kafka import KafkaProducer
from django.conf import settings

logger = logging.getLogger(__name__)

# Initialize the producer lazily to avoid connection issues during tests/migrations
_producer = None

def get_producer():
    global _producer
    if _producer is None:
        try:
            _producer = KafkaProducer(
                bootstrap_servers=settings.KAFKA_BROKERS,
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
        except Exception as e:
            logger.error(f"Error connecting to Kafka: {e}")
    return _producer

def publish_review_message(review_id, product_id, text):
    """
    Publish a review message to Kafka.
    """
    producer = get_producer()
    if producer:
        try:
            payload = {
                'review_id': review_id,
                'product_id': product_id,
                'text': text
            }
            # Fire and forget (or could add callback if needed)
            producer.send(settings.KAFKA_REVIEW_TOPIC, value=payload)
            producer.flush()
        except Exception as e:
            logger.error(f"Failed to publish review to Kafka: {e}")

def publish_review_async(review_id, product_id, text):
    """
    Run publish_review_message in a background thread to avoid blocking the request.
    """
    thread = threading.Thread(
        target=publish_review_message,
        args=(review_id, product_id, text)
    )
    thread.daemon = True
    thread.start()
