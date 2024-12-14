# V0

 - Initial Data Model: Started with a simple dictionary to store queries in memory for the MVP. query_id, query_text, user_id, timestamp are key fields. Lineage is a dictionary.
 - Lineage Extraction: Used basic string parsing to identify tables and columns. Aware this is rudimentary and will need a SQL parser for accuracy in v1.
 - AI Integration: Mocked the AI suggestion endpoint. Will integrate with OpenAI or similar in v1. Need to research suitable prompt engineering techniques.