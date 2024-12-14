from fastapi import FastAPI, HTTPException, Depends
import database
import lineage
import uuid
import openai
import cache

openai.api_key = "YOUR_OPENAI_API_KEY"

async def get_ai_suggestions(query: str):
  try:
      response = openai.Completion.create(
          engine="text-davinci-003",
          prompt=f"Suggest improvements to the following SQL query:\n\n{query}",
          max_tokens=150,
          n=1,
          stop=None,
          temperature=0.7,
      )
      suggestions = response.choices[0].text.strip().split('\n')      
      return {"suggestions": suggestions}
  except Exception as e:
      print(f"Error calling OpenAI API: {e}")
      return {"suggestions": ["Error getting suggestions"], "error": str(e) } # Return a default error message


app = FastAPI()

# 1. Store Query
@app.post("/queries/")
async def store_query(query_text: str, user_id: str = None):
    query_data = {"query_text": query_text, "user_id": user_id}
    
    stored_query = await database.add_query(query_data)
    if stored_query:
      extracted_lineage = lineage.extract_lineage(query_text) # get lineage for caching
      await cache.cache_query(stored_query, extracted_lineage) # cache query and lineage
      return stored_query
    else:
      raise HTTPException(status_code=400, detail="Failed to store the query.")


# 2. Retrieve Queries
@app.get("/queries/")
async def retrieve_queries(user_id: str = None, limit:int=100, skip:int=0):    
    return await database.retrieve_queries(user_id, limit, skip)


# 3. Get Lineage (updated to process lineage asynchronously)
@app.get("/queries/{query_id}/lineage")
async def get_lineage(query_id: uuid.UUID):
    cached_lineage = await cache.get_cached_lineage(query_id)

    if cached_lineage:
        return cached_lineage

    #If not in cache, fetch from DB and update cache
    query = await database.retrieve_query(query_id)
    if not query:
        raise HTTPException(status_code=404, detail="Query not found")

    if not query.lineage:      
      extracted_lineage = lineage.extract_lineage(query.query_text)
      update_success = await database.update_query_lineage(query_id, extracted_lineage)
      if not update_success:
          raise HTTPException(status_code=500, detail="Failed to update lineage")
    else:
      extracted_lineage = query.lineage


    await cache.cache_query(query, extracted_lineage) # update the cache. 
    return extracted_lineage



# 4. Get AI Suggestions (Corrected)
@app.get("/queries/{query_id}/suggestions")
async def get_suggestions(query_id: uuid.UUID):
    query = await database.retrieve_query(query_id)  # Retrieve from MongoDB

    if not query:
        raise HTTPException(status_code=404, detail="Query not found")

    suggestions = await get_ai_suggestions(query.query_text) # await call for openai
    return suggestions
