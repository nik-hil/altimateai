# V0

 - Initial Data Model: Started with a simple dictionary to store queries in memory for the MVP. query_id, query_text, user_id, timestamp are key fields. Lineage is a dictionary.
 - Lineage Extraction: Used basic string parsing to identify tables and columns. Aware this is rudimentary and will need a SQL parser for accuracy in v1.
 - AI Integration: Mocked the AI suggestion endpoint. Will integrate with OpenAI or similar in v1. Need to research suitable prompt engineering techniques.


# V1

 - Code splitted in multiple files.
 - We will use sqlparse library to extract lineage more accurately.
 - We'll transition from the in-memory dictionary to a MongoDB database. This allows for persistence and scalability.
 - Retrieve from MongoDB: The queries dictionary is no longer used. Instead, we use await database.retrieve_query(query_id) to fetch the query from the MongoDB database.
 - OpenAI Integration: Updated the mocked get_ai_suggestions with a call to the OpenAI API. You will need to replace "YOUR_OPENAI_API_KEY" with your actual OpenAI API key. Error handling is added to provide a more robust solution. Please remember that using OpenAI will incur costs.
 - Asynchronous Call: Made the OpenAI API call asynchronous using await to prevent blocking the main thread.

# V2

 - We'll introduce Redis (cluster) to cache query results and lineage information. This will significantly reduce database load and improve response times for frequently accessed queries.
 - Memory Management: Without a TTL, cached data would remain in Redis indefinitely, potentially consuming excessive memory as the number of queries grows. A TTL ensures that less frequently accessed or outdated entries are automatically evicted.
 - Data Freshness: Query definitions or underlying table schemas can change over time. A TTL helps ensure that cached data is not stale. When a cached entry expires, the system will fetch the latest information from the database, maintaining data consistency. If data is mutable and updated very frequently then its better to invalidate cache after every write operation. We will have to add await cache.invalidate_cache(query.query_id) in the update method for the resource.
 - CACHE_TTL Value: The CACHE_TTL is set to 3600 seconds (1 hour) as a reasonable starting point. This value should be adjusted based on factors like:
 - Frequency of Query Updates: If queries are updated frequently, a shorter TTL might be appropriate.
 - Query Access Patterns: If certain queries are accessed very frequently, a longer TTL could be beneficial.
 - Memory Capacity: Available Redis memory should also be considered.


# V3
 - Added Kafka producer and consumer to seprate the lineage processing and storing.
 - Added logger and logger.conf.
 - Fixed code and formatting.
