import { Kafka } from "kafkajs";

const kafka = new Kafka({
  clientId: "nepal-pulse-ingestion",
  brokers: ["localhost:9092"],
});

const producer = kafka.producer();

async function run() {
  try {
    await producer.connect();

    const message = {
      source: "test-node-service",
      title: "नेपाल समाचार परीक्षण",
      summary:
        "This is the first message sent from the Node.js ingestion service.",
      language: "ne",
      category: "general",
      url: "https://example.com/test-news",
      scraped_at: new Date().toISOString(),
    };

    await producer.send({
      topic: "raw-news",
      messages: [
        {
          value: JSON.stringify(message),
        },
      ],
    });

    console.log("✅ Message sent to Kafka topic raw-news");
    console.log(message);
  } catch (error) {
    console.error("❌ Error sending message:", error);
  } finally {
    await producer.disconnect();
  }
}

run();
