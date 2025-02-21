from langchain_community.vectorstores import Chroma
import os

def create_chroma_db(chunked_results, embedding_function, persist_directory):
    """Create a Chroma vector db from a list of documents."""
    if os.path.exists(persist_directory):
        import shutil
        shutil.rmtree(persist_directory)
        
    vectordb = Chroma.from_documents(
        documents=chunked_results,
        embedding=embedding_function,
        persist_directory=persist_directory
    )

    return vectordb


