import json
import pandas as pd
import streamlit as st
from kafka import KafkaConsumer
from collections import Counter
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

BOOTSTRAP_SERVERS = "localhost:9092"
TOPIC = "processed-news"

st.set_page_config(page_title="Nepal Pulse Dashboard", layout="wide")

st.title("🇳🇵 Nepal Pulse")
st.subheader("Real-Time Knowledge Discovery Engine for Nepali News Streams")

@st.cache_data(ttl=10)
def load_messages():
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        consumer_timeout_ms=3000,
        value_deserializer=lambda x: json.loads(x.decode("utf-8"))
    )

    rows = []
    for message in consumer:
        rows.append(message.value)

    return rows

rows = load_messages()

if not rows:
    st.warning("No processed news messages found yet.")
    st.stop()

df = pd.DataFrame(rows)

st.metric("Total Processed Articles", len(df))

col1, col2 = st.columns(2)

with col1:
    st.subheader("Source Distribution")
    source_counts = df["source"].value_counts()
    st.bar_chart(source_counts)

with col2:
    st.subheader("Languages")
    lang_counts = df["language"].value_counts()
    st.bar_chart(lang_counts)

st.subheader("🔥 Trending Topics")

texts = df["cleaned_title"].dropna().astype(str).tolist()
topics = []

if len(texts) >= 5:
    vectorizer = CountVectorizer(stop_words="english")
    X = vectorizer.fit_transform(texts)

    lda = LatentDirichletAllocation(n_components=3, random_state=42)
    lda.fit(X)

    words = vectorizer.get_feature_names_out()

    for topic in lda.components_:
        top_words = [words[i] for i in topic.argsort()[-5:]]
        topics.append(", ".join(top_words))

for i, topic in enumerate(topics):
    st.write(f"**Topic {i+1}:** {topic}")

st.subheader("Latest Processed News")
st.dataframe(
    df[["source", "title", "cleaned_title", "scraped_at", "processed_at"]],
    use_container_width=True
)

st.subheader("Top Frequent Words")

all_text = " ".join(df["cleaned_title"].dropna().astype(str).tolist()).lower()
words = re.findall(r"\b[a-zA-Z]+\b", all_text)

stopwords = {
    "the", "a", "an", "in", "on", "at", "to", "for", "of", "and", "or",
    "is", "are", "with", "from", "this", "that", "as", "by", "his", "her",
    "its", "be", "after", "amid", "over", "into"
}

filtered_words = [w for w in words if w not in stopwords and len(w) > 2]
word_counts = Counter(filtered_words).most_common(15)

word_df = pd.DataFrame(word_counts, columns=["word", "count"]).set_index("word")
st.bar_chart(word_df)

st.subheader("Raw Data Preview")
st.json(rows[:5])

st.markdown("---")
st.caption("Built using Kafka, Node.js, Python, and Machine Learning")