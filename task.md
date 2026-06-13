# 🛒 E-Commerce Sentiment Pipeline Tasks

## 📅 Day 1: Infrastructure & Backend

### Phase 1: Project Initialization & Infrastructure Scaffold
- `[x]` Create the root directory `C:\cpp\EcommerceSentimentPipeline`.
- `[x]` Create an `.env.example` file with configuration placeholders (Database credentials, Kafka brokers).
- `[x]` **Create `docker-compose.yml`**:
  - `[x]` Define `postgres` service (PostgreSQL 15+) with persistent volume mapping.
  - `[x]` Define `zookeeper` service for Kafka orchestration.
  - `[x]` Define `kafka` service with exposed ports (9092) and configurations.
  - `[x]` Configure an isolated Docker bridge network (e.g., `pipeline-net`).

### Phase 2: Django Backend Setup & App Scaffold
- `[x]` Create a `backend` subdirectory.
- `[x]` Initialize Django project (`config`) and create the `reviews` app.
- `[x]` Create `backend/requirements.txt` (needs `django`, `djangorestframework`, `psycopg2-binary`, `kafka-python`, `dj-database-url`).
- `[x]` Configure `settings.py` to use PostgreSQL via `dj-database-url` and add REST Framework.

### Phase 3: Core Business Logic (Fat Models & Thin Views)
- `[x]` Define `Product` model in `reviews/models.py` (name, description, price, created_at).
- `[x]` Define `Review` model in `reviews/models.py` (product FK, text, rating, sentiment_score, sentiment_label, created_at).
- `[x]` Create initial database migrations for the new models.
- `[x]` Create `reviews/serializers.py` with `ProductSerializer` and `ReviewSerializer`.
- `[x]` Create `reviews/views.py` using DRF `ModelViewSet` to maintain thin views.
- `[x]` Configure `urls.py` routers for the API endpoints.

### Phase 4: Kafka Producer Integration
- `[x]` Create `reviews/kafka_producer.py` to handle the Kafka connection.
- `[x]` Implement a helper function to publish review payloads (Review ID, Product ID, Text).
- `[x]` Hook into Django's `post_save` signal on the `Review` model to trigger the producer.
- `[x]` Ensure the producer executes asynchronously (e.g., via `threading.Thread`).

### Phase 5: Containerization (Backend)
- `[x]` Write `backend/Dockerfile` using a lightweight Python base image (`python:3.11-slim`).
- `[x]` Create an `entrypoint.sh` script to auto-run DB migrations and start Django.
- `[x]` Add the `django_backend` service to `docker-compose.yml`, depending on `postgres` and `kafka`.

---

## 📅 Day 2: Stream Processing, Frontend, & E2E Testing

### Phase 6: NLP Consumer (Stream Processing)
- `[x]` Create a `consumer` subdirectory.
- `[x]` Create `consumer/requirements.txt` (needs `kafka-python`, `psycopg2-binary`, `nltk`, `vaderSentiment`).
- `[x]` Write `consumer/Dockerfile` using a lightweight Python base image.
- `[x]` Develop `consumer/main.py` Python NLP Consumer script using NLTK/VADER.
- `[x]` Implement PostgreSQL connection pooling and retry mechanisms in the consumer to update `Review` records.
- `[x]` Add `nlp_consumer` service to `docker-compose.yml`, depending on `postgres` and `kafka`.

### Phase 7: Frontend Application (Streamlit)
- `[x]` Create a `frontend` subdirectory.
- `[x]` Create `frontend/requirements.txt` (needs `streamlit`, `pandas`, `requests`, `plotly`).
- `[x]` Write `frontend/Dockerfile` for the Streamlit application.
- `[x]` Build `frontend/app.py` Streamlit Dashboard for sentiment visualization.
- `[x]` Implement state management and data polling (calling Django API) in Streamlit.
- `[x]` Add `streamlit_frontend` service to `docker-compose.yml`, depending on `django_backend`.

### Phase 8: End-to-End Testing & Polish
- `[x]` Run `docker-compose up --build` to orchestrate all services.
- `[x]` Seed the database with sample products via the Django admin or API.
- `[x]` Send mock reviews via API and verify Kafka message delivery.
- `[x]` Verify the consumer correctly calculates sentiment and updates DB records.
- `[x]` Verify the Streamlit dashboard updates in real-time.
