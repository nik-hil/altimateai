import aioredis
import json
import pickle # for complex python objects
import uuid
from pydantic import BaseModel


REDIS_URL = "redis://localhost:6379" # Replace with your Redis connection URL
redis = aioredis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)
CACHE_TTL_SECS = 3600  # Default TTL of 1 hour (adjust as needed)


async def cache_query(query:BaseModel , lineage: dict = None, ttl: int = CACHE_TTL_SECS):
    query_id_str = str(query.query_id) # Convert UUID to string for Redis key
    
    # Store the query using pickle
    pickled_query = pickle.dumps(query)
    await redis.set(f"query:{query_id_str}", pickled_query, ex=ttl)

    if lineage:    
       await redis.set(f"lineage:{query_id_str}", json.dumps(lineage)) # json for simple dicts

async def get_cached_query(query_id: uuid.UUID):
  query_id_str = str(query_id)
  cached_data = await redis.get(f"query:{query_id_str}")  
  if cached_data:
      return pickle.loads(cached_data) # Unpickle the query
  return None


async def get_cached_lineage(query_id: uuid.UUID):
    query_id_str = str(query_id)
    cached_data = await redis.get(f"lineage:{query_id_str}")
    if cached_data:
        return json.loads(cached_data)
    return None

async def invalidate_cache(query_id: uuid.UUID):
    query_id_str = str(query_id)
    await redis.delete(f"query:{query_id_str}")
    await redis.delete(f"lineage:{query_id_str}")