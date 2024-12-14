import asyncio
import json
import logging
import logging.config
import uuid

import backoff

import cache
import database
import lineage
from kkafka import consumer

logging.config.fileConfig("logging.conf")


logger = logging.getLogger(__name__)


@backoff.on_exception(
    backoff.expo, Exception, max_tries=5
)  # retry with exponential backoff
async def process_message(msg):  # Separate function for processing with retry logic
    try:
        query_data = json.loads(msg.value.decode())
        query_id = uuid.UUID(query_data["query_id"])
        extracted_lineage = lineage.extract_lineage(query_data["query_text"])
        success = await database.update_query_lineage(query_id, extracted_lineage)
        if success:
            updated_query = await database.retrieve_query(query_id)
            await cache.cache_query(updated_query)
        logger.info(f"Lineage processed for query {query_id}")

    except json.JSONDecodeError as e:
        logger.error(f"Error decoding message: {msg.value}, Error: {e}")

    except Exception as e:  # Catching remaining errors related to db or cache
        logger.exception(f"Error processing message: {msg.value}, Error: {e}")


async def consume_lineage():
    await consumer.start()
    try:
        async for msg in consumer:
            await process_message(msg)
    except Exception as e:  # Consumer level exception handling
        logger.exception(f"Consumer error: {e}")
    finally:
        await consumer.stop()


if __name__ == "__main__":
    asyncio.run(consume_lineage())
