from langchain_community.vectorstores import Chroma
import os
from termcolor import colored

def create_chroma_db(chunked_results, embedding_function, persist_directory):
    """Create a Chroma vector db from a list of documents."""
    print(f"{create_chroma_db.__name__}:")
    
        
    print(f"\t{colored('Creating new directory', 'green')}")
    vectordb = Chroma.from_documents(
        documents=chunked_results,
        embedding=embedding_function,
        persist_directory=persist_directory
    )

    print(f"\t{colored('Vector db created', 'green')}")
    return vectordb


