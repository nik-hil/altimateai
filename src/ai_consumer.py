import asyncio
import json
import logging
import logging.config
import uuid

import backoff
import openai

import cache
import database
from genai import get_ai_suggestions
from kkafka import consumer

logging.config.fileConfig("logging.conf")  # load the config file


logger = logging.getLogger(__name__)


@backoff.on_exception(
    backoff.expo, (openai.error.APIError, openai.error.RateLimitError), max_tries=3
)
# Retry only for OpenAI API errors
async def get_ai_suggestions_with_retry(query: str):  # retry logic for openai
    return await get_ai_suggestions(query)


@backoff.on_exception(backoff.expo, Exception, max_tries=5)
async def process_message(msg):
    try:
        query_data = json.loads(msg.value.decode())
        query_id = uuid.UUID(query_data["query_id"])
        suggestions = await get_ai_suggestions_with_retry(query_data["query_text"])
        success = await database.update_query_suggestions(query_id, suggestions)
        if success:
            updated_query = await database.retrieve_query(query_id)
            await cache.cache_query(updated_query)  # use cache_query
        logger.info(f"AI suggestions processed for query {query_id}")
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding message: {msg.value} Error: {e}")

    except Exception as e:
        logger.exception(f"Error processing message:  {msg.value}, Error: {e}")


async def consume_ai():
    await consumer.start()
    try:
        async for msg in consumer:
            await process_message(msg)

    finally:
        await consumer.stop()


if __name__ == "__main__":
    asyncio.run(consume_ai())
