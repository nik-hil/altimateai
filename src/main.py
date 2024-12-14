import json
import logging
import logging.config
import uuid

from fastapi import HTTPException

import cache
import database
from application import app
from genai import get_ai_suggestions
from kkafka import KAFKA_TOPIC_AI, KAFKA_TOPIC_LINEAGE, producer

logging.config.fileConfig("logging.conf")  # load the config file


logger = logging.getLogger(__name__)


# 1. Store Query
@app.post("/queries/")
async def store_query(query_text: str, user_id: str = None):
    logger.info(f"Received request to store query: {query_text[:50]}...")
    query_data = {"query_text": query_text, "user_id": user_id}
    stored_query = await database.add_query(query_data)

    if stored_query:
        # Send message to Kafka for lineage extraction
        await producer.send_and_wait(
            KAFKA_TOPIC_LINEAGE,
            json.dumps(
                {"query_id": str(stored_query.query_id), "query_text": query_text}
            ).encode(),
        )
        # Send message to Kafka for AI suggestions
        await producer.send_and_wait(
            KAFKA_TOPIC_AI,
            json.dumps(
                {"query_id": str(stored_query.query_id), "query_text": query_text}
            ).encode(),
        )

        # cache the base query
        await cache.cache_query(stored_query)

        return stored_query
    else:
        raise HTTPException(status_code=400, detail="Failed to store the query.")


# 2. Retrieve Queries
@app.get("/queries/")
async def retrieve_queries(user_id: str = None, limit: int = 100, skip: int = 0):
    return await database.retrieve_queries(user_id, limit, skip)


# 3. Get Lineage (Updated for Async)
@app.get("/queries/{query_id}/lineage")
async def get_lineage(query_id: uuid.UUID):
    # Check cache first
    logger.info(f"Retriving {query_id=}")
    cached_lineage = await cache.get_cached_lineage(query_id)
    if cached_lineage:
        return cached_lineage

    # If not found in cache then get from db. it may not be available in db also as it will be updated by kafka consumer.
    query = await database.retrieve_query(query_id)
    if not query:
        raise HTTPException(status_code=404, detail="Query not found")

    if query.lineage:
        return query.lineage
    else:
        return {
            "status": "Lineage is being processed. Please try again later."
        }  # lineage is not in db as it is being processed


# 4. Get AI Suggestions (Updated for Async)
@app.get("/queries/{query_id}/suggestions")
async def get_suggestions(query_id: uuid.UUID):
    logger.info(f"Retriving ai suggestions {query_id=}")
    query = await database.retrieve_query(query_id)
    if not query:
        raise HTTPException(status_code=404, detail="Query not found")

    if "suggestions" in query.model_dump():  # check if suggestions already added in db
        return {"suggestions": query.suggestions}
    else:
        return {"status": "Suggestions are being processed. Please try again later."}
