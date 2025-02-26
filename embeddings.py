
from openai import OpenAI
import os
import dotenv
from termcolor import colored
dotenv.load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

print(colored(api_key, 'yellow'))
from langchain_openai import OpenAIEmbeddings


def get_embedding_function() -> OpenAIEmbeddings:
    """Returns the embedding function."""
    print(colored(f"{get_embedding_function.__name__}: ", 'yellow'))
    print(colored("\tGetting embedding function...", 'yellow'))
    embedding = OpenAIEmbeddings()
    print(colored("\tEmbedding function created", 'yellow'))
    
    return embedding

