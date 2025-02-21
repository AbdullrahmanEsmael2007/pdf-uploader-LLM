
from openai import OpenAI
import os
import dotenv

dotenv.load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


from langchain_openai import OpenAIEmbeddings


def get_embedding_function() -> OpenAIEmbeddings:
    """Returns the embedding function."""
    embedding = OpenAIEmbeddings()
    
    return embedding
