# Live E-Commerce Sentiment Analysis Pipeline

This document outlines the implementation plan for a 2-day development sprint to build a Live E-Commerce Sentiment Analysis Pipeline using Python, Django, Apache Kafka, PostgreSQL, Streamlit, and Docker.

## Project Workspace
Based on your feedback, the project will be built in a completely new directory separate from existing projects: `C:\cpp\EcommerceSentimentPipeline`. 
For the NLP requirements, we will utilize NLTK with the VADER lexicon, effectively addressing the need for robust sentiment analysis.

## Proposed Changes

We will create a multi-container Docker application with the following components:

### Infrastructure (Docker Compose)
- **docker-compose.yml**: Defines services for Django, Kafka, Zookeeper, PostgreSQL, Streamlit, and the NLP Consumer. Configures isolated networks (e.g., `web-net`, `kafka-net`, `db-net`).
- **.env.example**: Template for environment variables (DB credentials, Kafka brokers, etc.). *No secrets will be hardcoded.*

### Django Backend (E-commerce API)
- **Django Project & App**: Core API for managing products and receiving reviews.
- **Models**: Fat models for `Product` and `Review` to encapsulate business logic.
- **Views**: Thin views using Django REST Framework for API endpoints.
- **Kafka Producer**: Asynchronous pushing of review payloads to Kafka. We will use a lightweight background thread or async utility within Django to ensure it does not block the main web server event loop.

### Stream Processing (Python NLP Consumer)
- **Consumer Script**: A standalone Python application that subscribes to the Kafka review topic.
- **NLP Logic**: Calculates sentiment scores (positive, negative, neutral, compound) using NLTK/VADER.
- **Database Integration**: Writes processed results and metrics back to PostgreSQL using parameterized queries. Implements exponential backoff/retry mechanisms for DB connection failures.

### Frontend (Streamlit Dashboard)
- **Streamlit App**: Real-time visualization dashboard.
- **Data Fetching**: Queries PostgreSQL for aggregated sentiment metrics and recent reviews. Uses `st.cache_data` with TTL and clean polling to prevent redundant loads or memory leaks.

## Subagent Roles

To accelerate development, we will execute tasks conceptually aligned with these roles:

1. **Infra & DB**: Focuses on `docker-compose.yml`, PostgreSQL setup, Kafka/Zookeeper configuration, and networking.
2. **Backend API**: Focuses on the Django REST Framework setup, Models, Views, and the asynchronous Kafka Producer integration.
3. **NLP Consumer**: Focuses on the Python consumer script, NLP integration, robust PostgreSQL writes, and error handling.
4. **Dashboard**: Focuses on the Streamlit UI, database polling, and real-time visualizations.

## Sprint Task Breakdown

### Day 1: Infrastructure & Backend
- [ ] Initialize project directory structure.
- [ ] Create `docker-compose.yml` with PostgreSQL, Zookeeper, and Kafka services.
- [ ] Set up Django project and `reviews` app.
- [ ] Define `Product` and `Review` models (Fat Models paradigm).
- [ ] Create Django REST Framework serializers and views (Thin Views).
- [ ] Implement asynchronous Kafka producer logic in Django.
- [ ] Containerize Django backend (`Dockerfile`).

### Day 2: Stream Processing, Frontend, & E2E Testing
- [ ] Develop Python NLP Consumer script using the chosen NLP library.
- [ ] Implement PostgreSQL connection pooling and retry mechanisms in the consumer.
- [ ] Containerize NLP Consumer (`Dockerfile`).
- [ ] Build Streamlit Dashboard for sentiment visualization.
- [ ] Implement robust state management and data polling in Streamlit.
- [ ] Containerize Streamlit application (`Dockerfile`).
- [ ] End-to-End Integration Testing: Send mock reviews and verify dashboard updates.

## Verification Plan

### Automated Tests
- Unit tests for Django models and API endpoints.
- Unit tests for the NLP consumer's sentiment calculation logic.

### Manual Verification
- `docker-compose up --build` to ensure all containers start cleanly.
- Send POST requests to the Django API to submit reviews.
- Verify Kafka consumer logs indicate successful consumption and DB insertion.
- Access Streamlit dashboard at `http://localhost:8501` to view real-time updates.
