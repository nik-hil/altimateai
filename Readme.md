# SQL Query Service with Lineage and AI-powered Suggestions

This project implements a backend system for storing, retrieving, and analyzing SQL queries, including lineage tracking and AI-driven suggestions for query improvements.

## Features

* **Query Storage and Retrieval:** Store SQL queries with metadata (user ID, timestamp) and retrieve them with optional filtering.
* **Lineage Extraction:**  Extract the tables and columns referenced by a query using `sqlparse`.
* **AI-Driven Suggestions:** Integrate with OpenAI's GPT-3 API to provide suggestions for optimizing and improving queries.
* **Caching:** Leverage Redis for caching query results and lineage to improve performance.
* **Asynchronous Processing:** Utilize Kafka to handle lineage extraction and AI suggestion generation asynchronously, enhancing responsiveness under load.
* **Centralized Logging:** Logs are written to a central file (`app.log`) for easier monitoring and debugging.
* **Scalability:** Designed for scalability using MongoDB for persistence, Redis for caching, and Kafka for asynchronous task management.

## Architecture

The system comprises the following components:

* **FastAPI:**  Provides the RESTful API endpoints.
* **MongoDB:** Stores query data and lineage information.
* **Redis:** Caches frequently accessed queries and lineage.
* **Kafka:**  Handles asynchronous tasks (lineage extraction, AI suggestions).
* **OpenAI API:** Provides AI-powered query suggestions.  (Requires an OpenAI API key)

[![](https://mermaid.ink/img/pako:eNqVk99PgzAQx_-Vpr6wZHvxYZk8mOAWE-KMbosvgg8nHD-y0ZIW1GXZ_25bYLCJGI-kvV4_R-57bQ804CFSm8YC8oQs1z4jymT5XgV8ulktyapEsScbFB9pgD6tGG0vEoVl6XE0IpPJLXGeXc-n9yAL5ZkMFD59azN0WIOPnMV8cedZtTPqYdYYptKzzETmECTYRz1AtAXPMlN3v_U6aki3em0mzfxnmTKEGOecyTJDoWTUEdKEzoRou0jpCvsbNLJaDFn4v9rbyh23U7Tj_lZvi5mspxyZo0-rcnQ_hxN6lF0QfZL0dy7rpLQagx1IaU5TFoJv0b6KbqJx5U8-07BI7Ov8q8vWhZz4IBjmqwvU0ADDdNXXhp7Nhum6eQ0-nf7E6ZiqBmWQhuqdHXSyT4sEM_WSbOWGILb6ZI-Kg7Lgmz0LqF2IEsdU8DJOqB3BTqpVmYdQ4CIFdSOyUzQH9sp5sz5-AxP-JTE?type=png)](https://mermaid.live/edit#pako:eNqVk99PgzAQx_-Vpr6wZHvxYZk8mOAWE-KMbosvgg8nHD-y0ZIW1GXZ_25bYLCJGI-kvV4_R-57bQ804CFSm8YC8oQs1z4jymT5XgV8ulktyapEsScbFB9pgD6tGG0vEoVl6XE0IpPJLXGeXc-n9yAL5ZkMFD59azN0WIOPnMV8cedZtTPqYdYYptKzzETmECTYRz1AtAXPMlN3v_U6aki3em0mzfxnmTKEGOecyTJDoWTUEdKEzoRou0jpCvsbNLJaDFn4v9rbyh23U7Tj_lZvi5mspxyZo0-rcnQ_hxN6lF0QfZL0dy7rpLQagx1IaU5TFoJv0b6KbqJx5U8-07BI7Ov8q8vWhZz4IBjmqwvU0ADDdNXXhp7Nhum6eQ0-nf7E6ZiqBmWQhuqdHXSyT4sEM_WSbOWGILb6ZI-Kg7Lgmz0LqF2IEsdU8DJOqB3BTqpVmYdQ4CIFdSOyUzQH9sp5sz5-AxP-JTE)

## Getting Started

1. **Clone the repository:**

   ```bash
   git clone https://github.com/nik-hil/altimateai.git  
   cd altimateai
   ```

1. **Install dependencies:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On Linux/macOS
    .venv\Scripts\activate # On Windows
    pip install -r requirements.txt
    ```

1. **Configure environment variables:**

Create a `.env` file in the root directory.

Copy the contents of example.env into .env and fill in the required values:

    
    MONGO_DETAILS="your_mongodb_connection_string"
    OPENAI_API_KEY="your_openai_api_key"
    KAFKA_BOOTSTRAP_SERVERS="your_kafka_bootstrap_servers"
    KAFKA_TOPIC_LINEAGE="query_lineage"
    KAFKA_TOPIC_AI="query_ai"
    KAFKA_CONSUMER_GROUP="your_consumer_group_id"
    REDIS_URL="your_redis_connection_url"
    CACHE_TTL_SECS=3600 #cache ttl
    

1. **Run the application:**

    Using Docker
    ```
    docker build -t sql-query-service .
    docker run -d -p 8000:8000 --env-file .env sql-query-service
    ```
    Without Docker

    Start the FastAPI application: `uvicorn src.main:app --reload`

1. **Run Kafka Consumers in separate terminals:**
    ```bash
    python src/lineage_consumer.py

    python src/ai_consumer.py
    ```
    
    Access the API: The API will be available at http://localhost:8000. Use tools like Postman or curl to interact with the API endpoints. API documentation will be available at http://localhost:8000/docs when application is running.

1. **File Structure**
    ```
    /
    ├── src/
    │   ├── ai_consumer.py          # Kafka consumer for AI suggestions
    │   ├── application.py
    │   ├── cache.py               # Redis caching logic
    │   ├── database.py            # MongoDB interaction
    │   ├── example.env            # Example environment variables (rename to .env)
    │   ├── genai.py
    │   ├── kkafka.py
    │   ├── lineage.py             # Lineage extraction logic
    │   ├── lineage_consumer.py    # Kafka consumer for lineage extraction
    │   ├── logging.conf           # Logging configuration
    │   ├── main.py                # FastAPI application
    │   └── settings.py            # Environment variable management
    ├── requirements.txt          # Project dependencies
    ├── Dockerfile                # Docker build instructions
    └── README.md                  # This file
    ```

## Future Improvements
 - Implement comprehensive automated tests. Test cases not added and code not tested as I m using windows machine.
 - Integrate with an API gateway for authentication, authorization, and rate limiting.
 - Integrate Prometheus for metric collection, open telemetry for instrumentation.
 - Add more sophisticated error handling and monitoring.
 - Implement background tasks for cache invalidation.

