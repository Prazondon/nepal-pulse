## Nepal Pulse  

# Real-Time Knowledge Discovery Engine for Nepali News Streams

# Overview

Nepal Pulse is a real-time distributed data pipeline that collects news from multiple Nepali and English news websites, processes the data using Kafka and Python, applies machine learning (topic modeling), and displays insights through a live dashboard.

This project demonstrates a complete end-to-end system including:
- Data ingestion
- Streaming with Kafka
- Data processing
- Machine learning
- Visualization

---

# Architecture

News Websites
↓
Node.js Scraper (Ingestion)
↓
Kafka (raw-news)
↓
Python Processing
↓
Kafka (processed-news)
↓
Topic Modeling (ML)
↓
Streamlit Dashboard

---

## Technologies Used

- Node.js (TypeScript)
- Axios & Cheerio (Web scraping)
- Apache Kafka (Streaming)
- Docker (Containerization)
- Python
- kafka-python
- Scikit-learn (Machine Learning)
- Streamlit (Dashboard)
- Pandas

---

## Features

- Scrapes headlines from **20+ Nepali news websites**
- Real-time streaming using Kafka
- Cleans and normalizes text
- Topic modeling using LDA
- Interactive dashboard visualization
- Modular architecture

---

## Requirements

Install the following before running:

- Docker Desktop
- Node.js (v18+ recommended)
- Python 3
- Git

---

## 1. Clone the Repository
---
```bash
git clone https://github.com/rabin9863/nepal-pulse.git
cd nepal-pulse
---

## 2. Start Kafka

docker compose up -d

Verify:
docker ps

You should see:
nepal-pulse-kafka
nepal-pulse-zookeeper

## 3. Setup Ingestion Service (Node.js)
cd ingestion
npm install

## 4. Setup Processing Service (Python)
cd ../processing
python3 -m venv venv
source venv/bin/activate
pip install kafka-python scikit-learn nltk

## 5. Setup Dashboard
cd ../dashboard
python3 -m venv venv
source venv/bin/activate
pip install streamlit kafka-python pandas scikit-learn



# RUNNING THE PROJECT

 Open 4 separate terminals

 Terminal 1 — Processor
cd nepal-pulse/processing
source venv/bin/activate
python processor.py

 Terminal 2 — Topic Modeling
cd nepal-pulse/processing
source venv/bin/activate
python topic_model.py

 Terminal 3 — Dashboard
cd nepal-pulse/dashboard
source venv/bin/activate
python -m streamlit run app.py

Open in browser:
http://localhost:8501

 Terminal 4 — Scraper
cd nepal-pulse/ingestion
npx tsx src/scraper.ts

## Normal Startup Order (IMPORTANT)
Every time you run the project:

1. docker compose up -d
2. run processor.py
3. run topic_model.py
4. run dashboard
5. run scraper

## How It Works

Scraper collects news headlines from websites
Sends data to Kafka topic raw-news
Python processor cleans and processes the data
Sends cleaned data to processed-news
Topic model extracts trending topics
Dashboard visualizes everything

## Dashboard Includes
Total processed articles
Source distribution
Language distribution
Trending topics
Latest news table
Frequent words chart

## Stop the Project
Stop Kafka:
docker compose down
Stop scripts:
CTRL + C

## Troubleshooting

Kafka not connecting
docker compose up -d
docker ps

ModuleNotFoundError: kafka
source venv/bin/activate

pip install kafka-python
ModuleNotFoundError: sklearn
pip install scikit-learn
Scraper not found
Make sure you're in ingestion folder:
cd ingestion
npx tsx src/scraper.ts

## Project Structure
nepal-pulse/
├── ingestion/
├── processing/
├── dashboard/
├── docker-compose.yml
└── README.md
## Conclusion
Nepal Pulse demonstrates a complete real-time pipeline using:
distributed systems
streaming architecture
machine learning
visualization

## Author

Rabin Dhakal

---
