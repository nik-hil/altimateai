from pydantic import BaseSettings


class Settings(BaseSettings):
    mongo_details: str
    openai_api_key: str
    kafka_bootstrap_servers: str
    kafka_topic_lineage: str
    kafka_topic_ai: str
    kafka_consumer_group: str
    redis_url: str
    cache_ttl_secs: int

    class Config:
        env_file = ".env"  # Load environment variables from .env file
        env_file_encoding = "utf-8"


settings = Settings()
