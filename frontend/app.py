import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import os
import time

st.set_page_config(layout="wide", page_title="Live E-Commerce Sentiment")

st.title("🛒 Live E-Commerce Sentiment Analysis Pipeline")
st.markdown("Real-time sentiment monitoring of product reviews.")

DJANGO_API_URL = os.environ.get("DJANGO_API_URL", "http://django_backend:8000/api/reviews/")

@st.cache_data(ttl=5)
def fetch_reviews():
    try:
        response = requests.get(DJANGO_API_URL, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        st.warning(f"Connecting to Django backend at {DJANGO_API_URL}...")
        return []
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return []

# Auto-refresh using Streamlit's fragment or just by a rerun button/timer.
# The user prompt says "(using st_autorefresh or Streamlit's native time-based caching/reruns)".
# Let's use st.button and a cached fetch_reviews with ttl.
if st.button("Refresh Data"):
    fetch_reviews.clear()

reviews = fetch_reviews()

if not reviews:
    st.info("No reviews available yet or backend is still booting up.")
else:
    df = pd.DataFrame(reviews)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Recent Reviews")
        st.dataframe(df[['product', 'text', 'rating', 'sentiment_label', 'sentiment_score']].sort_values(by='sentiment_score', ascending=False, na_position='last'))
        
    with col2:
        st.subheader("Sentiment Distribution")
        # Filter out reviews where sentiment_label is None
        df_sent = df.dropna(subset=['sentiment_label'])
        if not df_sent.empty:
            fig = px.pie(df_sent, names='sentiment_label', title='Sentiment Labels Breakdown', color='sentiment_label', color_discrete_map={'Positive':'green', 'Negative':'red', 'Neutral':'gray'})
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No sentiment labels computed yet.")

# Simple sleep and rerun approach for auto-refresh:
time.sleep(5)
st.rerun()
