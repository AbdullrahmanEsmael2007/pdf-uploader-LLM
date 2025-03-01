
from openai import OpenAI
from termcolor import colored
from langchain_openai import OpenAIEmbeddings
import streamlit as st

def get_embedding_function(api_key) -> OpenAIEmbeddings:
    client = OpenAI(api_key=api_key)
    """Returns the embedding function."""
    print(colored(f"{get_embedding_function.__name__}: ", 'yellow'))
    print(colored("\tGetting embedding function...", 'yellow'))
    embedding = OpenAIEmbeddings()
    print(colored("\tEmbedding function created", 'yellow'))
    
    return embedding

