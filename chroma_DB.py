from langchain_community.vectorstores import Chroma
import os
from termcolor import colored

def create_chroma_db(chunked_results, embedding_function, persist_directory):
    """Create a Chroma vector db from a list of documents."""

    if os.path.exists(persist_directory):
        print(f"\t{colored('Persist directory exists, deleting it', 'yellow')}")
        sys_command = f"rm -r {persist_directory}"
        os.system(sys_command)

  
    print(f"\t{colored('Creating new directory', 'green')}")

    vectordb = Chroma.from_documents(
        documents=chunked_results,
        embedding=embedding_function,
        persist_directory=persist_directory
    )

    print(f"\t{colored('Vector db created', 'green')}")
    return vectordb
