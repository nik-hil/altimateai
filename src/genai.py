import logging
import logging.config

import openai

from settings import settings

logging.config.fileConfig("logging.conf")  # load the config file


logger = logging.getLogger(__name__)
openai.api_key = settings.openai_api_key


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
        suggestions = response.choices[0].text.strip().split("\n")
        return {"suggestions": suggestions}
    except Exception as e:
        logger.execption(f"Error calling OpenAI API: {e}")
        return {
            "suggestions": ["Error getting suggestions"],
            "error": str(e),
        }  # Return a default error message
