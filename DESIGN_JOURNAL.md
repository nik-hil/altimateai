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
