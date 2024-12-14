import aiokafka

from application import app
from settings import settings

KAFKA_BOOTSTRAP_SERVERS = settings.kafka_bootstrap_servers
KAFKA_TOPIC_LINEAGE = settings.kafka_topic_lineage
KAFKA_TOPIC_AI = settings.kafka_topic_ai
KAFKA_GROUP_ID = settings.kafka_consumer_group

producer = aiokafka.AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
consumer = aiokafka.AIOKafkaConsumer(
    KAFKA_TOPIC_LINEAGE,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    group_id=KAFKA_GROUP_ID,
)


@app.on_event("startup")
async def startup_event():
    await producer.start()


@app.on_event("shutdown")
async def shutdown_event():
    await producer.stop()
