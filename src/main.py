from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import uuid
import datetime

# Mock AI Response - Replace with actual AI integration in v1
def get_ai_suggestions(query: str):
    return {"suggestions": ["Consider using an index on column X", "Rewrite using a common table expression (CTE)"]}

app = FastAPI()

class Query(BaseModel):
    query_text: str
    user_id: str = None  
    created_at: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)

class QueryWithLineage(BaseModel):
  query_id: uuid.UUID
  query_text: str
  user_id: str = None
  created_at: datetime.datetime
  lineage: dict = {}

queries = {} # using in memory dict for now. Will change to DB in future

# 1. Store Query
@app.post("/queries/", response_model=QueryWithLineage)
async def store_query(query: Query):
    query_id = uuid.uuid4()
    lineage = extract_lineage(query.query_text) # implement basic lineage
    stored_query = QueryWithLineage(query_id = query_id, query_text=query.query_text, user_id=query.user_id, created_at=query.created_at, lineage=lineage)
    queries[query_id] = stored_query
    return stored_query

# basic lineage extraction
def extract_lineage(query: str):
    # Basic string parsing for MVP - Improve in v1
    words = query.lower().split()
    tables = []
    columns = []

    keywords = ["from", "join", "update", "insert", "select"]

    for i, word in enumerate(words):
        if word in keywords :
          if word == "select":
            columns.extend(words[i+1].split(',')) # naive column extraction
          else:
            tables.append(words[i+1])

    return {"tables": list(set(tables)), "columns": list(set(columns))}


# 2. Retrieve Queries
@app.get("/queries/", response_model=list[QueryWithLineage])
async def retrieve_queries(user_id: str = None):
  if user_id:
    return [q for q in queries.values() if q.user_id == user_id ]
  else:
    return list(queries.values())


# 3. Get Lineage
@app.get("/queries/{query_id}/lineage", response_model=dict)
async def get_lineage(query_id: uuid.UUID):
    if query_id not in queries:
        raise HTTPException(status_code=404, detail="Query not found")
    return queries[query_id].lineage

# 4. Get AI Suggestions
@app.get("/queries/{query_id}/suggestions")
async def get_suggestions(query_id: uuid.UUID):
  if query_id not in queries:
        raise HTTPException(status_code=404, detail="Query not found")
  
  suggestions = get_ai_suggestions(queries[query_id].query_text)
  return suggestions

