import motor.motor_asyncio
from pymongo.errors import DuplicateKeyError
import uuid
import datetime
from pydantic import BaseModel, Field


MONGO_DETAILS = "mongodb://localhost:27017" # Replace your connection string here

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.sql_query_service # Database Name
query_collection = database.get_collection("queries") # Collection Name


class Query(BaseModel):
    query_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    query_text: str
    user_id: str = None  
    created_at: datetime.datetime = datetime.datetime.utcnow()
    lineage: dict = {}


async def add_query(query_data: dict):
    try:
      query = Query(**query_data)
      result = await query_collection.insert_one(query.model_dump())
      return query # return created query
    except DuplicateKeyError:
      return None #ideally we would want to retry after sometime


async def retrieve_queries(user_id: str = None, limit: int = 100, skip: int=0): #pagination
  query_filter = {}

  if user_id:
    query_filter["user_id"] = user_id

  queries = []
  async for query_record in query_collection.find(query_filter).skip(skip).limit(limit): #pagination added
    queries.append(Query(**query_record))  
  return queries


async def retrieve_query(query_id: uuid.UUID):
  query_record = await query_collection.find_one({"query_id": query_id})
  if query_record:
    return Query(**query_record)
  return None



async def update_query_lineage(query_id: uuid.UUID, lineage:dict):
    result = await query_collection.update_one({"query_id": query_id}, {"$set": {"lineage": lineage}})    
    return result.modified_count > 0