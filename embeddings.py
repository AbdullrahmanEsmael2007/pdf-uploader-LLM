from langchain_openai import OpenAIEmbeddings

embedding = OpenAIEmbeddings()

from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
client = OpenAI()


response = client.embeddings.create(
    input="a",
    model="text-embedding-3-small"
)

print(response.data[0].embedding)