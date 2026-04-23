import json
from kafka import KafkaConsumer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

BOOTSTRAP_SERVERS = "localhost:9092"
TOPIC = "processed-news"

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=BOOTSTRAP_SERVERS,
    auto_offset_reset="latest",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

print("✅ Listening for processed news...")

texts = []

for message in consumer:
    data = message.value
    text = data.get("cleaned_title", "")

    if text:
        texts.append(text)

    # Run model every 10 articles
    if len(texts) >= 10:
        print("\n🔥 Running Topic Modeling...\n")

        vectorizer = CountVectorizer(stop_words="english")
        X = vectorizer.fit_transform(texts)

        lda = LatentDirichletAllocation(n_components=3, random_state=42)
        lda.fit(X)

        words = vectorizer.get_feature_names_out()

        for i, topic in enumerate(lda.components_):
            print(f"\n📌 Topic {i+1}:")
            top_words = [words[i] for i in topic.argsort()[-6:]]
            print(", ".join(top_words))

        texts = []